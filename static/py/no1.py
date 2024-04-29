from graphviz import Digraph
import graphviz


class ENFA:
    def __init__(self, no_state, states, no_alphabet, alphabets, start,
                 no_final, finals, no_transition, transitions):
        self.no_state = no_state
        self.states = states
        self.no_alphabet = no_alphabet
        self.alphabets = alphabets

        # Adding epsilon alphabet to the list
        # and incrementing the alphabet count
        self.start = start
        self.no_final = no_final
        self.finals = finals
        self.no_transition = no_transition
        self.transitions = transitions
        self.graph = Digraph()

        # Dictionaries to get index of states or alphabets
        self.states_dict = dict()
        for i in range(self.no_state):
            self.states_dict[self.states[i]] = i
        self.alphabets_dict = dict()
        for i in range(self.no_alphabet):
            self.alphabets_dict[self.alphabets[i]] = i

        # transition table is of the form
        # [From State + Alphabet pair] -> [Set of To States]
        self.transition_table = dict()
        for i in range(self.no_state):
            for j in range(self.no_alphabet):
                self.transition_table[str(i)+str(j)] = []
        for i in range(self.no_transition):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])
                                  + str(self.alphabets_dict[
                                      self.transitions[i][1]])].append(
                self.states_dict[self.transitions[i][2]])
    def __str__(self):
        return f"Number of States: {self.no_state}\nStates: {self.states}\n" \
               f"Number of Alphabets: {self.no_alphabet}\nAlphabets: {self.alphabets}\n" \
               f"Start State: {self.start}\nNumber of Final States: {self.no_final}\n" \
               f"Final States: {self.finals}\nNumber of Transitions: {self.no_transition}\n" \
               f"Transitions: {self.transitions}\nTransition Table: {self.transition_table}"        

    def getEpsilonClosure(self, state):

        # Method to get Epsilon Closure of a state of NFA
        # Make a dictionary to track if the state has been visited before
        # And a array that will act as a stack to get the state to visit next
        closure = dict()
        closure[self.states_dict[state]] = 0
        closure_stack = [self.states_dict[state]]

        # While stack is not empty the loop will run
        while (len(closure_stack) > 0):

            # Get the top of stack that will be evaluated now
            cur = closure_stack.pop(0)

            # For the epsilon transition of that state,
            # if not present in closure array then add to dict and push to stack
            for x in self.transition_table[
                    str(cur)+str(self.alphabets_dict['e'])]:
                if x not in closure.keys():
                    closure[x] = 0
                    closure_stack.append(x)
            closure[cur] = 1
        return closure.keys()

    def getStateName(self, state_list):

        # Get name from set of states to display in the final DFA diagram
        name = ''
        for x in state_list:
            name += self.states[x]
        return name

    def isFinalDFA(self, state_list):

        # Method to check if the set of state is final state in DFA
        # by checking if any of the set is a final state in NFA
        for x in state_list:
            for y in self.finals:
                if (x == self.states_dict[y]):
                    return True
        return False

class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if ('', state) in self.transitions:
                for next_state in self.transitions[('', state)]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return tuple(sorted(closure))

    def move(self, states, symbol):
        result = set()
        for state in states:
            if (symbol, state) in self.transitions:
                result.update(self.transitions[(symbol, state)])
        return self.epsilon_closure(result)

    def simulate(self, input_string):
        current_states = self.epsilon_closure({self.start_state})
        for symbol in input_string:
            current_states = self.move(current_states, symbol)
        return bool(current_states.intersection(self.accept_states))
    def __str__(self):
        return f"NFA(states={self.states}, alphabet={self.alphabet}, transitions={self.transitions}, start_state={self.start_state}, accept_states={self.accept_states})"


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def simulate(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            current_state = self.transitions.get((current_state, symbol))
            if current_state is None:
                return False
        return current_state in self.accept_states

    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nStart State: {self.start_state}\nAccept States: {self.accept_states}"


def powerset(s):
    from itertools import chain, combinations
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def nfa_to_dfa(nfa):
    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = nfa.epsilon_closure({nfa.start_state})
    dfa_accept_states = set()
    alphabet = nfa.alphabet

    queue = [dfa_start_state]
    visited = set()

    while queue:
        current_state = queue.pop(0)
        if current_state in visited:
            continue
        visited.add(current_state)
        dfa_states.add(current_state)

        if any(state in nfa.accept_states for state in current_state):
            dfa_accept_states.add(current_state)

        for symbol in alphabet:
            next_state = set()
            for nfa_state in current_state:
                if (symbol, nfa_state) in nfa.transitions:
                    next_state.update(nfa.transitions[(symbol, nfa_state)])
            next_state_closure = nfa.epsilon_closure(next_state)
            dfa_transitions[(current_state, symbol)] = next_state_closure
            if next_state_closure not in visited:
                queue.append(next_state_closure)

    return DFA(dfa_states, alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)





# # Membuat NFA dari input pengguna
# states = input("Masukkan states NFA (pisahkan dengan spasi): ").split()
# alphabet = input("Masukkan alphabet NFA (pisahkan dengan spasi): ").split()
# transitions = {}
# while True:
#     transition_input = input(
#         "Masukkan transisi NFA (dari, simbol, ke) atau ketik 'selesai' untuk mengakhiri: ").split()
#     if transition_input[0].lower() == 'selesai':
#         break
#     from_state, symbol, to_state = transition_input
#     transitions.setdefault((symbol, from_state), set()).add(to_state)
# start_state = input("Masukkan start state NFA: ")
# accept_states = input(
#     "Masukkan accept states NFA (pisahkan dengan spasi): ").split()

# nfa = NFA(states, alphabet, transitions, start_state, accept_states)
# print(nfa)

# # Mengonversi NFA menjadi DFA
# dfa = nfa_to_dfa(nfa)

# # Visualisasi DFA
# visualize_dfa(dfa.states, dfa.alphabet, dfa.transitions,
#               dfa.start_state, dfa.accept_states)