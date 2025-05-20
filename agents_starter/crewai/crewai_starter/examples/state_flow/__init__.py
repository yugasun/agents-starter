import os
from .research_flow import ResearchFlow
from ...utils import print_message

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)


def run():
    # Create and run the crew
    result = ResearchFlow().kickoff()

    # Print the result
    print_message(result)
