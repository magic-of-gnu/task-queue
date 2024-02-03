import unittest

from project.doubly_linked_list import DoublyLinkedList, Node
from project.resources import Resources
from project.task import Task


class TestDoublyLinkedList(unittest.TestCase):
    def test_is_empty(self):
        """Test DLL is empty or not"""
        dll = DoublyLinkedList()
        self.assertTrue(dll.is_empty(), msg="doubly_linked_list is not empty")

        dll.start_node = Node({"id:": 1})
        dll.end_node = dll.start_node
        dll.nodes[1] = True

        self.assertFalse(dll.is_empty(), msg="doubly_linked_list is empty")

    def test_insert_to_empty_list(self):
        """Test inserting an object to an empty DLL"""
        dll = DoublyLinkedList()

        self.assertTrue(dll.is_empty(), msg="doubly_linked_list is not empty")
        task = Task(1, 1, Resources(1, 1, 1), "123", 0)

        dll.insert_to_empty_list(task)
        self.assertEqual(
            dll.start_node.item,
            task,
            msg="start_node.item and created task are not equal",
        )
        self.assertTrue(
            task.id in dll.nodes,
            msg="created task id does not exist among doubly_linked_list nodes",
        )

    def test_append(self):
        """Test appending an object to a DLL"""
        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append(task)

            self.assertEqual(
                len(dll), ii + 1, msg="wrong count of nodes in doubly_linked_list"
            )
            # self.assertEqual(dll.end_node.item, task, msg="wrong count of nodes in doubly_linked_list")

            tasks.append(task)
            nodes.append(curr_node)

        # check start node
        self.assertEqual(dll.start_node, nodes[0], msg="non identical start_nodes")
        self.assertIsNone(
            dll.start_node.prev_item, msg="previous item of start_node is not None"
        )
        self.assertEqual(
            dll.start_node.next_item, nodes[1], msg="wrong next_item for curr_node"
        )

        for ii in range(1, 4):
            prev_item, curr_item, next_item = nodes[ii - 1], nodes[ii], nodes[ii + 1]
            self.assertEqual(
                curr_item.prev_item, prev_item, msg="wrong prev_item for curr_item"
            )
            self.assertEqual(
                curr_item.next_item, next_item, msg="wrong next_item for curr_item"
            )

        self.assertEqual(dll.end_node, nodes[-1], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, nodes[-2], msg="wrong prev_item for end_node"
        )

    def test_get_node_by_id(self):
        """Test getting an object from a DLL via object id"""
        dll = DoublyLinkedList()

        for ii in range(10):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            dll.append(task)

            if ii == 5:
                target_task = task
                target_task_id = ii

        # correct length
        self.assertEqual(
            len(dll.nodes), 10, msg="wrong items count in doubly_linked_list"
        )

        retrieved_node = dll.get_node_by_id(target_task_id)
        self.assertEqual(
            retrieved_node.item.id,
            target_task_id,
            msg="different ids at retrieved and target tasks",
        )
        self.assertEqual(
            retrieved_node.item,
            target_task,
            msg="different tasks between retrieved and target tasks",
        )

    def test_append_left(self):
        """Test appending an object to a DLL from the left side"""
        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append_left(task)

            self.assertEqual(
                len(dll), ii + 1, msg="wrong count of nodes in doubly_linked_list"
            )

            tasks.append(task)
            nodes.append(curr_node)

        self.assertEqual(dll.start_node, nodes[-1], msg="non identical start_nodes")
        self.assertIsNone(
            dll.start_node.prev_item, msg="previous item of start_node is not None"
        )
        self.assertEqual(
            dll.start_node.next_item, nodes[-2], msg="wrong next_item for curr_node"
        )

        for ii in range(1, 4):
            prev_item, curr_item, next_item = nodes[ii + 1], nodes[ii], nodes[ii - 1]
            self.assertEqual(
                curr_item.prev_item, prev_item, msg="wrong prev_item for curr_item"
            )
            self.assertEqual(
                curr_item.next_item, next_item, msg="wrong next_item for curr_item"
            )

        self.assertEqual(dll.end_node, nodes[0], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, nodes[1], msg="wrong prev_item for end_node"
        )

    def test_pop_right_with_single_item_in_the_list(self) -> Node:
        """Test popping an object from DLL at the right side when DLL has only one item"""
        dll = DoublyLinkedList()

        # test pop when 1 item in the list
        task = Task(
            id=1,
            priority=1,
            resources=Resources(1, 1, 1),
            content="some content",
            result=0,
        )
        dll.append(task)

        self.assertEqual(len(dll), 1, msg="wrong count of nodes in doubly_linked_list")

        dll.pop_right()

        self.assertEqual(len(dll), 0, msg="wrong count of nodes in doubly_linked_list")
        self.assertIsNone(
            dll.start_node, msg="start_node of empty doubly_linked_list is not None"
        )
        self.assertIsNone(
            dll.end_node, msg="end_node of empty doubly_linked_list is not None"
        )

    def test_pop_right_with_multiple_item_in_the_list(self) -> Node:
        """Test popping an object from DLL at the right side when DLL has multiple items"""
        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append(task)

            tasks.append(task)
            nodes.append(curr_node)

        # check end_node for correctness
        self.assertEqual(dll.end_node, nodes[-1], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, nodes[-2], msg="wrong prev_item for end_node"
        )

        end_node = dll.pop_right()

        # check whether popped node is the end_node
        self.assertEqual(end_node, nodes[-1], msg="non identical end_nodes")
        self.assertIsNone(end_node.next_item, msg="next item of end_node is not None")
        self.assertEqual(
            end_node.prev_item, nodes[-2], msg="wrong prev_item for end_node"
        )

        # check whole list
        self.assertEqual(dll.start_node, nodes[0], msg="non identical start_nodes")
        self.assertIsNone(
            dll.start_node.prev_item, msg="previous item of start_node is not None"
        )
        self.assertEqual(
            dll.start_node.next_item, nodes[1], msg="wrong next_item for curr_node"
        )

        for ii in range(1, 3):
            prev_item, curr_item, next_item = nodes[ii - 1], nodes[ii], nodes[ii + 1]
            self.assertEqual(
                curr_item.prev_item, prev_item, msg="wrong prev_item for curr_item"
            )
            self.assertEqual(
                curr_item.next_item, next_item, msg="wrong next_item for curr_item"
            )

        self.assertEqual(dll.end_node, nodes[-2], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, nodes[-3], msg="wrong prev_item for end_node"
        )

    def test_pop_left_with_single_item_in_the_list(self) -> Node:
        """Test popping an object from DLL at the left side when DLL has only one item"""
        dll = DoublyLinkedList()

        # test pop when 1 item in the list
        task = Task(
            id=1,
            priority=1,
            resources=Resources(1, 1, 1),
            content="some content",
            result=0,
        )
        dll.append(task)

        self.assertEqual(len(dll), 1, msg="wrong count of nodes in doubly_linked_list")

        dll.pop_left()

        self.assertEqual(len(dll), 0, msg="wrong count of nodes in doubly_linked_list")
        self.assertIsNone(
            dll.start_node, msg="start_node of empty doubly_linked_list is not None"
        )
        self.assertIsNone(
            dll.end_node, msg="end_node of empty doubly_linked_list is not None"
        )

    def test_pop_left_with_multiple_item_in_the_list(self) -> Node:
        """Test popping an object from DLL at the left side when DLL has multiple items"""
        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append(task)

            tasks.append(task)
            nodes.append(curr_node)

        # check start_node for correctness
        self.assertEqual(dll.start_node, nodes[0], msg="non identical start_nodes")
        self.assertIsNone(
            dll.start_node.prev_item, msg="next item of start_node is not None"
        )
        self.assertEqual(
            dll.start_node.next_item, nodes[1], msg="wrong prev_item for start_node"
        )

        start_node = dll.pop_left()

        # check whether popped node is the start_node
        self.assertEqual(start_node, nodes[0], msg="non identical start_nodes")
        self.assertIsNone(
            start_node.prev_item, msg="next item of start_node is not None"
        )
        self.assertEqual(
            start_node.next_item, nodes[1], msg="wrong prev_item for start_node"
        )

        # check whole list
        self.assertEqual(dll.start_node, nodes[1], msg="non identical start_nodes")
        self.assertIsNone(
            dll.start_node.prev_item, msg="previous item of start_node is not None"
        )
        self.assertEqual(
            dll.start_node.next_item, nodes[2], msg="wrong next_item for curr_node"
        )

        for ii in range(2, 4):
            prev_item, curr_item, next_item = nodes[ii - 1], nodes[ii], nodes[ii + 1]
            self.assertEqual(
                curr_item.prev_item, prev_item, msg="wrong prev_item for curr_item"
            )
            self.assertEqual(
                curr_item.next_item, next_item, msg="wrong next_item for curr_item"
            )

        self.assertEqual(dll.end_node, nodes[-1], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, nodes[-2], msg="wrong prev_item for end_node"
        )

    def test_pop_with_single_item_in_the_list(self) -> Node:
        """Test popping an object from DLL via object id when DLL has only one item"""
        dll = DoublyLinkedList()

        # test pop when 1 item in the list
        task = Task(
            id=1,
            priority=1,
            resources=Resources(1, 1, 1),
            content="some content",
            result=0,
        )
        dll.append(task)

        self.assertEqual(len(dll), 1, msg="wrong count of nodes in doubly_linked_list")

        dll.pop(1)

        self.assertEqual(len(dll), 0, msg="wrong count of nodes in doubly_linked_list")
        self.assertIsNone(
            dll.start_node, msg="start_node of empty doubly_linked_list is not None"
        )
        self.assertIsNone(
            dll.end_node, msg="end_node of empty doubly_linked_list is not None"
        )

    def test_pop_with_multiple_item_in_the_list(self) -> Node:
        """Test popping an object from DLL via object id when DLL has only multiple items"""
        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append(task)

            tasks.append(task)
            nodes.append(curr_node)

        node = dll.pop(1)  # 0 1 2 3 4 -> pop(1)

        # check popped node
        self.assertEqual(node, nodes[1], msg="non identical nodes")
        self.assertEqual(node.next_item, nodes[2], msg="wrong next item of popped node")
        self.assertEqual(node.prev_item, nodes[0], msg="wrong prev_item of popped node")

        # pop first
        node = dll.pop(0)  # 0 2 3 4 -> pop(0)

        # check popped node
        self.assertEqual(node, nodes[0], msg="non identical nodes")
        self.assertEqual(node.next_item, nodes[2], msg="wrong next item of popped node")
        self.assertIsNone(node.prev_item, msg="prev_item of popped node is not None")

        # check new start_node
        self.assertEqual(dll.start_node, nodes[2], msg="non identical start_nodes")
        self.assertIsNone(
            dll.start_node.prev_item, msg="previous item of start_node is not None"
        )
        self.assertEqual(
            dll.start_node.next_item, nodes[3], msg="wrong next_item for curr_node"
        )

        # pop last
        node = dll.pop(4)  # 2 3 4 -> pop(4)

        # check popped node
        self.assertEqual(node, nodes[-1], msg="non identical nodes")
        self.assertIsNone(node.next_item, msg="next_item of node is not None")
        self.assertEqual(node.prev_item, nodes[-2], msg="wrong prev item of node")

        # check new end_node
        self.assertEqual(dll.end_node, nodes[-2], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, nodes[-3], msg="wrong next_item of end_node"
        )

    def test_insert_at_index(self):
        """Test insering an object into DLL at a certain index"""

        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append(task)

            self.assertEqual(
                len(dll), ii + 1, msg="wrong count of nodes in doubly_linked_list"
            )
            # self.assertEqual(dll.end_node.item, task, msg="wrong count of nodes in doubly_linked_list")

            tasks.append(task)
            nodes.append(curr_node)

        # insert in the middle
        new_task = Task(
            id=100,
            priority=1,
            resources=Resources(1, 1, 1),
            content="some content",
            result=0,
        )

        node = dll.insert_at_index(3, new_task)

        # check current node
        self.assertEqual(node.item, new_task, msg="wrong task for returned node")
        self.assertEqual(node.prev_item, nodes[3], msg="wrong prev_item for curr_item")
        self.assertEqual(node.next_item, nodes[4], msg="wrong next_item for curr_item")

        # check new end node
        self.assertEqual(dll.end_node, nodes[-1], msg="non identical end_nodes")
        self.assertIsNone(
            dll.end_node.next_item, msg="next item of end_node is not None"
        )
        self.assertEqual(
            dll.end_node.prev_item, node, msg="wrong prev_item for end_node"
        )

        # insert at the beginning
        new_task = Task(
            id=101,
            priority=1,
            resources=Resources(1, 1, 1),
            content="some content",
            result=0,
        )
        node = dll.insert_at_index(0, new_task)

        # check current node
        self.assertEqual(dll.start_node, node, msg="wrong node for returned node")
        self.assertIsNone(node.prev_item, msg="prev_item for inserted item is not None")
        self.assertEqual(node.next_item, nodes[0], msg="wrong next_item for curr_item")

        # insert at the end
        new_task = Task(
            id=102,
            priority=1,
            resources=Resources(1, 1, 1),
            content="some content",
            result=0,
        )
        n = len(dll)
        node = dll.insert_at_index(n - 1, new_task)

        # check current node
        self.assertEqual(dll.end_node, node, msg="wrong node for returned node")
        self.assertEqual(
            node.prev_item, nodes[4], msg="wrong next_item for returned_node"
        )
        self.assertIsNone(node.next_item, msg="next_item for inserted item is not None")

    def test_pop_at_index(self):
        """Test popping an object from DLL at a certain index"""

        dll = DoublyLinkedList()

        tasks = []
        nodes = []
        for ii in range(5):
            task = Task(
                id=ii,
                priority=1,
                resources=Resources(1, 1, 1),
                content="some content",
                result=0,
            )
            curr_node = dll.append(task)

            self.assertEqual(
                len(dll), ii + 1, msg="wrong count of nodes in doubly_linked_list"
            )
            # self.assertEqual(dll.end_node.item, task, msg="wrong count of nodes in doubly_linked_list")

            tasks.append(task)
            nodes.append(curr_node)

        # remove from the middle
        node = dll.pop_at_index(3)

        self.assertEqual(node, nodes[3], msg="nodes are not identical")
        self.assertEqual(
            nodes[2].next_item,
            nodes[4],
            msg="next_node was not changed after pop at the middle",
        )
        self.assertNotEqual(
            nodes[2].next_item, node, msg="next_node still points to deleted node"
        )

        self.assertEqual(
            nodes[4].prev_item,
            nodes[2],
            msg="next_node was not changed after pop at the middle",
        )
        self.assertNotEqual(
            nodes[4].prev_item, node, msg="next_node still points to deleted node"
        )

        # remove from the beginning
        node = dll.pop_at_index(0)

        self.assertEqual(dll.start_node, nodes[1], msg="start_node was not updated")
        self.assertIsNone(
            dll.start_node.prev_item, msg="start_node.prev_item is not None"
        )

        # remove from the beginning
        n = len(dll)
        node = dll.pop_at_index(n - 1)

        self.assertEqual(dll.end_node, nodes[2], msg="end_node was not updated")
        self.assertIsNone(dll.end_node.next_item, msg="end_node.next_item is not None")
