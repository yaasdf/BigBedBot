class MsgContainer:
    def __init__(self, capacity):
        self.data = list()
        self.capacity = capacity

    def __getitem__(self, idx):
        return self.data[idx]

    def append(self, item):
        self.data.append(item)
        if len(self.data) > self.capacity:
            self.data.pop(0)

    def pop(self, idx=-1):
        return self.data.pop(idx)


m = MsgContainer(10)

m.append(1)
m.append(2)
m.append(3)

print(m.pop())
print(m.pop(0))