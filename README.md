## Elanco Tick Sighting Data Analysis

This project is python based application that gets and analyses tick sighting data from 
an Elanco API.

It allows users to search tick sighting by UK city and species,view results in a table format, calculate statistics, and export filtered records to CSV file.

## Features 
- Get tick sighting data using an HTTP GET  request
- Filter records by city and tick species
- Display matching records in a formatted table
- Calculate species percentages
- Calculate the total number of sighting for each species
- Verify matching records 
- Handle connection errors, timeouts, and invalid responses
- Export filtered data to a CSV file for use in Excel
- Display a meessage when no matching records are found

## Technologies
- Python
- Requested library
- CSV module
- JSON  data
- REST API
- Visual Studio Code

## API Endpoint
https://dev-task.elancoapps.com/data/tick-sightings


## How to run
- Install Python
- Download the project files
- Open the project folder in Visual Studio Code 
- Run python main.py
- Enter a UK city
- Enter a tick species or press Enter to view all species
- Review the results and choose whether to export them to CSV

## Future Improvements 
- Add date range filtering
- Add automated tests
- Develop a web interface








