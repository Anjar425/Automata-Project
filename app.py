import os
from flask import Flask, render_template, request
from static.py.no1 import ENFA, NFA, nfa_to_dfa
from no2 import convertToNFA
from static.py.no3 import DFA as DFA_3
from static.py.no4 import DFA as DFA_4, are_equivalent
from static.py.no5 import DFA as DFA_5, NFA as NFA_5, ENFA as ENFA_5, test_regex
import static.py.visualize as visualize
import logging
from static.py.input_function import tranform_transition, get_states, get_start_and_final_states, get_alphabet, set_to_string, change_format, change_format_to_list, convert_data, convert_transitions, change_transition_5, change_epsilon_transitions_5


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/task1')
def task1():
    return render_template('task1.html')

@app.route('/dfa_convert', methods=['POST'])
def convertDFA():
    alphabets = change_format_to_list(get_alphabet(request.form.getlist('nfa')))
    
    result = False
    if 'e' in alphabets:
        transition = request.form.getlist('nfa')
        transition = change_format(transition)

        no_transition = len(transition)

        states = convert_data(request.form.getlist('nfa') + request.form.getlist('start_states') + request.form.getlist('finishing_states'))

        no_states = len(states)

        no_alphabets = len(alphabets)

        start_states = request.form.getlist('start_states')
        start_states = set_to_string(start_states)

        finishing_states = change_format_to_list(request.form.getlist('finishing_states'))

        no_finishing_states = len(finishing_states)

        enfa = ENFA(no_state=no_states, states=states, no_alphabet=no_alphabets,
            alphabets=alphabets, start=start_states, no_final=no_finishing_states,
            finals=finishing_states, no_transition=no_transition, transitions=transition)
        
        if finishing_states:
            visualize.visualize_enfa_1(enfa)
            visualize.visualize_dfa_from_enfa_1(enfa)
            result = 'enfa'

    else:
        transition = request.form.getlist('nfa')
        transition = convert_transitions(tranform_transition(transition))

        states = convert_data(request.form.getlist('nfa') + request.form.getlist('start_states') + request.form.getlist('finishing_states'))

        start_states = request.form.getlist('start_states')
        start_states = set_to_string(start_states)

        finishing_states = change_format_to_list(request.form.getlist('finishing_states'))

        nfa = NFA(states=states, alphabet=alphabets, transitions=transition, start_state=start_states, accept_states=finishing_states)

        if finishing_states : 
            visualize.visualize_nfa_1(states=states, alphabet=alphabets, transitions=transition, start_state=start_states, accept_states=finishing_states)
            dfa = nfa_to_dfa(nfa)
            visualize.visualize_dfa_from_nfa_1(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states)
            result = 'nfa'

    return render_template('task1.html', result=result)

@app.route('/task2')
def task2():
    return render_template('task2.html')

@app.route('/convert', methods=['POST'])
def convert():
    regex = request.form.get('regex')  # Ambil nilai 'regex' dari formulir

    nfa = convertToNFA(regex)

    visualize.visualize_nfa(nfa)
    
    enfa_generated = True
    return render_template('task2.html', nfa_image='static/img/no2/enfa.svg', enfa_generated=enfa_generated )

@app.route('/task3')
def task3():
    return render_template('task3.html')

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

    test_string = request.form.get('test_string')

    states = get_states(transition)

    valid = False

    if finishing_states:
        dfa = DFA_3(set(states), set(alphabets), transition, start_states, set(finishing_states))
        visualize.visualize_automaton(states, alphabets, transition, start_states, finishing_states, 'static/img/no3/dfa1')
        dfa.minimize()
        visualize.visualize_automaton(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states, 'static/img/no3/dfa2')
        dfa_generated = True
    else:
        dfa_generated = False

    if test_string:
        valid = dfa.simulate(test_string)

    return render_template('task3.html', dfa_generated=dfa_generated, valid=valid, string=test_string)

@app.route('/task4')
def task4():
    return render_template('task4.html')

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

    return render_template('task4.html', dfa_generated=dfa_generated)

@app.route('/task5')
def task5():
    return render_template('task5.html')

@app.route('/test', methods=['POST'])
def testString():

    type = request.form.get('type')
    logging.debug(f"type: {type}")
    
    result = False
    valid = False
    show = False
    test_string = request.form.get('test_string')
    if type == 'DFA':
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
        result = 'dfa'
        show = True

    elif type == 'NFA':
        alphabets = change_format_to_list(get_alphabet(request.form.getlist('dfa')))
        logging.debug(f"alphabets : {alphabets}")

        test_string = request.form.get('test_string')
        result = False

        if 'e' in alphabets:
            type = 'ε-NFA'
            alphabets = get_alphabet(request.form.getlist('dfa'))
            alphabets.discard('e')
            logging.debug(f"alphabets : {alphabets}")

            transition = tranform_transition(request.form.getlist('dfa'))
            logging.debug(f"transition : {transition}")

            epsilon_transition = change_epsilon_transitions_5(transition)
            logging.debug(f"epsilon_transition : {epsilon_transition}")

            start_states = request.form.getlist('start_states')
            start_states = set_to_string(start_states)
            logging.debug(f"start_states : {start_states}")

            states = get_states(transition)
            logging.debug(f"states : {states}")

            transition = change_transition_5(transition)
            logging.debug(f"transition : {transition}")

            finishing_states = request.form.getlist('finishing_states')
            finishing_states = get_start_and_final_states(finishing_states)
            logging.debug(f"finishing_states : {finishing_states}")

            enfa = ENFA_5(states=states, alphabet=alphabets, epsilon_transitions=epsilon_transition, transition=transition, start_states=start_states, final_states=finishing_states)
            logging.debug(f"enfa : {enfa}")

            valid = False
            if finishing_states:
                if test_string:
                    valid = enfa.accepts(test_string)
                visualize.visualize_enfa_5(enfa.states, enfa.alphabet, enfa.epsilon_transitions, enfa.transition_function, enfa.start_state, enfa.final_states)
                result = 'enfa'
                show = True

        else:
            alphabets = get_alphabet(request.form.getlist('dfa'))
            logging.debug(f"alphabets : {alphabets}")

            transition = tranform_transition(request.form.getlist('dfa'))
            logging.debug(f"transition : {transition}")

            start_states = request.form.getlist('start_states')
            start_states = set_to_string(start_states)
            logging.debug(f"start_states : {start_states}")

            states = get_states(transition)
            logging.debug(f"states : {states}")

            finishing_states = request.form.getlist('finishing_states')
            finishing_states = get_start_and_final_states(finishing_states)
            logging.debug(f"finishing_states : {finishing_states}")

            nfa = NFA_5(states=states, alphabets=alphabets, transition=transition, start_state=start_states, final_state=finishing_states)
            
            test_string = request.form.get('test_string')
            valid = False
            if test_string:
                valid = nfa.accepts(test_string)

            visualize.visualize_automaton(nfa.states, nfa.alphabet, nfa.transition_function, nfa.start_state, nfa.final_states, 'static/img/no5/nfa')
            result = 'nfa'
            show = True

    elif type == 'REGEX':
        regex = request.form.get('regex')
        regex = regex.replace('+', '|')

        valid = test_regex(regex, test_string)
        show = True

    return render_template('task5.html', show=show , result=result, valid=valid, string=test_string, type=type)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.environ.get('PORT', 5000))  # Gunakan PORT dari variabel lingkungan, atau default ke 5000
    app.run(debug=True, host='0.0.0.0', port=port)