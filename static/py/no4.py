class DFA:
    def __init__ (self, states, initial_state, final_states, input_symbols, transitions):
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.input_symbols = input_symbols
        self.transitions = transitions
    def __str__(self):
        return f"States: {self.states}\nInitial state: {self.initial_state}\nFinal states: {self.final_states}\nInput symbols: {self.input_symbols}\nTransitions:\n{self.transitions}"

def get_next_state(current_state, symbol, transitions):
    return transitions.get(current_state, {}).get(symbol)

def are_states_equivalent(state1, state2, dfa1, dfa2, equivalent_table):
    return equivalent_table[state1][state2]

def equivalent(dfa1, dfa2):
    def initialize_equivalence_table(dfa1, dfa2):
        equivalent_table = {}
        for state1 in dfa1.states:
            equivalent_table[state1] = {}
            for state2 in dfa2.states:
                equivalent_table[state1][state2] = (state1 in dfa1.final_states) == (state2 in dfa2.final_states)
        return equivalent_table

    # Initialize equivalence table
    equivalent_table = initialize_equivalence_table(dfa1, dfa2)

    # Check if any initial pair is not equivalent
    if not equivalent_table[dfa1.initial_state][dfa2.initial_state]:
        return False

    # Check for unreachable states and mark them as non-equivalent
    for state1 in dfa1.states:
        for state2 in dfa2.states:
            for symbol in dfa1.input_symbols:
                next_state1 = get_next_state(state1, symbol, dfa1.transitions)
                next_state2 = get_next_state(state2, symbol, dfa2.transitions)
                if (next_state1 is None and next_state2 is not None) or (next_state1 is not None and next_state2 is None):
                    equivalent_table[state1][state2] = False

    # Iteratively refine equivalence table
    while True:
        changed = False
        for state1 in dfa1.states:
            for state2 in dfa2.states:
                if not equivalent_table[state1][state2]:
                    continue
                for symbol in dfa1.input_symbols:
                    next_state1 = get_next_state(state1, symbol, dfa1.transitions)
                    next_state2 = get_next_state(state2, symbol, dfa2.transitions)
                    if not are_states_equivalent(next_state1, next_state2, dfa1, dfa2, equivalent_table):
                        equivalent_table[state1][state2] = False
                        changed = True
                        break
            if changed:
                break
        if not changed:
            break

    # Check if all states are equivalent
    for state1 in dfa1.states:
        for state2 in dfa2.states:
            if are_states_equivalent(state1, state2, dfa1, dfa2, equivalent_table):
                for symbol in dfa1.input_symbols:
                    next_state1 = get_next_state(state1, symbol, dfa1.transitions)
                    next_state2 = get_next_state(state2, symbol, dfa2.transitions)
                    if not are_states_equivalent(next_state1, next_state2, dfa1, dfa2, equivalent_table):
                        return False
            else:
                if state1 in dfa1.final_states != state2 in dfa2.final_states:
                    return False
    return True

