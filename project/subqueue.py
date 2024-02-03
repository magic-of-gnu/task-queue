from dataclasses import dataclass


@dataclass
class SubQueue:
    name: str
    tasks: dict  # ordered by default; set is not ordered

    def __len__(self):
        return len(self.tasks)

    def popleft(self):
        for k in self.tasks.keys():
            v = self.tasks.pop(k)
            break
        return (k, v)

    def popright(self):
        return self.tasks.popitem()
