import os
import sys


def run() -> None:
    config_file = os.path.join(os.path.dirname(__file__), "langgraph.json")
    # Add the parent directory to the system path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # run langgraph command
    os.system(f"langgraph dev --config {config_file}")
