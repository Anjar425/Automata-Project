import re

class DFA:
    def __init__(self, states, alphabet, transition, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition
        self.start_state = start_state
        self.final_states = final_states

    def is_valid(self):
        # Check if every state has a transition for each symbol in the alphabet
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transition_function:
                    print(f"Transisi tidak ditemukan untuk state '{state}' dan simbol '{symbol}'")
                    return False
        return True

    def accepts(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_state = self.transition_function.get((current_state, symbol))
            if current_state is None:
                return False
        return current_state in self.final_states


class NFA:
    def __init__(self, states, alphabets, transition, start_state, final_state):
        self.states = states
        self.alphabet = alphabets
        self.transition_function = transition
        self.start_state = start_state
        self.final_states = final_state

    def is_valid(self):
        # Validation logic
        if self.start_state not in self.states or not self.final_states.issubset(self.states):
            return False
        for (state, symbol), next_state in self.transition_function.items():
            if state not in self.states or next_state not in self.states or symbol not in self.alphabet:
                return False
        return True

    def accepts(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_state = self.transition_function.get((current_state, symbol))
            if current_state is None:
                return False
        return current_state in self.final_states


class ENFA:
    def __init__(self, states, alphabet, epsilon_transitions, transition, start_states, final_states):
        self.states = states
        self.alphabet = alphabet
        self.epsilon_transitions = epsilon_transitions
        self.transition_function = transition
        self.start_state = start_states
        self.final_states = final_states

    def get_input(self):
        # Input states
        states_input = input("Masukkan states (pisahkan dengan koma): ")
        self.states = set(states_input.split(','))

        # Input alphabet
        alphabet_input = input("Masukkan alphabet (pisahkan dengan koma): ")
        self.alphabet = set(alphabet_input.split(','))

        # Input start state
        self.start_state = input("Masukkan start state: ")

        # Input final states
        final_states_input = input("Masukkan final states (pisahkan dengan koma): ")
        self.final_states = set(final_states_input.split(','))

        # Input epsilon transitions
        print("Masukkan transisi epsilon (ε):")
        while True:
            epsilon_transition = input("Transisi (state next_state) (tekan enter untuk selesai): ")
            if not epsilon_transition:
                break
            epsilon_parts = epsilon_transition.split()
            if len(epsilon_parts) != 2:
                print("Transisi epsilon tidak lengkap.")
                continue
            state, next_state = map(str.strip, epsilon_parts)
            if state not in self.states or next_state not in self.states:
                print("Transisi epsilon tidak valid.")
                continue

            if state in self.epsilon_transitions:
                self.epsilon_transitions[state].append(next_state)
            else:
                self.epsilon_transitions[state] = [next_state]

        # Input transitions
        print("Masukkan transisi ENFA:")
        while True:
            transition = input("Transisi (state symbol next_state) (tekan enter untuk selesai): ")
            if not transition:
                break
            transition_parts = transition.split()
            if len(transition_parts) != 3:
                print("Transisi tidak lengkap.")
                continue
            state, symbol, next_state = map(str.strip, transition_parts)

            if state not in self.states or next_state not in self.states or symbol not in self.alphabet:
                print("Transisi tidak valid.")
                continue

            key = (state, symbol)

            if key in self.transition_function:
                self.transition_function[key].append(next_state)
            else:
                self.transition_function[key] = [next_state]
    def __str__(self):
        return f"NFA(states={self.states}, alphabet={self.alphabet}, epsilon_transitions={self.epsilon_transitions}, transition_function={self.transition_function}, start_state={self.start_state}, final_states={self.final_states})"


    def is_valid(self):
        # Validation logic
        if self.start_state not in self.states or not self.final_states.issubset(self.states):
            return False
        for (state, symbol), next_states in self.transition_function.items():
            if state not in self.states or not set(next_states).issubset(self.states) or symbol not in self.alphabet:
                return False
        return True

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            current_state = stack.pop()
            if current_state in self.epsilon_transitions:
                for next_state in self.epsilon_transitions[current_state]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def transition(self, states, symbol):
        result = set()
        for state in states:
            key = (state, symbol)
            if key in self.transition_function:
                result.update(self.transition_function[key])
        return self.epsilon_closure(result)

    def accepts(self, input_string):
        current_states = self.epsilon_closure({self.start_state})
        for symbol in input_string:
            current_states = self.transition(current_states, symbol)
        return any(state in self.final_states for state in current_states)


def test_regex(pattern, string):
    if re.match(pattern, string):
        if re.match(pattern, string).group(0) != '':
            return True
        else:
            return False
    else:
        return False