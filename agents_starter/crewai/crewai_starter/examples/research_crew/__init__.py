import os
from .crew import ResearchCrew
from ...utils import print_message

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)


def run():
    """
    Run the research crew.
    """
    inputs = {"topic": "Artificial Intelligence in Healthcare"}

    # Create and run the crew
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print_message(result.raw)
