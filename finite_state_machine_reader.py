class FiniteAutomaton:
    def __init__(self, file):
        self.file = file
        results = self.read_file()
        self.transitions = results[4]
        self.final_states = set(results[3])
        self.start_state = results[2]
        self.current_state = self.start_state
        self.alphabet = set(results[1])
        self.states = set(results[0])

    def read_file(self):
        results = list()
        with open(self.file, "r") as inp:
            states = inp.readline()[1:-2].split(",")
            results.append(states)
            alphabet = inp.readline()[1:-2].split(",")
            results.append(alphabet)
            start_state = inp.readline()[:-1]
            if start_state not in states:
                print("Start state not in set of states")
            else:
                print("No problem with start state")
            results.append(start_state)
            final_states = inp.readline()[1:-2].split(",")
            problem = False
            for state in final_states:
                if state not in states:
                    print("Final state " + state + " not in set of states")
                    problem = True
            if not problem:
                print("No problem with final states")
            results.append(final_states)
            transitions = dict()
            for line in inp:
                tokens = line.split(";")
                transition_start = tokens[0]
                problem = False
                if transition_start not in states:
                    print("Transition start state " + transition_start + " not in set of states")
                    problem = True
                transition_input = tokens[1][1:-1].split(",")
                transition_destination = tokens[2][:-1]
                if transition_destination not in states:
                    print("Transition destination state " + transition_destination + " not in set of states")
                    problem = True
                for char in transition_input:
                    if (transition_start, char) not in transitions.keys():
                        transitions[(transition_start, char)] = list()
                    transitions[(transition_start, char)].append(transition_destination)
                if not problem:
                    print("No problem with transition states")
            results.append(transitions)

        return results

    def is_deterministic(self):
        for transition in self.transitions:
            if len(self.transitions[transition]) > 1:
                return False
        return True

    def reset_start(self):
        self.current_state = self.start_state

    def _check_sequence(self, sequence: str):
        if len(sequence) == 0:
            return self.current_state in self.final_states
        if (self.current_state, sequence[0]) not in self.transitions.keys():
            return False
        for destination in self.transitions[(self.current_state, sequence[0])]:
            state_temp = self.current_state
            self.current_state = destination
            if self._check_sequence(sequence[1:]):
                return True
            self.current_state = state_temp
        return False

    def check_sequence(self, sequence):
        self.reset_start()
        if not self.is_deterministic():
            return False
        for char in sequence:
            if char not in self.alphabet:
                return False
        return self._check_sequence(sequence)

    def menu(self):
        print("1 - set of states")
        print("2 - alphabet")
        print("3 - start state")
        print("4 - set of final states")
        print("5 - transition function")
        print("6 - deterministic ?")
        print("x - exit")
        while True:
            user_input = input("your option: ")
            if user_input == "1":
                print(self.states)
                continue
            if user_input == "2":
                print(self.alphabet)
                continue
            if user_input == "3":
                print(self.start_state)
                continue
            if user_input == "4":
                print(self.final_states)
                continue
            if user_input == "5":
                for tran in self.transitions:
                    print(tran, " -> ", self.transitions[tran])
                continue
            if user_input == "6":
                print(self.is_deterministic())
                continue
            if user_input == "x":
                break
