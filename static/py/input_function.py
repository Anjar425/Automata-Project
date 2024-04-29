def tranform_transition(transition):
    result = {}
    for i in range(0, len(transition), 3):
        start_state = transition[i].lower()
        alphabet = transition[i+1]
        next_state = transition[i+2].lower()
        key = (start_state,alphabet)
        result[key] = next_state
    return result

def get_states(transisi):
    states = set()
    for key in transisi.keys():
        states.add(key[0])
    return states

def get_start_and_final_states(states):
    if not states:
        return ''
    states_set = {state.lower() for state in states}
    return states_set

def get_alphabet(transition):
    alphabet = set(item for item in transition if item.isdigit() or item == 'e')
    return alphabet

def set_to_string(s):
    # Mengambil item dari set
    item = s.pop()
    # Mengonversi item menjadi string dan mengubahnya menjadi lowercase
    s_string = str(item).lower()
    return s_string

def change_format(input_list):
    output_list = []
    temp = []
    for item in input_list:
        if item == 'e':
            temp.append('e')
        else:
            temp.append(item.lower())
        if len(temp) == 3:
            output_list.append(temp)
            temp = []
    return output_list

def change_format_to_list(input_set):
    return [item.lower() for item in input_set]

def convert_data(data):
    result = []
    seen = set()
    for item in data:
        if item.startswith('Q') and item.lower() not in seen:
            result.append(item.lower())
            seen.add(item.lower())
    return result




