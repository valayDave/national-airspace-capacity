import json

source_city = "LAX"
dest_city = "JFK"
in_between = [
    "PHX",
    "SEA",
    "DEN",
    "ATL",
    "ORD",
    "BOS",
    "SFO",
    "IAD",
]

source_to_cities = [[source_city,dest] for dest in in_between]
source_to_cities.append([source_city,dest_city])
cities_to_dest = [[dest,dest_city] for dest in in_between]

rest_of_flights = []

for source in in_between:
    for dest in in_between:
        if source != dest:
            rest_of_flights.append([source,dest])

final_cities = cities_to_dest+source_to_cities+rest_of_flights
fligt_combinations = {
    'flights': final_cities
}
print(len(final_cities) ,len(cities_to_dest),len(source_to_cities),len(rest_of_flights))
with open('flight_dests.json','w') as f:
    json.dump(fligt_combinations,f)