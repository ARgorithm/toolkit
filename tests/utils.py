"""Utility functions for testing."""
def last_state(algo):
    """Get last state of stateset.

    Args:
        algo (ARgorithm.utils.StateSet): The Stateset

    Returns:
        dict: The state metadata
    """
    state = algo.states.pop()
    return state


def check_states(statelist,algo):
    """Checks a series of states within the stateset.

    Args:
        statelist (list): The states we need to check in the StateSet
        algo (ARgorithm.utils.StateSet): The Stateset
    """
    k = len(statelist)
    statesgen = [x.state_type for x in algo.states[-k:]]
    for st1,st2 in zip(statesgen , statelist):
        assert st1 == st2
