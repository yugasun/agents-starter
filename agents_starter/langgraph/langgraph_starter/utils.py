from langgraph.graph.state import CompiledStateGraph

def print_message(message: str) -> None:
    """
    Print a message to the console.

    Args:
        message (str): The message to print.
    """
    print("--------------------------")
    print(f"{message}")
    print("--------------------------")


import os

def display_image(graph: CompiledStateGraph, filename: str = "graph.png"):
    """
    Save the graph image as a PNG file in the outputs directory.

    Args:
        graph (CompiledStateGraph): The compiled state graph.
        filename (str): The filename for the saved image.
    """
    try:
        img_bytes = graph.get_graph().draw_mermaid_png()
        os.makedirs("outputs", exist_ok=True)
        output_path = os.path.join("outputs", filename)
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        print(f"Graph image saved to {output_path}")
    except Exception as e:
        # This requires some extra dependencies and is optional
        print(f"Failed to save graph image: {e}")
        pass
