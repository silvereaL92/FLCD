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


if __name__ == "__main__":
    hash_table = HashTable(TABLE_SIZE, custom_hash)
    hash_table.insert("istike")
    hash_value, index = hash_table.insert("istike")

    print(hash_table.get_index(hash_value, index))

    print(hash_table.get_value(23))
    hash_table.insert(23)
    print(hash_table.get_value(23))

    print()
    hash_table.display()
    print()
