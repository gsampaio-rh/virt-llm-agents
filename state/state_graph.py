from langgraph.graph import StateGraph, START, END


def create_graph(stateGraph, nodes: dict[str, callable]) -> StateGraph:
    """
    Create the state graph by defining nodes and edges from a dictionary of node definitions.

    Args:
    - nodes (dict[str, callable]): A dictionary where the key is the node name and
                                   the value is the function associated with the node.

    Returns:
    - StateGraph: The compiled state graph ready for execution.
    """
    graph = StateGraph(stateGraph)

    # Add nodes dynamically from the provided dictionary
    for node_name, node_function in nodes.items():
        graph.add_node(node_name, node_function)

    # Define the flow of the graph
    node_names = list(nodes.keys())
    graph.add_edge(START, node_names[0])  # First node in the list

    # Connect nodes in sequence
    for i in range(len(node_names) - 1):
        graph.add_edge(node_names[i], node_names[i + 1])

    # End the flow at the last node
    graph.add_edge(node_names[-1], END)

    return graph


def run_workflow(
    graph: StateGraph,
    input_query: str,
    config: dict,
    memory,
    iterations=10,
    verbose=True,
):
    """
    Execute the workflow by streaming through the graph.

    Args:
    - graph (StateGraph): The compiled state graph
    - input_query (str): The user input query
    - config (dict): The configuration for the workflow
    - memory (SqliteSaver): Checkpointer for memory persistence
    - iterations (int): Maximum recursion limit
    - verbose (bool): If True, print event details during execution
    """
    dict_inputs = {"input": input_query}
    limit = {"recursion_limit": iterations}

    workflow = graph.compile(checkpointer=memory)

    # Stream the events through the workflow
    for event in workflow.stream(dict_inputs, config):
        if verbose:
            print("\nEvent:", event)
        else:
            print("\n")
