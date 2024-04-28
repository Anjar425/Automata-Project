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
    dot.render(name, format='svg', view=False)
