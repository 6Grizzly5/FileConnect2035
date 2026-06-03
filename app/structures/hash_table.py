class HashTable:

    def __init__(self, taille=100):

        self.taille = taille

        self.table = []

        for _ in range(taille):

            self.table.append([])

    # -------------------------
    # FONCTION DE HASH
    # -------------------------

    def hash_function(self, key):

        total = 0

        for char in str(key):

            total += ord(char)

        return total % self.taille

    # -------------------------
    # INSERTION
    # -------------------------

    def insert(self, key, value):

        index = self.hash_function(key)

        bucket = self.table[index]

        for item in bucket:

            if item[0] == key:

                item[1] = value

                return

        bucket.append([key, value])

    # -------------------------
    # RECHERCHE
    # -------------------------

    def get(self, key):

        index = self.hash_function(key)

        bucket = self.table[index]

        for item in bucket:

            if item[0] == key:

                return item[1]

        return None

    # -------------------------
    # SUPPRESSION
    # -------------------------

    def delete(self, key):

        index = self.hash_function(key)

        bucket = self.table[index]

        for i, item in enumerate(bucket):

            if item[0] == key:

                del bucket[i]

                return True

        return False