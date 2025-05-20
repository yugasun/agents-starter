import os
from .creator_flow import GuideCreatorFlow
from ...utils import print_message

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)


def run():
    """
    Run the research crew.
    """
    flow = GuideCreatorFlow()
    result = flow.kickoff()

    # Print the result
    print_message(result)

    flow.plot()
