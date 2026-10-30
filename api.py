from fastapi import FastAPI, HTTPException #create AI  endpoints and return HTTP errors(such sa 404,400...)
from datetime import date, datetime
from collections import Counter
from functools import lru_cache #store results in memory 
import requests #gets data from API

app = FastAPI(title="Elanco Tick Tracking Service")

ELANCO_URL = "https://dev-task.elancoapps.com/data/tick-sightings"

@lru_cache(maxsize=1) #it stores the most recent function call
def get_data(): #define a function
    try:
        response = requests.get(ELANCO_URL, timeout=30) #to get the data from API
        response.raise_for_status() #to detedct unsuccessfful requests
        data = response.json()#converts the JSON 
    except (requests.RequestException, ValueError): #if the request fails 
        raise HTTPException(502, "Unable to get Elanco data") #return a 502 error to the client

    if not isinstance(data, list): #to make sure the API response is a list
        raise HTTPException(502, "Invalid data format")

    valid_records = [] #stores the relaible data
    processed_records = set()#tracks the dudplicates 

    for sighting in data:
        if not isinstance(sighting, dict): #object and list
            continue

        if not all( #check if all three fields are valid
            isinstance(sighting.get(item), str) #check if the value is a string
            and sighting[item].strip()
            for item in ("date", "location", "species")):
            continue #if any check fails skip
        try:
            datetime.fromisoformat(sighting["date"])
        except ValueError: #if the date is invalid
            continue

        record_id = sighting.get("id") #unique ID of thr sighting
        key = (
            ("id", str(record_id))
            if record_id is not None #if no ID, use details of the data
            else ("record",sighting["date"],
                sighting["location"].strip().lower(),
                sighting["species"].strip().lower(),
                str(sighting.get("latinName", "")).lower()))

        if key not in processed_records:
            processed_records.add(key)
            valid_records.append(sighting)

    return valid_records

@app.get("/sightings") #endpoint to search tick sigthing
def get_sightings(
    city: str = "",
    species: str = "",
    start_date: date = "",
    end_date: date =""):

    data = get_data()
    results = [] #stores filtered data

    for sighting in data:
        sighting_date = datetime.fromisoformat(sighting["date"]).date() #conver the date form

        if city and sighting["location"].strip().lower() != city.strip().lower():
            continue #continue if it does match the selected city
        if species and sighting["species"].strip().lower() != species.strip().lower():
            continue 
        if start_date and sighting_date < start_date: #skip sigthing before the slected start date
            continue
        if end_date and sighting_date > end_date: #skip them after the selected end date
            continue

        results.append(sighting) #add the matching to the result 

    return { "total_sightings": len(results), #as a Json response
        "species_statistics": dict(Counter(s["species"] for s in results)),
        "sightings": results}


@app.get("/cities") #endpoint for cities
def get_cities():
    data = get_data()
    counts = Counter(s["location"].strip() for s in data) #how many sightings there are in each city

    return { "total_sightings": len(data),
        "cities": dict(counts.most_common()) } #ordered by sightings count


@app.get("/weekly-monthly-report") 
def get_weekly_and_monthly_report():
    data = get_data()
    weekly = Counter()
    monthly = Counter()

    for sighting in data:
        sighting_date = datetime.fromisoformat(sighting["date"]) #gets the date from the record
        year, week, _ = sighting_date.isocalendar()

        week_name = f"{year}-W{week:02d}" # it will displays the week using two digits
        month_name = sighting_date.strftime("%Y-%m")
        weekly[week_name] += 1 #it will increase if  another sighting happens 
        monthly[month_name] += 1 #same proccess for monthly counter

    return {"total_sightings": len(data),
        "weekly_report": dict(sorted(weekly.items())), #weekly counts in order
        "monthly_report": dict(sorted(monthly.items()))} #monthly counts in order
