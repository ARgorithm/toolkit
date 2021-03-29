"""The processor module consists of tools and pipeline to process and optimise
StateSet which simplifies rendering."""
import json
from ARgorithmToolkit.utils import StateSet
from ARgorithmToolkit.encoders import StateEncoder

def post_process(algo:StateSet):
    size = len(algo.states)
    if algo.autoplay is not None:
        for state in algo.states:
            state.autoplay = algo.autoplay
    else:
        for i in range(1,size):
            if algo.states[i].state_type == 'comment':
                algo.states[i-1].autoplay = True

    data = json.dumps(algo.states,cls=StateEncoder)
    return data


