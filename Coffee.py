import time
import random

""" All states in our state machine """
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

""" Time duration per state """
timePerState = {
    5: .20, # Making coffee takes 20 seconds
    2: .10, # Adding milk and sugar 10 seconds (parallel)
    3: .10, # Adding milk takes 10 seconds
    4: .5 # Adding sugar takes 5 seconds
}

""" Function that returns an order as string based on states """
def orderToMessage(states):
    s = 'coffee'
    if ('B' in states):
        return s + ' with milk and sugar'
    if ('M' in states):
        return s + ' with milk'
    if ('S' in states):
        return s + ' with sugar'

    return s


""" Constants """
initialState = 0
possibleOrders = ['GBK', 'GMK', 'GSK', 'GK']

""" Configuration """
# Two people are initially ordering coffee with milk and sugar
orders = ['GB', 'GBK']

# Chance everytime the machine is doing something that a person enters the queue
chanceOfNewPerson = .1

""" State machine """
state = initialState
for order in orders:
    # !NOTE: Convert our string to a list to fix immutability issues
    order = list(order)
    
    print('Creating order:')
    for s in order:
        if s in dfa[state]:
            currentState = dfa[state][s]
        else:
            print(f"{s} was not found as a nextstate of state {state} \n")
            break

        currentStateDescription = currentState['description']
        nextState = currentState['nextState']

        # If the nextState has a time duration handle it here
        if nextState in timePerState:
            print(f"{currentStateDescription} please wait {timePerState[nextState]} seconds")
            
            # Add a person randomly
            if (random.random() <= chanceOfNewPerson):
                choice = random.choice(possibleOrders)
                print(f"A person was added to the queue and bought {orderToMessage(choice)}")
                orders.append(choice)

            # Wait for the action to complete
            time.sleep(timePerState[nextState])
        
        # Check if the next state is the last state and if it is say "Thank you" and reset the state.
        if nextState == 5:
            print(f"{dfa[5]['R']['description']} \n")

            # The machine automatically resets and the user doesn't need to press a button
            order.append('R')

        state = nextState
