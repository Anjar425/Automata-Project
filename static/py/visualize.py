import graphviz

def visualize_automaton(states, alphabet, transitions, start_state, accept_states, name):
    # Membuat digraph objek
    dot = graphviz.Digraph()
    
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    
    # Menambah node
    for state in states:
        if state in accept_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    
    # Menambah start node
    dot.node("start", label="start", shape="none", fontsize="24")
    dot.edge('start', start_state)
    
    # Tambah transisi
    for transition in transitions:
        from_state, symbol = transition
        to_state = transitions[transition]
        dot.edge(from_state, to_state, label=symbol)
    
    # render
    dot.render(name, format='svg', view=False, cleanup=True)


def visualize_nfa (data):
    # Membuat objek Graphviz dengan orientasi horizontal
    dot = graphviz.Digraph()
    dot.graph_attr['rankdir'] = 'LR'

    # Menambahkan node
    for state in data["states"]:
        if state in data["final_states"]:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    dot.node("start", label="start", shape="none", fontsize="24")
    dot.edge("start", data["start_states"][0])
    # Menambahkan edge
    for transition in data["transition_matrix"]:
        dot.edge(transition[0], transition[2], label=transition[1])

    dot.graph_attr['bgcolor'] = '#e5e7eb'
    # Menyimpan dan menampilkan graf
    dot.render('nfa', format='svg' , cleanup=True, view=False)


def visualize_enfa_1(nfa):
    nfa.graph = graphviz.Digraph()
    nfa.graph.graph_attr['rankdir'] = 'LR'

    # Adding states/nodes in NFA diagram
    for x in nfa.states:
        # If state is not a final state, then border shape is single circle
        # Else it is double circle
        if x not in nfa.finals:
            nfa.graph.attr('node', shape='circle')
            nfa.graph.node(x)
        else:
            nfa.graph.attr('node', shape='doublecircle')
            nfa.graph.node(x)

    # Adding start state arrow in NFA diagram
    nfa.graph.attr('node', shape='none')
    nfa.graph.node("start", label="start", shape="none", fontsize="24")
    nfa.graph.edge("start",nfa.start)

    # Adding edge between states in NFA from the transitions array
    for x in nfa.transitions:
        nfa.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])

    # Makes a pdf with name nfa.graph.pdf and views the pdf
    nfa.graph.graph_attr['bgcolor'] = '#e5e7eb'
    nfa.graph.render('static/img/no1/enfa', format="svg", view=False, cleanup=True)

def visualize_dfa_from_enfa_1(nfa):
    dfa = graphviz.Digraph()
    dfa.graph_attr['rankdir'] = 'LR'

    # Finding epsilon closure beforehand so to not recalculate each time
    epsilon_closure = dict()
    for x in nfa.states:
        epsilon_closure[x] = list(nfa.getEpsilonClosure(x))

    # First state of DFA will be epsilon closure of start state of NFA
    # This list will act as stack to maintain till when to evaluate the states
    dfa_stack = list()
    dfa_stack.append(epsilon_closure[nfa.start])

    # Check if start state is the final state in DFA
    if nfa.isFinalDFA(dfa_stack[0]):
        dfa.attr('node', shape='doublecircle')
    else:
        dfa.attr('node', shape='circle')
    dfa.node(nfa.getStateName(dfa_stack[0]))

    # Adding start state arrow to start state in DFA
    dfa.attr('node', shape='none')
    dfa.node("start", label="start", shape="none", fontsize="24")
    dfa.edge("start",nfa.getStateName(dfa_stack[0]))


    # List to store the states of DFA
    dfa_states = list()
    dfa_states.append(epsilon_closure[nfa.start])
    # nfa.alphabets = [symbol.replace('e', 'ε') for symbol in nfa.alphabets]
    # Loop will run till this stack is not empty
    while len(dfa_stack) > 0:
        # Getting top of the stack for current evaluation
        cur_state = dfa_stack.pop(0)

        # Traversing through all the alphabets for evaluating transitions in DFA
        for al in range(nfa.no_alphabet - 1):
            # Set to see if the epsilon closure of the set is empty or not
            from_closure = set()
            for x in cur_state:
                # Performing Union update and adding all the new states in set
                from_closure.update(set(nfa.transition_table[str(x) + str(al)]))

            # Check if epsilon closure of the new set is not empty
            if len(from_closure) > 0:
                # Set for the To state set in DFA
                to_state = set()
                for x in list(from_closure):
                    to_state.update(set(epsilon_closure[nfa.states[x]]))

                # Check if the to state already exists in DFA and if not then add it
                if list(to_state) not in dfa_states:
                    dfa_stack.append(list(to_state))
                    dfa_states.append(list(to_state))

                    # Check if this set contains final state of NFA
                    # to get if this set will be final state in DFA
                    if nfa.isFinalDFA(list(to_state)):
                        dfa.attr('node', shape='doublecircle')
                    else:
                        dfa.attr('node', shape='circle')
                    dfa.node(nfa.getStateName(list(to_state)))

                # Adding edge between from state and to state
                dfa.edge(nfa.getStateName(cur_state), nfa.getStateName(list(to_state)), label=nfa.alphabets[al])

            # Else case for empty epsilon closure
            # This is a dead state(ϕ) in DFA
            else:
                # Check if any dead state was present before this
                # if not then make a new dead state ϕ
                if -1 not in dfa_states:
                    dfa.attr('node', shape='circle')
                    dfa.node('ϕ')

                    # For new dead state, add all transitions to itself,
                    # so that machine cannot leave the dead state
                    for alpha in range(nfa.no_alphabet - 1):
                        dfa.edge('ϕ', 'ϕ', nfa.alphabets[alpha])

                    # Adding -1 to list to mark that dead state is present
                    dfa_states.append(-1)

                # Adding transition to dead state
                dfa.edge(nfa.getStateName(cur_state), 'ϕ', label=nfa.alphabets[al])

    # Makes a pdf with name dfa.pdf and views the pdf
    dfa.graph_attr['bgcolor'] = '#e5e7eb'
    dfa.render('static/img/no1/dfa', format="svg", cleanup=True, view=False)


def visualize_dfa_from_nfa_1(states, alphabet, transitions, start_state, accept_states):
    # Create a new graph
    graph = graphviz.Digraph()
    graph.graph_attr['rankdir'] = 'LR'

    # Add states to the graph
    for state in states:
        state_label = ','.join(state) if state else 'ϕ'
        if state in accept_states:
            graph.node(state_label, shape='doublecircle')
        else:
            graph.node(state_label, shape='circle')

    # Add transitions to the graph
    for transition, next_state in transitions.items():
        current_state, symbol = transition
        current_state_label = ','.join(
            current_state) if current_state else 'ϕ'
        next_state_label = ','.join(next_state) if next_state else 'ϕ'
        graph.edge(current_state_label, next_state_label, label=symbol)

    # Set start state
    start_state_label = ','.join(start_state) if start_state else 'ϕ'
    graph.attr('node', shape='plaintext')
    graph.node("start", label="start", shape="none", fontsize="24")
    graph.edge('start', start_state_label)

    # Render and display the graph
    graph.graph_attr['bgcolor'] = '#e5e7eb'
    graph.render('static/img/no1/dfa', format="svg", cleanup=True, view=False)

def visualize_nfa_1(states, alphabet, transitions, start_state, accept_states):
    # Inisialisasi objek graph
    dot = graphviz.Digraph(comment='NFA')
    dot.graph_attr['rankdir'] = 'LR'

    # Tambahkan state
    for state in states:
        dot.node(state, shape='circle')
    
    # Tambahkan state awal
    dot.node("start", label="start", shape="none", fontsize="24")
    dot.edge("start",start_state)

    # Tambahkan transisi
    for transition, next_states in transitions.items():
        current_state, symbol = transition
        for next_state in next_states:
            dot.edge(current_state, next_state, label=symbol)

    # Tambahkan state akhir
    for accept_state in accept_states:
        dot.node(accept_state, shape='doublecircle')

    # Render dan tampilkan diagram
    dot.graph_attr['bgcolor'] = '#e5e7eb'
    dot.render('static/img/no1/nfa', format="svg", cleanup=True, view=False)


def visualize_enfa_5(states, alphabet, epsilon_transitions, transition_function, start_state, final_states):
    # Create graph
    dot = graphviz.Digraph()
    dot.graph_attr['rankdir'] = 'LR'
    
    # Add nodes
    for state in states:
        if state == start_state:
            dot.node(state, shape='circle', label=start_state)
            dot.node("start", label="start", shape="none", fontsize="24")
            dot.edge('start', state)
        elif state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')
    
    # Add transitions
    for state in states:
        for symbol in alphabet:
            if (state, symbol) in transition_function:
                for next_state in transition_function[(state, symbol)]:
                    dot.edge(state, next_state, label=symbol)
        if state in epsilon_transitions:
            for next_state in epsilon_transitions[state]:
                dot.edge(state, next_state, label='ε')
    
    # Render and save the graph
    dot.graph_attr['bgcolor'] = '#e5e7eb'
    dot.render('static/img/no5/enfa', format="svg", cleanup=True, view=False)