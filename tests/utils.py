"""Utility functions for testing
"""
def last_state(algo):
    """Get last state of stateset

    Args:
        algo (ARgorithm.utils.StateSet): The Stateset

    Returns:
        dict: The state metadata
    """
    state = algo.states.pop()
    return state.content
