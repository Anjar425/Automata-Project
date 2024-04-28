class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def is_accepting(self, state):
        return state in self.accept_states

    def transition(self, state, symbol):
        if (state, symbol) in self.transitions:
            return self.transitions[(state, symbol)]
        else:
            return None

    def minimize(self):
        from collections import defaultdict

        partition = [self.accept_states, self.states - self.accept_states]
        changed = True
        while changed:
            changed = False
            new_partition = []
            for part in partition:
                split_dict = defaultdict(list)
                for state in part:
                    transition_key = tuple(self.transition(state, symbol) for symbol in self.alphabet)
                    split_dict[transition_key].append(state)
                if len(split_dict) > 1:
                    changed = True
                    new_partition.extend(split_dict.values())
                else:
                    new_partition.append(part)
            partition = new_partition

        state_map = {}
        minimized_states = set()
        minimized_accept_states = set()
        minimized_transitions = {}

        for part in partition:
            representative = next(iter(part))
            minimized_states.add(representative)
            if representative in self.accept_states:
                minimized_accept_states.add(representative)
            for state in part:
                state_map[state] = representative

        for (state, symbol), next_state in self.transitions.items():
            new_state = state_map[state]
            new_next_state = state_map[next_state]
            minimized_transitions[(new_state, symbol)] = new_next_state

        self.states = minimized_states
        self.transitions = minimized_transitions
        self.accept_states = minimized_accept_states
        self.start_state = state_map[self.start_state]


    def simulate(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            current_state = self.transition(current_state, symbol)
            if current_state is None:
                return False
        
        return self.is_accepting(current_state)
    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nStart State: {self.start_state}\nAccept States: {self.accept_states}"
