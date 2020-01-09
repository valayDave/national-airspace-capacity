from typing import List
class Graph:
    # $ This Datastructure accounts for Multiple Edges to Same node. 
    def __init__(self,source_node:str,sink_node:str,nodes:List[str]):
        # $ Datastructure for edge from start_node to end_node would be : self.graph[start_node_id][end_node_id][edge_id]
        self.graph = []
        self.org_graph =  []
        self.ROW = 0
        self.node_list = nodes
        self.nodes = {} # {node_name: node_index_in_matrix}
        self.create_graph(source_node,sink_node,nodes)

    # $ Based on Node Data Initialize the Graph Matrix 
    def create_graph(self,source_node:str,sink_node:str,node_list:List[str]):
        total_num_nodes = len(node_list)+2
        self.nodes[source_node] = 0
        self.graph.append([[] for i in range(total_num_nodes)])

        for node_index in range(0,len(node_list)):
            self.nodes[node_list[node_index]] = node_index+1
            self.graph.append([[] for i in range(total_num_nodes)])
        
        self.nodes[sink_node] = total_num_nodes-1
        self.graph.append([[] for i in range(total_num_nodes)])
        self.ROW = len(self.graph)
    
    def get_matching_nodes(self,search_str:str):
        return [node for node in self.node_list if search_str in node]

    def get_node_id(self,node_name:str):
        if node_name in self.nodes:
            return self.nodes[node_name]
        return None

    def set_edges(self,start_node:str,end_nodes:List[str],weights:List[int]):
        if start_node not in self.nodes:
            return
        for i in range(len(end_nodes)):
            self.set_edge(start_node,end_nodes[i],weights[i])

    def set_edge(self,start_node:str,end_node:str,weight:int):
        if start_node not in self.nodes or end_node not in self.nodes:
            return 
        # print("Setting Edge  ",start_node,end_node,self.nodes[start_node],self.nodes[end_node])
        self.graph[self.nodes[start_node]][self.nodes[end_node]].append(weight)
        