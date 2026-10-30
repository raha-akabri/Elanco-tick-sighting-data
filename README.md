## Elanco Tick Sighting Data Analysis

This project is python based application that gets and analyses tick sighting data from 
an Elanco API.

The aim is to get and process tick sighting data from Elanco's API and provide a simple way to search and analyse the information.

## Features 
- Search tick sightings by city, species and date range
- View the total number of sightings and statistics for each species
- View the number of tick sightings recorded in each city
- Generate weekly and monthly reports to understand trends over time
- Handle connection errors, timeouts, and invalid responses

## Technologies
- Python
- Requests library
- FastAPI
- Datetime
- Counter
- lru cache
- Uvicorn
- Visual Studio Code

## API source
https://dev-task.elancoapps.com/data/tick-sightings
## API Endpoints
http://127.0.0.1:8000/docs
The API includes three endpoints:
- GET /sightings: Search sightings by city, species and date range
- GET /cities: View the number of sightings in each city
- GET /weekly-monthly-report: View weekly and monthly trends


## How to run
- Install Python
- Download the project files
- Open the project folder in Visual Studio Code 
- Run python api.py
- Open http://127.0.0.1:8000/docs in your browser
- Select an endpoint, click "Try it out", and then "Execute"

## YouTube
https://youtu.be/29T1LgBzADY 

## What I Learned
This project helped me develop my software engineering skills and understand how to approach unfamiliar technical challenges. I started by researching different technologies and learning how APIs work before choosing Python and FastAPI.








