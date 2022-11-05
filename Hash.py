
class HashMap:
    # Constructor for the HashMap class
    def __init__(self, pkgCounts=40):
        self.map = []
        for index in range(pkgCounts):
            self.map.append([])

    # Returns the hash value for the key
    def returnHash(self, key):
        bucket = int(key) % len(self.map)
        return bucket

    # Inserts the key and value into the bucket
    def insertVal(self, key, val):
        HashKey = self.returnHash(key)
        ValueKey = [key, val]

        if self.map[HashKey] is None:
            self.map[HashKey] = list([ValueKey])
            return True
        else:
            for i in self.map[HashKey]:
                if i[0] == key:
                    i[1] = ValueKey
                    return True
            self.map[HashKey].append(ValueKey)
            return True

    # Update new values in the bucket
    def updateVal(self, key, val):
        HashKey = self.returnHash(key)
        if self.map[HashKey] is not None:
            for i in self.map[HashKey]:
                if i[0] == key:
                    i[1] = val
                    return True
        else:
            print("Update failed: " + key)

    # Get the value from the hash table
    def getVal(self, key):
        HashKey = self.returnHash(key)
        if self.map[HashKey] is not None:
            for i in self.map[HashKey]:
                if i[0] == key:
                    return i[1]
        return None

    # Delete the value from the hash table
    def deleteVal(self, key):
        HashKey = self.returnHash(key)
        if self.map[HashKey] is None:
            return False
        for i in range(0, len(self.map[HashKey])):
            if self.map[HashKey][i][0] == key:
                self.map[HashKey].pop(i)
                return True
        return False
