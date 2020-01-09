from . import logger as logger
from .graph import Graph


def BFS(graph_object:Graph, source_index, sink_index, parent):
    # Mark all the vertices as not visited
    visited = [False]*(graph_object.ROW)
    # Create a queue for BFS
    queue = []
    # Mark the source node as visited and enqueue it
    queue.append(source_index)
    visited[source_index] = True

    # $ Standard BFS Loop
    while queue:

        # Dequeue a vertex from queue and print it
        u = queue.pop(0)

        # Get all adjacent vertices of the dequeued vertex u
        # If a adjacent has not been visited, then mark it
        # visited and enqueue it
        for ind in range(graph_object.ROW):
            if visited[ind] == False and len(graph_object.graph[u][ind]) > 0 and sum(graph_object.graph[u][ind]) > 0:
                # print('graph_object.graph[u][ind]',u,ind)
                queue.append(ind)
                visited[ind] = True
                parent[ind] =[ u,graph_object.graph[u][ind].index(max(graph_object.graph[u][ind]))]
             
    # If we reached sink in BFS starting from source, then return
    # true, else false
    return True if visited[sink_index] else False

def max_flow(graph_object:Graph, source:str, sink:str):
    # $  This array is filled by BFS and to store path and the edge It considered on the Path.
    parent = [[-1,-1]]*(graph_object.ROW) # $ [(node_id,edge_id)]

    max_flow = 0  # $ There is no flow initially
    
    source_node_index = graph_object.get_node_id(source) 
    sink_node_index = graph_object.get_node_id(sink)
    # $ Augment the flow while there is path from source to sink
    while BFS(graph_object,source_node_index,sink_node_index ,parent):

        # $ Find minimum residual capacity of the edges along the
        # $ path filled by BFS. Or we can say find the maximum flow
        # $ through the path found.
        path_flow = float("Inf")
        curr_node_index = sink_node_index
        edge_index = None

        # $ Find Path flow in the Graph
        while(curr_node_index != graph_object.get_node_id(source)):
            parent_node_index,edge_id = parent[curr_node_index]
            path_flow = min(path_flow, graph_object.graph[parent_node_index][curr_node_index][edge_id])
            curr_node_index = parent_node_index

        # $ Add path flow to overall flow
        max_flow += path_flow
        
        # $ Also add 
        # $ update residual capacities of the edges and reverse edges along the path
        curr_node_index = sink_node_index
        while(curr_node_index != source_node_index):
            parent_node_index,edge_id = parent[curr_node_index]
            graph_object.graph[parent_node_index][curr_node_index][edge_id] -= path_flow
            # $ This seems corect. 
            graph_object.graph[curr_node_index][parent_node_index].append(path_flow)
            # print(graph_object.graph[parent_node_index][curr_node_index],graph_object.graph[curr_node_index][parent_node_index],curr_node_index,parent_node_index)
            curr_node_index = parent_node_index

    return max_flow