import re

TABLE_SIZE = 10


def custom_hash(value):
    ascii_sum = 0
    for char in value:
        ascii_sum += ord(char)
    return ascii_sum % TABLE_SIZE


class HashTable:
    def __init__(self, table_size, hash_function):
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

    def insert(self, value):
        string_value = str(value)
        hash_key = self.hash(string_value)
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


def is_identifier(token: str):
    identifier_regex = '[a-zA-Z][0-9a-zA-Z]*'
    return None is not re.fullmatch(identifier_regex, token)


def is_integer_constant(token: str):
    integer_regex = '^([+-]?[1-9]\d*|0)$'
    return None is not re.fullmatch(integer_regex, token)


if __name__ == "__main__":
    hash_table = HashTable(TABLE_SIZE, custom_hash)
    tokens = open("token.in", "r")
    operators = tokens.readline().split()
    separators = tokens.readline().split()
    reserved_words = tokens.readline().split()
    tokens.close()

    with open("sourcep1err.txt", "r", encoding="utf8") as source_code:
        pif = list()
        inside_string = False
        string = ""
        for line, raw_code in enumerate(source_code):
            tokenized_code = re.split("\[|]|{|}|\(|\)|,| |;|\n|\t", raw_code)

            for token in tokenized_code:
                if "" == token:
                    continue
                if '"' in token:
                    if token[0] == '"' and len(token) > 1:
                        if inside_string:
                            print("lexical error - <", token, "> line - ", line)
                        else:
                            inside_string = True
                            string += token[1:] + " "
                    elif token[-1] == '"':
                        if not inside_string:
                            print("lexical error - <<", token, ">> line - ", line)
                        else:
                            inside_string = False
                            string += token[:-1]
                            index = hash_table.insert(string)
                            string = ""
                            pif.append(("const", index))
                    else:
                        print("lexical error - <.", token, ".> line - ", line)
                elif inside_string:
                    string += token + " "
                else:
                    if token in reserved_words or token in operators:
                        pif.append((token, -1))
                    elif is_identifier(token):
                        index = hash_table.insert(token)
                        pif.append(("id", index))
                    elif is_integer_constant(token):
                        index = hash_table.insert(token)
                        pif.append(("id", index))
                    else:
                        print("lexical error - <:", token, ":> line - ", line)

        if inside_string:
            print("lexical error - unfinished string")
        for f in pif:
            print(f)
        hash_table.display()
