from dataclasses import dataclass

from .doubly_linked_list import DoublyLinkedList, Node
from .resources import Resources
from .subqueue import SubQueue
from .task import Task

PriorityNameToInt = {
    "QHIGHEST": 1,
    "QHIGH": 2,
    "QMIDDLE": 3,
    "QLOW": 4,
    "QLOWEST": 5,
}

PriorityIntToName = {val: key for key, val in PriorityNameToInt.items()}


@dataclass
class Queue:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

        self.tasks = DoublyLinkedList()

        self.QHIGHEST = SubQueue(
            name="HIGHEST",
            tasks=dict(),
        )
        self.QHIGH = SubQueue(
            name="HIGH",
            tasks=dict(),
        )
        self.QMIDDLE = SubQueue(
            name="MIDDLE",
            tasks=dict(),
        )
        self.QLOW = SubQueue(
            name="LOW",
            tasks=dict(),
        )
        self.QLOWEST = SubQueue(
            name="LOWEST",
            tasks=dict(),
        )

    def __len__(self):
        subqs_len = (
            len(self.QHIGHEST.tasks)
            + len(self.QHIGH.tasks)
            + len(self.QMIDDLE.tasks)
            + len(self.QLOW.tasks)
            + len(self.QLOWEST.tasks)
        )

        tasks_len = len(self.tasks)
        assert subqs_len == tasks_len, ValueError("subqueues and tasks lengths differ")
        return tasks_len

    def subq_len(self, subq_int: int):
        return len(getattr(self, PriorityIntToName[subq_int]))

    def insert_task_id_to_subqueue(self, id: int, priority: int) -> None:
        subq = getattr(self, PriorityIntToName[priority])
        subq.tasks[id] = True

    def pop_task_id_from_subqueue(self, id: int, priority: int) -> None:
        subq = getattr(self, PriorityIntToName[priority])
        subq.tasks.pop(id)

    def append(self, data: Task) -> None:
        self.insert_task_id_to_subqueue(data.id, data.priority)
        self.tasks.append(data)

    def append_left(self, data: Task) -> None:
        self.insert_task_id_to_subqueue(data.id, data.priority)
        self.tasks.append_left(data)

    def append_right(self, data: Task) -> None:
        self.append(data)

    def pop(self, id: int) -> Node:
        curr_node = self.tasks.pop(id)
        self.pop_task_id_from_subqueue(id, curr_node.item.priority)
        return curr_node

    def pop_right(self) -> Node:
        curr_node = self.tasks.pop_right()
        self.pop_task_id_from_subqueue(curr_node.item.id, curr_node.item.priority)
        return curr_node

    def pop_left(self) -> Node:
        curr_node = self.tasks.pop_left()
        self.pop_task_id_from_subqueue(curr_node.item.id, curr_node.item.priority)
        return curr_node

    def insert_at_index(self, index: int, data: Task) -> None:
        self.insert_task_id_to_subqueue(data.id, data.priority)
        curr_node = self.tasks.insert_at_index(index, data)
        return curr_node

    def pop_at_index(self, index: int) -> Node:
        curr_node = self.tasks.pop_at_index(index)
        self.pop_task_id_from_subqueue(curr_node.item.id, curr_node.item.priority)
        return curr_node

    def get_node_by_id(self, id: int) -> Node:
        return self.tasks.get(id)


class TaskQueue(Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid_with_resources(
        self, task: Task, available_resources: Resources
    ) -> bool:
        task_resources = task.resources

        if (
            task_resources.ram <= available_resources.ram
            and task_resources.cpu_cores <= available_resources.cpu_cores
            and task_resources.gpu_count <= available_resources.gpu_count
        ):
            return True
        return False

    def get_task_from_subq(self, priority: int, available_resources: Resources) -> Task:
        subq = getattr(self, PriorityIntToName[priority])

        for task_id in subq.tasks.keys():
            task_node = self.get_node_by_id(task_id)
            if self.is_valid_with_resources(task_node.item, available_resources):
                valid_task_node = self.pop(task_id)
                return valid_task_node.item

        return False

    def add_task(self, task):
        self.append(task)

    def get_task(self, available_resources: Resources) -> Task:
        # start from high to low priority
        for priority_int in PriorityIntToName.keys():
            valid_task = self.get_task_from_subq(priority_int, available_resources)
            if valid_task is not False:
                return valid_task

        return None
