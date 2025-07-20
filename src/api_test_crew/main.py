#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from api_test_crew.crew import ApiTestCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'url': 'https://api.frankfurter.dev/v1/{date}?base={base}&symbols={symbols}',
        'method': 'GET',
        'params': {
            'date': {
                'required': True,
                'examples': ['latest', '1999-01-04', '2000-01-01..2000-12-31', '2024-01-01..']
            },
            'base': {
                'required': False,
                'examples': ['USD', 'GBP', 'JPY']
            },
            'symbols': {
                'required': False,
                'examples': ['USD,EUR', 'CHF', 'BGN']
            }
        }
    }
    
    try:
        ApiTestCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        ApiTestCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ApiTestCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        ApiTestCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
