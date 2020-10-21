import functools
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


# can utilize regex
def is_identifier(token: str):
    if not token[0].isalpha():
        return False
    for character in token:
        if not character.isalnum():
            return False
    return True


def is_integer_constant(token: str):
    if token[0] == '0' and len(token) > 1:
        return False
    try:
        int(token)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    hash_table = HashTable(TABLE_SIZE, custom_hash)
    tokens = open("token.in", "r")
    operators = tokens.readline().split()
    separators = tokens.readline().split()
    delimiters = functools.reduce(lambda a, b: a + b if b != 'space' else a + ' ', separators)
    reserved_words = tokens.readline().split()
    tokens.close()

    with open("source2.txt", "r", encoding="utf8") as source_code:
        pif = list()
        inside_string = False
        string = ""
        for line, raw_code in enumerate(source_code):
            # need to change this to split using the delimiters directly
            mod_code = ""
            for c in raw_code:
                if c in separators:
                    mod_code += " "
                else:
                    mod_code += c
            tokenized_code = mod_code.split()
            print(tokenized_code)

            for token in tokenized_code:
                if inside_string:
                    string += token

                if token[0] == "\"":
                    if inside_string:
                        print("bblexical error - ", token, " line - ", line)
                    else:
                        inside_string = True
                        string += token

                if token[-1] == "\"":
                    if not inside_string:
                        print("aalexical error - ", token, " line - ", line)
                    else:
                        inside_string = False
                        string += token
                        index = hash_table.insert(string)
                        string = ""
                        pif.append(("const", index))
                if not inside_string:
                    if token in reserved_words or token in operators:
                        pif.append((token, -1))
                    elif is_identifier(token):
                        index = hash_table.insert(token)
                        pif.append(("id", index))
                    elif is_integer_constant(token):
                        index = hash_table.insert(token)
                        pif.append(("id", index))
                    else:
                        print("cclexical error - ", token, " line - ", line)

        if inside_string:
            print("ddlexical error - unfinished string")
        for f in pif:
            print(f)
        hash_table.display()
