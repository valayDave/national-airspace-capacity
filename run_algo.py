import Algorithm.load as DataLoader
import Algorithm.transform as DataTransformer
import Algorithm.logger as logger 
from Algorithm.flow import max_flow
import os
import json
import constants
import pandas

log = logger.create_logger('Flight_Capacity_Data')
module_dir = os.path.abspath(os.path.join(os.path.abspath(__file__),'..'))

dataset_DF = pandas.read_csv(os.path.join(module_dir,'Dataset/final_dataset.csv'))
flight_json_array = json.loads(dataset_DF.reset_index().to_json(orient='records'))
algo_dataset = DataTransformer.transform(flight_json_array)
# print(json.dumps(algo_dataset[0],indent=4))

SOURCE_AIRPORT = 'LAX'
SINK_AIRPORT = 'JFK'
Graph = DataTransformer.create_graph(SOURCE_AIRPORT,SINK_AIRPORT,constants.airports,algo_dataset)

log.info("Capacity of the Current Model %d ",max_flow(Graph,SOURCE_AIRPORT,SINK_AIRPORT))
