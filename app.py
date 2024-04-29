from flask import Flask, render_template, request, redirect, url_for
from static.py.no1 import ENFA, NFA, nfa_to_dfa
from static.py.no2 import convertToNFA
from static.py.no3 import DFA as DFA_3
from static.py.no4 import DFA as DFA_4, are_equivalent
from static.py.no5 import DFA as DFA_5
import static.py.visualize as visualize
import logging
from static.py.input_function import tranform_transition, get_states, get_start_and_final_states, get_alphabet, set_to_string, change_format, change_format_to_list, convert_data, convert_transitions


app = Flask(__name__)

@app.route('/number1')
def number1():
    return render_template('number1.html')

@app.route('/dfa_convert', methods=['POST'])
def convertDFA():

    alphabets = change_format_to_list(get_alphabet(request.form.getlist('dfa')))
    logging.debug(f"alphabets : {alphabets}")
    
    result = False
    if 'e' in alphabets:
        transition = request.form.getlist('dfa')
        transition = change_format(transition)
        logging.debug(f"transition : {transition}")

        no_transition = len(transition)
        logging.debug(f"no_transition : {no_transition}")

        states = convert_data(request.form.getlist('dfa') + request.form.getlist('start_states') + request.form.getlist('finishing_states'))
        logging.debug(f"states : {states}")

        no_states = len(states)
        logging.debug(f"no_states : {no_states}")

        no_alphabets = len(alphabets)
        logging.debug(f"no_alphabets : {no_alphabets}")

        start_states = request.form.getlist('start_states')
        start_states = set_to_string(start_states)
        logging.debug(f"start_states : {start_states}")

        finishing_states = change_format_to_list(request.form.getlist('finishing_states'))
        logging.debug(f"finishing_states: {finishing_states}")

        no_finishing_states = len(finishing_states)
        logging.debug(f"no_finishing_states : {no_finishing_states}")
        # test_string = request.form.get('test_string')

        enfa = ENFA(no_state=no_states, states=states, no_alphabet=no_alphabets,
            alphabets=alphabets, start=start_states, no_final=no_finishing_states,
            finals=finishing_states, no_transition=no_transition, transitions=transition)
        
        logging.debug(f"enfa : {enfa}")

        
        if finishing_states:
            visualize.visualize_nfa_no1(enfa)
            visualize.create_dfa_from_nfa(enfa)
            result = 'enfa'

    else:
        transition = request.form.getlist('dfa')
        transition = convert_transitions(tranform_transition(transition))
        logging.debug(f"transition : {transition}")

        states = convert_data(request.form.getlist('dfa') + request.form.getlist('start_states') + request.form.getlist('finishing_states'))
        logging.debug(f"states : {states}")

        start_states = request.form.getlist('start_states')
        start_states = set_to_string(start_states)
        logging.debug(f"start_states : {start_states}")

        finishing_states = change_format_to_list(request.form.getlist('finishing_states'))
        logging.debug(f"finishing_states: {finishing_states}")

        nfa = NFA(states=states, alphabet=alphabets, transitions=transition, start_state=start_states, accept_states=finishing_states)
        logging.debug(f"nfa: {nfa}")

        if finishing_states : 
            visualize.visualize_nfa_1(states=states, alphabet=alphabets, transitions=transition, start_state=start_states, accept_states=finishing_states)
            dfa = nfa_to_dfa(nfa)
            visualize.visualize_dfa_from_nfa_1(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states)
            result = 'nfa'

        

    return render_template('number1.html', result=result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    regex = request.form.get('regex')  # Ambil nilai 'regex' dari formulir

    logging.debug(f"Regular expression: {regex}")
    nfa = convertToNFA(regex)
    logging.debug(f"NFA: {nfa}")

    visualize.visualize_nfa(nfa)
    
    nfa_generated = True
    return render_template('index.html', nfa_image='static/img/no2/nfa.svg', nfa_generated=nfa_generated )

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
        visualize.visualize_automaton(states, alphabets, transition, start_states, finishing_states, 'static/img/no3/dfa1')
        dfa.minimize()
        visualize.visualize_automaton(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states, 'static/img/no3/dfa2')
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

        visualize.visualize_automaton(states1, alphabets1, transition1, start_states1, finishing_statesDFA1, 'static/img/no4/dfa1')
        visualize.visualize_automaton(states2, alphabets2, transition2, start_states2, finishing_statesDFA2, 'static/img/no4/dfa2')
        dfa_generated = True
    else:
        dfa_generated = False

    return render_template('number4.html', dfa_generated=dfa_generated)

@app.route('/number5')
def number5():
    return render_template('number5.html')

@app.route('/test', methods=['POST'])
def testString():

    type = request.form.get('type')
    logging.debug(f"type: {type}")
    
    if type == 'dfa':
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

        dfa = DFA_5(states=states, alphabet=alphabets, transition=transition, start_state=start_states, final_states=finishing_states)
        valid = dfa.accepts(test_string)
        logging.debug(f"dfa : {valid}")

        visualize.visualize_automaton(dfa.states, dfa.alphabet, dfa.transition_function, dfa.start_state, dfa.final_states, 'static/img/no5/dfa')

    elif type == 'nfa':
        transition


    return render_template('number5.html')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Aktifkan logging debug
    app.run(debug=True)
