class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def add_state(self, state):
        self.states.add(state)

    def set_initial_state(self, state):
        self.initial_state = state

    def add_transition(self, from_state, symbol, to_state):
        if symbol not in self.alphabet:
            self.alphabet.add(symbol)
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state

    def set_final_state(self, state):
        self.final_states.add(state)

    def simulate(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if current_state not in self.transitions or symbol not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][symbol]
        return current_state in self.final_states
    
    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nStart State: {self.initial_state}\nAccept States: {self.final_states}"


def are_equivalent(dfa1, dfa2):
    if dfa1.alphabet != dfa2.alphabet or dfa1.states != dfa2.states:
        return False
    for state in dfa1.states:
        for symbol in dfa1.alphabet:
            if (state in dfa1.transitions and symbol in dfa1.transitions[state]) != (state in dfa2.transitions and symbol in dfa2.transitions[state]):
                return False
            if state in dfa1.transitions and state in dfa2.transitions and (dfa1.transitions[state][symbol] != dfa2.transitions[state][symbol]):
                return False
    return True
