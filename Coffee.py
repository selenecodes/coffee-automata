import time


dfa = {
    0: {  # Insert Money
        'G': { "nextState": 1, "description": "Insert money" }
    },
    1: {  # Make a choice
        'B': { "nextState": 2, "description": "Adding milk and sugar" },
        'M': { "nextState": 3, "description": "Adding milk" },
        'S': { "nextState": 4, "description": "Adding sugar" },
        'K': { "nextState": 5, "description": "Making coffee" },
    },
    2: {  # Add milk and sugar
        'K': {"nextState": 5, "description": "Making coffee" }
    },
    3: {  # Add milk
        'K': {"nextState": 5, "description": "Making coffee" }
    },
    4: {  # Add sugar
        'K': {"nextState": 5, "description": "Making coffee" }
    },
    5: {  # Add the coffee
        'R': {"nextState": 0, "description": "Thank you for your visit"}  # Reset the machine
    },
}

time_per_state = {
    5: 20, # Making coffee takes 20 seconds
    2: 10, # Adding milk and sugar 10 seconds (parallel)
    3: 10, # Adding milk takes 10 seconds
    4: 5 # Adding sugar takes 5 seconds
}

accepting_states = {
    2, # We have coffee
    3, # We have cofee with milk (and possibly sugar)
    4, # We have cofee with sugar (and possibly milk)
}


def accepts(transitions, initial, accepting, time_per_state, given_states):
    state = initial
    for s in given_states:
        current_state = transitions[state][s]
        current_state_description = current_state['description']
        next_state = current_state['nextState']

        if next_state in time_per_state:
            print(f"{current_state_description} please wait {time_per_state[next_state]} seconds")
            time.sleep(time_per_state[next_state])
        
        if next_state == 5:
            print(transitions[5]['R']['description'])

        state = next_state
    return state in accepting


accepts(dfa, 0, accepting_states, time_per_state, 'GBKR')
