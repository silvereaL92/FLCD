TABLE_SIZE = 10


def custom_hash(value):
    ascii_sum = 0
    for char in value:
        ascii_sum += ord(char)
    return ascii_sum % TABLE_SIZE


class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.table = [[] for _ in range(table_size)]

    def display(self):
        for i in range(self.table_size):
            print(i, end=" ")

            for j in self.table[i]:
                print("-->", end=" ")
                print(j, end=" ")

            print()

    def insert(self, value):
        string_value = str(value)
        hash_key = custom_hash(string_value)
        self.table[hash_key].append(string_value)

    def is_entry(self, value):
        string_value = str(value)
        hash_key = custom_hash(string_value)
        for item in self.table[hash_key]:
            if item == string_value:
                return True
        return False

    def get_index(self, index):
        for entry in self.table[index]:
            yield entry


if __name__ == "__main__":
    hash_table = HashTable(TABLE_SIZE)
    hash_table.insert("istike")
    hash_table.insert("istike")

    print(hash_table.is_entry(23))
    hash_table.insert(23)
    print(hash_table.is_entry(23))

    print()
    hash_table.display()
    print()

    for entry in hash_table.get_index(9):
        print(entry)
