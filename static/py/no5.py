class DFA:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transition_function = {}
        self.start_state = None
        self.final_states = set()

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

        # Input transitions
        print("Masukkan transisi DFA:")
        transition_dict = {}
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

            # Create key for checking transitions
            key = (state, symbol)

            # Check for determinism: each state-symbol pair should have exactly one next state
            if key in transition_dict:
                print(f"DFA tidak bisa menerima state dengan trasnisi yang sama, kesalahan state '{state}' dan transisi '{symbol}'")
                continue

            # Add to the transition dictionary
            transition_dict[key] = next_state

        self.transition_function = transition_dict

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


def main():
    dfa = DFA()

    # Input DFA definition
    dfa.get_input()

    # Check if DFA is valid
    if not dfa.is_valid():
        print("Input bukan bentuk DFA.")
        exit()

    # Input string
    input_string = input("Masukkan string input: ")

    # Check if input is accepted by DFA
    if dfa.accepts(input_string):
        print("String diterima oleh DFA.")
    else:
        print("String ditolak oleh DFA.")


if __name__ == "__main__":
    main()
