import re
from finite_state_machine_reader import FiniteAutomaton

TABLE_SIZE = 10


def custom_hash(value):
    ascii_sum = 0
    for char in value:
        ascii_sum += ord(char)
    return ascii_sum % TABLE_SIZE


class HashTable:
    def __init__(self, table_size, hash_function):
        self.identifier_automaton = FiniteAutomaton("identifier.in")
        self.int_const_automaton = FiniteAutomaton("int_const.in")
        self.table_size = table_size
        self.table = [[] for _ in range(table_size)]
        self.hash = hash_function

    def display(self):
        for i in range(self.table_size):
            print(i, end=" ")

            for j in self.table[i]:
                print("-->", end=" ")
                print(j, end=" ")

            print()

    def write(self):
        with open("symTable.out", "w") as out:
            out.write("Implemented on hashtable\n")
            for i in range(self.table_size):
                out.write(str(i) + " ")

                for j in self.table[i]:
                    out.write("--> ")
                    out.write(j + " ")

                out.write("\n")

    def insert(self, value):
        string_value = str(value)
        hash_key = self.hash(string_value)
        for index, item in enumerate(self.table[hash_key]):
            if item == string_value:
                return hash_key, index
        self.table[hash_key].append(string_value)
        return hash_key, len(self.table[hash_key]) - 1

    def get_value(self, value):
        string_value = str(value)
        hash_key = self.hash(string_value)
        for item in self.table[hash_key]:
            if item == string_value:
                return item

    def get_index(self, hash_value, index):
        try:
            return self.table[hash_value][index]
        except IndexError:
            return None

    def is_identifier(self, token: str):
        # identifier_regex = '[a-zA-Z][0-9a-zA-Z]*'
        # return None is not re.fullmatch(identifier_regex, token)
        return self.identifier_automaton.check_sequence(token)

    def is_integer_constant(self, token: str):
        # integer_regex = '^([+-]?[1-9]\d*|0)$'
        # return None is not re.fullmatch(integer_regex, token)
        return self.int_const_automaton.check_sequence(token)


def is_character_constant(token: str):
    character_regex = '^\'.\'$'
    return None is not re.fullmatch(character_regex, token)


if __name__ == "__main__":
    hash_table = HashTable(TABLE_SIZE, custom_hash)
    tokens = open("token.in", "r")
    operators = tokens.readline().split()
    separators = tokens.readline().split()
    reserved_words = tokens.readline().split()
    tokens.close()

    with open("source3.txt", "r", encoding="utf8") as source_code:
        pif = list()
        inside_string = False
        string = ""
        string_start = -1
        for line, raw_code in enumerate(source_code):
            tokenized_code = ""
            for char in raw_code:
                if char in "[]{}(),;":
                    tokenized_code += (" " + char + " ")
                else:
                    tokenized_code += char
            tokenized_code = tokenized_code.split()

            for token in tokenized_code:
                if "//" == token[:2]:
                    break

                if "" == token:
                    continue
                if '"' in token:
                    if token[0] == '"' and len(token) > 1:
                        if inside_string:
                            print("lexical error - <", token, "> line - ", line)
                        else:
                            inside_string = True
                            string_start = line
                            string += token + " "
                    elif token[-1] == '"':
                        if not inside_string:
                            print("lexical error - <<", token, ">> line - ", line)
                        else:
                            inside_string = False
                            string += token
                            index = hash_table.insert(string)
                            string = ""
                            pif.append(("constant", index))
                    else:
                        print("lexical error - <.", token, ".> line - ", line)
                elif inside_string:
                    string += token + " "
                else:
                    if token in reserved_words or token in operators or token in "[]{}(),;":
                        pif.append((token, -1))
                    elif hash_table.is_identifier(token):
                        index = hash_table.insert(token)
                        pif.append(("identifier", index))
                    elif hash_table.is_integer_constant(token) or is_character_constant(token):
                        index = hash_table.insert(token)
                        pif.append(("constant", index))
                    else:
                        print("lexical error - <:", token, ":> line - ", line)

        if inside_string:
            print("lexical error - unfinished string - starting at line", string_start)
        with open("pif.out", "w") as out:
            for f in pif:
                out.write(str(f[0]))
                out.write(" --> ")
                out.write(str(f[1]))
                out.write("\n")
        hash_table.write()
