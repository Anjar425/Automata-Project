from flask import Flask, render_template, request, redirect, url_for
from static.py.no2 import convertToNFA
from static.py.no3 import DFA as DFA_3
from static.py.no4 import DFA as DFA_4, are_equivalent
from static.py.visualize import visualize_automaton
import logging
import graphviz
from static.py.input_function import tranform_transition, get_states, get_start_and_final_states, get_alphabet, set_to_string


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
    dfa = DFA_3

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
        dfa = DFA_3(set(states), set(alphabets), transition, start_states, set(finishing_states))
        visualize_automaton(states, alphabets, transition, start_states, finishing_states, 'static/img/no3/dfa1')
        dfa.minimize()
        visualize_automaton(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states, 'static/img/no3/dfa2')
        dfa_generated = True
    else:
        dfa_generated = False

    return render_template('number3.html', dfa_generated=dfa_generated)

@app.route('/number4')
def number4():
    return render_template('number4.html')

@app.route('/compare', methods=['POST'])
def compare():
    transition1 = tranform_transition(request.form.getlist('dfa1'))
    transition2 = tranform_transition(request.form.getlist('dfa2'))
    logging.debug(f"transition1 :  {transition1}")
    logging.debug(f"transition2 :  {transition2}")

    alphabets1 = get_alphabet(request.form.getlist('dfa1'))
    alphabets2 = get_alphabet(request.form.getlist('dfa2'))
    logging.debug(f"alphabets1 :  {alphabets1}")
    logging.debug(f"alphabets2 :  {alphabets2}")

    start_states1 = set_to_string(request.form.getlist('start_states1'))
    start_states2 = set_to_string(request.form.getlist('start_states2'))
    logging.debug(f"start_states1 :  {start_states1}")
    logging.debug(f"start_states2 :  {start_states2}")

    finishing_statesDFA1 = get_start_and_final_states(request.form.getlist('finishing_statesDFA1'))
    finishing_statesDFA2 = get_start_and_final_states(request.form.getlist('finishing_statesDFA2'))
    logging.debug(f"finishing_statesDFA1 :  {finishing_statesDFA1}")
    logging.debug(f"finishing_statesDFA2 :  {finishing_statesDFA2}")

    states1 = get_states(transition1)
    states2 = get_states(transition2)
    logging.debug(f"states1 :  {states1}")
    logging.debug(f"states2 :  {states2}")

    if finishing_statesDFA1 and finishing_statesDFA2:
        dfa1 = DFA_4(set(states1), set(alphabets1), transition1, start_states1, set(finishing_statesDFA1))
        dfa2 = DFA_4(set(states2), set(alphabets2), transition2, start_states2, set(finishing_statesDFA2))

        equivalent = are_equivalent(dfa1, dfa2)

        visualize_automaton(states1, alphabets1, transition1, start_states1, finishing_statesDFA1, 'static/img/no4/dfa1')
        visualize_automaton(states2, alphabets2, transition2, start_states2, finishing_statesDFA2, 'static/img/no4/dfa2')
        dfa_generated = True
    else:
        dfa_generated = False

    return render_template('number4.html', dfa_generated=dfa_generated)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Aktifkan logging debug
    app.run(debug=True)
