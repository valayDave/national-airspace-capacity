import pandas as pd
import json
from . import logger as logger
log = logger.create_logger('Data Loader',logger.logging.INFO)

def get_json_from_file(file_path):
    f = open(file_path)
    return json.load(f)
    
def get_flights_data_frame(file_path) -> pd.DataFrame:
    airlines_json = get_json_from_file(file_path)
    flights = [flight for x in airlines_json for flight in x['flights'] ]  
    df =pd.DataFrame(flights)
    return df

def extract_from_scraping_data(load_data_set):
    '''
        extract_from_scraping_data : Flattens scraping information and filters the ones with most relevant records.  
        @param: load_data_set : This is the Data Structure of the Any Data collected from the Web scraping Interface. 
        [{
            "source": "PHX",
            "destination": "JFK",
            "flights": [
                {
                    "id": 0,
                    "flights": [
                        {
                            "flight_number": "AA2651",
                            "carrier": "American Airlines",
                            "depart_terminal": "PHX",
                            "arrival_terminal": "JFK",
                            "depart_time": 1578295380000,
                            "arrival_time": 1578312000000,
                            "aircraft": "Boeing 737-800 (738)"
                        }
                    ]
                },
            ]
        }] 

        @returns : [
            {
                "flight_number": "AA2651",
                "carrier": "American Airlines",
                "depart_terminal": "PHX",
                "arrival_terminal": "JFK",
                "depart_time": 1578295380000,
                "arrival_time": 1578312000000,
                "aircraft": "Boeing 737-800 (738)"
            }
        ]
    '''
    t = list(map(lambda d : d['flights'],load_data_set))
    filtered_flights_with_routes = list(filter(lambda x : len(x)>0,t))
    k = [item for sublist in filtered_flights_with_routes for item in sublist]
    flattened_flight_data = [item for sublist in k for item in sublist['flights']] 
    flights_with_aircrafts_marked = [i for i in flattened_flight_data if 'aircraft' in i]
    log.info("Number Of Flights Filtered : %d",len(flights_with_aircrafts_marked))
    return flights_with_aircrafts_marked