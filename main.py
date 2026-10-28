import requests #allow us to make HTTP requests to the API
import csv #allow us to work with CSV files

url = "https://dev-task.elancoapps.com/data/tick-sightings" #save the url of the tick sightings API in a variable

try:  #any error that occurs during the request will be caught in this block
    response = requests.get(url, timeout=20) #max time to wait for a response
    print("Status Code:", response.status_code) #it shows the status of the request 
    response.raise_for_status() #raise an error if the request was unsuccessful
    data = response.json() # convert the response to JSON format
    city = input("Enter a UK city:").strip() #ask the user to enter a city name
    species_choice = input("Enter a tick species (or press Enter to see all species):").strip() #ask the user to enter a tick species
    city_sightings = [] # this is an empty list for matching sighting 

    for sighting in data: #loop through all tick sighting 
        city_match = sighting.get("location", "").lower() == city.lower() #check if the location of the sighting matches the chosen city
        species_match = (not species_choice or sighting.get("species","").lower() == species_choice.lower())
        
        if city_match and species_match: #check if both the location and species match
            city_sightings.append(sighting) #add the matching sighting to the list
    double_check = sum(1 for sighting in data if sighting.get("location", "").lower() == city.lower() #count the number of sightings in the chosen city
    and (not species_choice or sighting.get("species","").lower() == species_choice.lower()))
    total_sightings = len(data) #get the total number of records in the data
    city_sightings_count = len(city_sightings) #get the number of sightings in the chosen city
    
    if city_sightings_count == 0: #check if there are no matching sightings
        print(f"No tick sightings found for {city} with species '{species_choice}'") #display a message if no sightings are found
        print("Please check the city name and species name for any typos and try again.") #display a message to check for typos
    print("\nTick Sightings Table")
    print(f"{'Date':<22}{'City':<18}{'Species':<30}{'Latin Name'}") #print the header of the table
    print("-"*80) #print a deprator line
    species_counts = {} #create an empty dictionary to store the counts of each species
    
    for sighting in city_sightings: #loop through all matching sightings
        species = sighting.get("species", "") #get the species of the tick
        if species in species_counts: #check if the species is already in the dictionary
            species_counts[species] += 1 #increment the count of the species by 1
        else:
            species_counts[species] = 1 #add the species to the dictionary with a count of 1
        date = sighting.get("date", "") #get the date of the sighting
        location = sighting.get("location", "") #get the location of the sighting
        species = sighting.get("species", "") #get the species of the tick
        latin_name = sighting.get("latinName", "Unknown") #get the latin name of the tick
        print(f"{date:<22}{location:<18}{species:<30}{latin_name}") #print the details of each matching sighting
    print("\nTick Species Statistics")
    
    for species, count in species_counts.items():
        print(f"{species:<25}: {count}")
    print("Total:", sum(species_counts.values())) #print the total number of sightings for all species
    total_species = sum(species_counts.values()) #get the total number of sightings for all species
    print("\nTick Species percentage")
    
    for species, count in species_counts.items():
        percentage = (count / total_species) * 100 if total_species > 0 else 0 #calculate the percentage of each species
        print(f"{species:<25}: {percentage:.2f}%") #print the percentage of each species
    print("Double check:", double_check) #print the number of sightings in the chosen city
    print("Do the counts match?", double_check == city_sightings_count) #check if the counts match
    print("Total tick sightings:", total_sightings) #print the total number of sightings
    print("Matching sightings:", city_sightings_count) #print the number of matching sightings
    #print("Data type:", type(data))#print the type of the data
    #print("Data preview:", str(data)[:1024]) #print the first 1024 characters of the data

    if city_sightings_count > 0: #check if there are matching sightings to export
        export_choice = input("Do you want to export the matching sightings to a CSV file? (yes/no): ").strip().lower()

        if export_choice == "yes": #check if the user wants to export the matching sightings to a CSV file
            filename = "tick_sightings.csv" #set the filename for the CSV file

            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file) #create a CSV writer object
                writer.writerow(["Date", "City", "Species", "Latin Name"]) #write the header row to the CSV file

                for sighting in city_sightings: #loop through all matching sightings
                    writer.writerow([ #write the details of each matching sighting to the CSV file
                        sighting.get("date", ""),
                        sighting.get("location", ""),
                        sighting.get("species", ""),
                        sighting.get("latinName", "Unknown")
                    ])

            print("CSV file exported successfully!", filename) #display a message to indicate that the CSV file has been exported successfully
        else: #check if the user does not want to export the matching sightings to a CSV file
            print("CSV export skipped.") #display a message to indicate that the CSV export has been skipped
    else: #check if there are no matching sightings to export
        print("No matching sightings to export.") #display a message to indicate that there are no matching sightings to export

               

except ValueError as e: #catch any errors that occur during the request
    print("JSON error:", e) #display the error message
except requests.exceptions.ConnectionError as e: #catch any connection errors that occur during the request
    print("Connection error:Please check your internet connection and try again.", e) #display the error message
except requests.exceptions.Timeout as e: #catch any timeout errors that occur during the request
    print("Request timed out:", e) #display the error message
except requests.exceptions.RequestException as e: #catch any errors that occur during the request
    print("API request error:", e) #display the error message
