from . import load as DataLoader
from . import logger as logger
from .graph import Graph
from typing import List
import pendulum
import os 
import json

module_dir = os.path.abspath(os.path.join(os.path.abspath(__file__),'..'))
log = logger.create_logger('Data Transformation',logger.logging.INFO)
airline_capacity_object = DataLoader.get_json_from_file(os.path.join(module_dir,'capacity.json'))
available_aircraft_names = list(airline_capacity_object.keys())

def get_la_time(time_d): 
    return pendulum.timezone('America/Los_Angeles').convert(time_d)


def get_aircraft_capacity(aircraft_string:str):
    global airline_capacity_object
    for aircraft in available_aircraft_names:
        if aircraft.lower() in aircraft_string.lower():
            return (aircraft,airline_capacity_object[aircraft])
    return (None,None)


def round_to_closest_hour(time_data:pendulum.DateTime) -> pendulum.DateTime:
    if time_data.minute == 0:
        return time_data
    elif time_data.minute > 30:
        return time_data.add(minutes=60-time_data.minute)
    else:
        return time_data.subtract(minutes=time_data.minute)


def transform(dataset,start_time=pendulum.datetime(2020,1,6,tz='America/Los_Angeles'),end_time = pendulum.datetime(2020,1,6,23,59,59,tz='America/Los_Angeles')):
    """
    transform : convert Dataset to another form which will aid the creation of the Graph. 
    @param : dataset = [
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
    @param : start_time : {pendulum.DateTime} : the time to consider for the selection of flights given to the Algo 
    @param : end_time : {pendulum.DateTime} : the time to consider for the selection of flights given to the Algo
    @ return : [
            {
                "flight_number": "AA2651",
                "carrier": "American Airlines",
                "depart_terminal": "PHX",
                "arrival_terminal": "JFK",
                "depart_time": 1578295380000,
                "arrival_time": 1578312000000,
                "aircraft": "Boeing 737-800 (738)",
                "aircraft_capacity" : 102,
                "depart_hour" : 12  --> Range of values for this is relative to difference of start_time and end_time in the function's input
                "arrival_hour" : 15 --> Range of values for this is relative to difference of start_time and end_time in the function's input
            }
        ]
    """
    final_dataset = []
    log.debug("Start Time : %s || End Time : %s",start_time.to_datetime_string(),end_time.to_datetime_string())
    for flight_object in dataset:
        aircraft_name,capacity = get_aircraft_capacity(flight_object['aircraft'])
        if capacity is None:
            # $ Ignore Data because There is no Capacity Mapping for the Flight
            continue
        flight_object['aircraft_capacity'] = capacity
        flight_object['aircraft'] = aircraft_name

        # $ Time transformations done here so that all flights are on the same timezone to Map the Capacity of Travel.
        arrival_time = pendulum.from_timestamp(flight_object['arrival_time']/1000)
        depart_time = pendulum.from_timestamp(flight_object['depart_time']/1000)
        arrival_time = round_to_closest_hour(arrival_time)
        depart_time = round_to_closest_hour(depart_time)
        
        if start_time.diff(depart_time,False).in_seconds() < 0:
            log.debug('depart_time < start_time %s %s %s %s',flight_object['flight_number'],flight_object['arrival_terminal'],flight_object['depart_terminal'],get_la_time(depart_time).to_datetime_string())
            # $ Igrnore Data Because depart_time is before start time. 
            continue
        
        if end_time.diff(depart_time,False).in_seconds() > 0:
            # $ Igrnore Data Because depart_time is after end time. 
            log.debug('depart_time > end_time %s %s %s %s',flight_object['flight_number'],flight_object['arrival_terminal'],flight_object['depart_terminal'],depart_time.to_datetime_string())
            continue

        if end_time.diff(arrival_time,False).in_seconds() > 0:
            # $ Igrnore Data Because arrival_time is after end time. 
            log.debug('arrival_time > end_time %s %s %s %s',flight_object['flight_number'],flight_object['arrival_terminal'],flight_object['depart_terminal'],arrival_time.to_datetime_string())
            continue

        flight_object['arrival_time']=arrival_time.timestamp()
        flight_object['depart_time']=depart_time.timestamp()

        # $ Mark the Flights With timestamps into the hour for easier Segregation
        flight_object['depart_hour'] = start_time.diff(depart_time).in_hours()
        flight_object['arrival_hour'] = start_time.diff(arrival_time).in_hours() 
        final_dataset.append(flight_object)
    
    log.info("Filtered Dataset With Flights : %d",len(final_dataset))
    return final_dataset



"""
create_graph : Creates a Graph From Transformed Datastructure. 
@param : source_node : Node of from which flow starts
@param : sink_node : node from of which flow ends
@param : airports : the List of airports to cover.
@param : airline_data : {JSON Array} = Follows Structure From following Json. 
[
    {
        "flight_number": "AA2651",
        "carrier": "American Airlines",
        "depart_terminal": "PHX",
        "arrival_terminal": "JFK",
        "depart_time": 1578295380000,
        "arrival_time": 1578312000000,
        "aircraft": "Boeing 737-800 (738)",
        "aircraft_capacity" : 102,
        "depart_hour" : 12 
        "arrival_hour" : 15
    }
]

Problem Transformation : 
Convert Dataset into Graph .The graph is supposed to help map applicable Flights. 

Node Representation And Edge Creation for Graph : 
    - (AIRPORT_CODE:day_hour) --> This Recognises all nodes Other than Source or Sink.

    - Two More nodes Added As Source(LAX) and Sink(JFK) nodes. 
        - They Will have p_infinity connections to or From them. 
        - Source node connects all (Source:day_hour) nodes with p_infinity
        - all (Sink:day_hour) nodes connect to Sink node with p_infinity

    - All nodes from same Depart terminal will be connected sequentially according to thier depart_time. 
        - Eg SFO:3 -- p_inifinity --> SFO:4 -- p_inifinity -->SFO:5 
        - This is done so that flow is gaurenteed between the nodes for the same airport. 

    - Edge Creation For All Flights Done as follows : 
        - (depart_airport_code_i:depart_time_i) --- aircraft_capacity_i --->  (arrival_airport_code_i:arrival_time_i) for Flight i 
        - Because of P_inf, there will be easy flow among nodes in same Airport so only connecting airports in the way can ensure flow calc is ensured. 

Final Algo :
    1. Until No more path flow. 
        1. BFS To Sink 
        2. Find Path Flow for path. 
        3. Create Residual Graph From Path Flow
"""
def create_graph(source_node:str,sink_node:str,airports:List[str],airline_data:List):
    # $ Create the Nodes in the Graph
    airport_node_data = []
    for airport in airports:
        graph_node_names = [airport+":"+str(depart_time) for depart_time in range(24)]
        airport_node_data+=graph_node_names
    
    Airline_Network_Graph = Graph(source_node,sink_node,airport_node_data)
    p_infinity = float('inf')

    # $ Set Source Node Edges. Each node edge set as p_infinity as a connection for the Source node. Meaning LAX Souce Node Connects LAX:1 , LAX:2, LAX:3 etc
    source_conn_nodes = list(filter(lambda x:source_node in x,Airline_Network_Graph.node_list))
    Airline_Network_Graph.set_edges(source_node,source_conn_nodes,[p_infinity for i in range(len(source_conn_nodes))])
    log.debug(source_conn_nodes)
    # $ Set Edges to Sink Node. Each node edge set as p_inifinity to sink node. Eg. JFK:1 -- p_inifinity --> JFK , JFK:2 -- p_inifinity --> JFK  etc. 
    sink_conn_nodes = list(filter(lambda x:sink_node in x,Airline_Network_Graph.node_list))
    for sink_conn_node in sink_conn_nodes:
        Airline_Network_Graph.set_edge(sink_conn_node,sink_node,p_infinity)
    
    log.debug(sink_conn_nodes)
    # $ set Edges between the Nodes of same Airport. : Each edge is set sequentially according to time of the hour marked in the Graph. Eg. PHX:1 -- p_inifinity --> PHX:2 -- p_inifinity -->PHX:3 etc.
    for airport in airports:
        if airport != source_node or airport !=sink_node:
            for i in range(23):
                Airline_Network_Graph.set_edge(airport+":"+str(i),airport+":"+str(i+1),p_infinity)
    
    
    # $ Connect Which have flights to the Other Nodes. Meaning Add Edge for a Flight in the Following Fashion : 
    for flight_object in airline_data: 
        start_node_name = flight_object['depart_terminal']+":"+str(flight_object['depart_hour'])
        end_node_name = flight_object['arrival_terminal']+":"+str(flight_object['arrival_hour'])
        # print("Marking ",start_node_name,end_node_name)
        edge_weight = flight_object['aircraft_capacity']
        Airline_Network_Graph.set_edge(start_node_name,end_node_name,edge_weight)

    return Airline_Network_Graph
    # print(Airline_Network_Graph.graph[0])
    