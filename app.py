from flask import Flask, render_template, request, redirect, url_for
from regex2nfafinal import convertToNFA
import logging
import graphviz
from static.py.transform_transition import tranform_transition, get_states, get_start_and_final_states, get_alphabet, set_to_string
from static.py.no3 import DFA, visualize_automaton

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    regex = request.form.get('regex')  # Ambil nilai 'regex' dari formulir

    logging.debug(f"Regular expression: {regex}")
    nfa = convertToNFA(regex)
    logging.debug(f"NFA: {nfa}")

    # Visualisasi NFA
    dot = graphviz.Digraph(comment='NFA Visualization')
    dot.graph_attr['rankdir'] = 'LR'

    # Buat node dan edge sesuai dengan NFA
    for state in nfa['states']:
        dot.node(state)
    for arc in nfa['transition_matrix']:
        start, label, end = arc
        dot.edge(start, end, label)

    # Simpan gambar ke file
    dot.render('static/nfa_graph', format='svg', cleanup=False)

    nfa_generated = True
    return render_template('index.html', nfa_image='static/nfa_graph.svg', nfa_generated=nfa_generated )

@app.route('/number3')
def number3():
    return render_template('number3.html')

@app.route('/minimize', methods=['POST'])
def minimizedfa():
    dfa = DFA

    transition = request.form.getlist('dfa')

    alphabets = get_alphabet(transition)

    transition = tranform_transition(transition)

    start_states = request.form.getlist('start_states')
    start_states = set_to_string(start_states)

    finishing_states = request.form.getlist('finishing_states')
    finishing_states = get_start_and_final_states(finishing_states)
    logging.debug(f"NFA: {finishing_states}")

    test_string = request.form.get('test_string')

    states = get_states(transition)

    
    if finishing_states:
        dfa = DFA(set(states), set(alphabets), transition, start_states, set(finishing_states))
        visualize_automaton(states, alphabets, transition, start_states, finishing_states, 'static/img/no3/dfa1')
        dfa.minimize()
        visualize_automaton(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states, 'static/img/no3/dfa2')
        dfa_generated = True
    else:
        dfa_generated = False

    return render_template('number3.html', dfa_generated=dfa_generated)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Aktifkan logging debug
    app.run(debug=True)
