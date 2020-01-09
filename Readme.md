# Problem Statement

You  are  tasked  with  the  **computation  of  the  capacity**  of  a simplified model of the National Airspace System (NAS), **between** 

    Source:  Los  Angeles  (LAX)  and  
    Destina-tion:  New  York  City  (JFK)

**on  January  6,  2020,  in  a  24  hour  time  period,  starting  at  12:00AM  and  ending at  11:59  PM.** 

Apart from these two airports, our simplified NAS consists of the following airports (codes) as well 
- Phoenix (PHX), 
- Seattle (SEA),
- Denver (DEN),
- Atlanta (ATL),
- Chicago (ORD),
- Boston (BOS) 
- Washington DC (IAD). 
- San Francisco (SFO), 

Furthermore, you can assume that our simplified NAS consists ofthree airlines: 
- American Airlines (AA), 
- Delta Airlines (DL)
- United Airlines (UA)

More Information about Problem available [Here](Question.md)

# Running the Code 

- Ensure ``final_dataset.csv`` is present in the ``Dataset`` folder. 
- ``python3 -m venv .env`` 
- ``.env/bin/pip install -r requirements.txt``
- ``.env/bin/python run_algo.py``

# Problem Solution Breakup  

- Data Collection 
- Data Transformation 
- Capacity Calculation 


## 1. Data Collection.
- Array of Source and Destination airports generated using [extract_dests.py](extract_dests.py). 
- Collection Source : https://api.flightstats.com
- [Endpoint Used](https://api.flightstats.com/flex/schedules/rest/v1/json/from/LAX/to/JFK/departing/2019/1/6)

<div style="page-break-after: always;"></div>

## 2. Data Transformation

- ``Algorithm.transform`` : This module is responsible for transforming the dataset into the datastructures required for the computation. 
- Transformation 1 (``Algorithm.transform.transform``): 
    - Adds ``airline_capacity`` , ``depart_hour`` , ``arrival_hour`` keys to each flight on the dataset. ``airline_capcity`` is mapped from [Algorithm/capacity.json](Algorithm/capacity.json). The ``depart_hour``  and ``arrival_hour`` keys are added so that when the graph is constructed, these keys help derive the temporal information.
    - In this transformation, All flights which are not from required timeperiod are removed from the dataset. 
    - The timeperiod used here :
        - Start Time :  January 6, 2020 12:00 AM (Timezone = America/Los_Angeles)
        - Start Time :  January 7, 2020 12:00 AM (Timezone = America/Los_Angeles)

<div style="page-break-after: always;"></div>

- Transformation 2 (``Algorithm.transform.create_graph``): 
    - Converting the json array of flights created in Transformation 1 into a Graph. 
        - Core Datastructure ``Graph`` present in [Algorithm/graph.py](Algorithm/graph.py)
        - The ``Graph`` Object uses the following Matrix helps map the Directed Mulitgraph : ``self.graph[source_node_id][destination_node_id][edge_id]``. As this is a multi graph there are multiple edge_ids and so all edges are a part of an array. ``self.graph[source_node_id][destination_node_id][edge_id]`` retrives edge_weight of ``edge_id`` from ``source_node_id`` to ``destination_node_id``.
        - The ``Graph`` Object has methods to manupilate the graph. 
    
    - The Conversion Takes place in the following way : 
        - For each airport we create 24 temeporal time nodes representing each hour in the day. 
            - Eg. PHX ==> *PHX:0,PHX:1,PHX:2....*
        - We initialise the Graph with these ``airportCode:day_hour`` nodes. We additionally add 2 nodes representing Source(``LAX``) and Sink(``JFK``) in the graph. 
        - Node connection takes place in the following fashion:
            - ``ADD_STEP_1``: Direct edges from Source to all nodes ``source:hour_id`` with a weight of ``p_inifinity``. ``p_inifinty`` is positive inifinity. 
            - ``ADD_STEP_2``: Direct Edges for all nodes ``sink:hour_id`` to sink with weight of ``p_inifinty``.
            - ``ADD_STEP_3``: Sequentially direct an edge with weight of ``p_infinity`` for all Airports representing ``airport:hour_id`` except ``sink:hour_id``. 
                - Eg `SFO:3 ----p_inifinity-----> SFO:4 -----p_inifinity---->SFO:5 ....`
                - Esures that when a passenger arrives to an airport he can take flights from any time after he arrives. 
            - ``ADD_STEP_4``: Direct edges for all airports with flights in the following way : 
                - ``source_airport:depart_hour``---``aircraft_capacity``---->``dest_airport:arrival_hour``
                - This step helps caputure temporal time information

<div style="page-break-after: always;"></div>
        
## Maximum Flow Of Graph using Edmonds Karp's Algorithm

- ``Algorithm.flow.max_flow`` : This module runs the Edmonds Karp's Max flow calculation algorithm on the directed multigraph ``Graph`` from a ``source`` to a ``sink``. 
- Algorithm : 
    ```python
    def Edmonds_Karp_Max_Flow(Graph G):
        max_flow = 0
        path = BFS_Augmented_Path(G)
        while path is not None: 
            path_flow = 0
            for edge_weight in path_to_root(path):
                path_flow = min(edge_weight,path_flow)
            max_flow+=path_flow
            G = create_residual_graph_from_path(G,path,path_flow)
            path = BFS_Augmented_Path(G)
        return max_flow
    ```
- The  above is the psuedo code of the algorithm that can help find the maximum flow between source node and sink node. 
- As the problem statement dictates to find the capacity of simplified model of the National Airspace System, The Graph created in the transformation helps capture the nature of temporal time information and subsequent flight choice from same airport at a different time. The max flow between source and sink nodes on such a graph will help derive the capacity of the NAS System. 

- Time Complexity of Algorithm : E is Edges, V is Vertices.  
![equation](https://latex.codecogs.com/gif.latex?O(VE^2)&space;=&space;O(AirportCodes*24*E^2)&space;=&space;O(AirportCodes&space;*&space;E^2))
- This takes a complexity of E^2 because of BFS augmenting paths. 

## Code Output 

```
2019-12-02 14:39:02,399 - Data Transformation - INFO - Filtered Dataset With Flights : 623
2019-12-02 14:39:02,658 - Flight_Capacity_Data - INFO - Capacity of the Current Model 7414 
```