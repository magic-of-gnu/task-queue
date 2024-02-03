from .task import Task


# node of a doubly linked list
class Node:
    def __init__(self, data) -> None:
        self.next_item, self.prev_item = None, None
        self.item = data


# doubly linked list with fast indexing of node/task id
class DoublyLinkedList:
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.nodes = dict()

    def __len__(self):
        return len(self.nodes)

    def is_empty(self):
        # TC: O(1); SC: O(1)
        return self.start_node is None and self.end_node is None and self.__len__() == 0

    def get_node_by_id(self, id: int) -> Node:
        # TC: O(1); SC: O(1)
        return self.nodes.get(id, None)

    def insert_to_empty_list(self, data: Task) -> None:
        # TC: O(1); SC: O(1)
        self.start_node = Node(data)
        self.nodes[data.id] = self.start_node

        return self.start_node

    def append(self, data: Task) -> Node:
        # TC: O(1); SC: O(1)

        # if empty
        if self.is_empty():
            return self.insert_to_empty_list(data)

        # if duplicates
        if data.id in self.nodes:
            raise ValueError("duplicate id in tasks")

        if self.__len__() == 1:
            old_end_node = self.start_node
        else:
            old_end_node = self.end_node

        new_item = Node(data)
        self.end_node = new_item
        old_end_node.next_item = self.end_node

        self.end_node.prev_item = old_end_node
        self.end_node.next_item = None

        self.nodes[data.id] = self.end_node

        return new_item

    def append_left(self, data: Task) -> None:
        # TC: O(1); SC: O(1)

        # if empty
        if self.is_empty():
            return self.insert_to_empty_list(data)

        # if duplicates
        if data.id in self.nodes:
            raise ValueError("duplicate id in tasks")

        if self.__len__() == 1:
            old_start_node = self.start_node
            self.end_node = old_start_node
        else:
            old_start_node = self.start_node

        new_item = Node(data)
        self.start_node = new_item
        old_start_node.prev_item = self.start_node

        self.start_node.next_item = old_start_node
        self.start_node.prev_item = None

        self.nodes[data.id] = self.start_node

        return new_item

    def append_right(self, data: Task) -> None:
        return self.append(data)

    def _actions_on_last_node_after_pop(self) -> None:
        # executed after pop
        if self.__len__() == 1:
            self.end_node = None
            self.start_node.prev_item = None
            self.start_node.next_item = None

    def _actions_on_pop_when_len_is_1(self) -> Node | None:
        # pop itself when len(q) == 1
        if self.__len__() == 1:
            node = self.start_node
            self.start_node = None
            self.end_node = None
            self.nodes.popitem()
            return node

        return None

    def pop_right(self) -> Node:
        # fast pop item from the right; TC: O(1); SC: O(1)
        if self.is_empty():
            return None

        tmp = self._actions_on_pop_when_len_is_1()
        if tmp is not None:
            return tmp

        # pop last and put prev of the last as the last
        old_end_node = self.end_node
        self.end_node = old_end_node.prev_item
        self.end_node.next_item = None

        self.nodes.pop(old_end_node.item.id)
        self._actions_on_last_node_after_pop()

        return old_end_node

    def pop_left(self) -> Task:
        # pop from the left; TC: O(1); SC: O(1)
        if self.is_empty():
            return None

        tmp = self._actions_on_pop_when_len_is_1()
        if tmp is not None:
            return tmp

        # pop first and put prev of the second as None
        old_start_node = self.start_node

        self.start_node = old_start_node.next_item
        self.start_node.prev_item = None

        self.nodes.pop(old_start_node.item.id)
        self._actions_on_last_node_after_pop()

        return old_start_node

    def pop(self, id: int) -> Node:
        # pop by id from anywhere; TC: O(1); SC: O(1)
        if self.is_empty() or (self.nodes.get(id, None) is None):
            raise ValueError(f"id {id} not found in tasks")

        tmp = self._actions_on_pop_when_len_is_1()
        if tmp is not None:
            return tmp

        # if first or last
        if self.start_node == self.nodes.get(id):
            return self.pop_left()
        elif self.end_node == self.nodes.get(id):
            return self.pop_right()

        node = self.nodes.pop(id)
        prev_item = node.prev_item
        next_item = node.next_item

        prev_item.next_item = next_item
        next_item.prev_item = prev_item

        self._actions_on_last_node_after_pop()

        return node

    def insert_at_index(self, index: int, data: Task) -> None:
        # insert at any index; TC: O(N); SC: O(1)
        # needed if one wants to implement task priority update or insert task into the middle (aka higher priority)
        if index < 0:
            raise ValueError("negative index does not exist in a list")

        if self.is_empty():
            raise ValueError(f"index {index} not found in empty list")

        if data.id in self.nodes:
            raise ValueError("duplicate id in tasks")

        if index >= len(self.nodes):
            raise ValueError(
                f"index {index} not found in list, list length: {len(self.nodes)}"
            )

        # if first
        if index == 0:
            return self.append_left(data)

        # if last
        if index == len(self.nodes) - 1:
            return self.append_right(data)

        ii = 1
        curr_item = self.start_node.next_item

        # if ii == 1 -> self.start_node.next_item
        # if ii == 2 -> self.start_node.next_item.next_item
        while ii < index:
            ii += 1
            curr_item = curr_item.next_item

        next_item = curr_item.next_item

        new_item = Node(data=data)
        curr_item.next_item = new_item

        new_item.prev_item = curr_item
        new_item.next_item = next_item

        next_item.prev_item = new_item

        self.nodes[data.id] = new_item
        return new_item

    def pop_at_index(self, index: int) -> Node:
        # pop at any index; TC: O(N); SC: O(1)
        # needed for removing task if previous tasks cannot be executed due to resource limitations
        if index < 0:
            raise ValueError("negative index does not exist in a list")

        if self.is_empty():
            raise ValueError(f"index {index} not found in empty list")

        if index >= len(self.nodes):
            raise ValueError(
                f"index {index} not found in list, list length: {len(self.nodes)}"
            )

        tmp = self._actions_on_pop_when_len_is_1()
        if tmp is not None:
            return tmp

        # if first or last
        if index == 0:
            return self.pop_left()
        elif index == self.__len__() - 1:
            return self.pop_right()

        ii = 0
        curr_item = self.start_node

        # if ii == 1 -> self.start_node.next_item
        # if ii == 2 -> self.start_node.next_item.next_item
        while ii < index:
            ii += 1
            curr_item = curr_item.next_item

        prev_item = curr_item.prev_item
        next_item = curr_item.next_item

        prev_item.next_item = next_item
        next_item.prev_item = prev_item

        self.nodes.pop(curr_item.item.id)

        return curr_item

    def get(self, id: int) -> Node:
        return self.nodes.get(id)
