from collections import defaultdict
import unittest

from project.resources import Resources
from project.task import Task
from project.task_queue import PriorityIntToName, Queue, TaskQueue


class TestQueue(unittest.TestCase):
    def test_len(self):
        """Test queue length"""
        q = Queue(1, "q1")
        resources = Resources(1, 1, 1)

        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName.keys()):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )

            subq = getattr(q, PriorityIntToName[priority_int])
            subq.tasks[ii] = True

            q.tasks.append(task)

            self.assertEqual(len(q), ii + 1, msg="wrong queue length")

        for priority_name in PriorityIntToName.values():
            subq = getattr(q, priority_name)
            self.assertEqual(len(subq.tasks), 1, msg="wrong queue length")

    def test_subq_len(self):
        """Test subqueue length"""
        q = Queue(1, "q1")
        resources = Resources(1, 1, 1)

        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName.keys()):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )

            subq = getattr(q, PriorityIntToName[priority_int])
            subq.tasks[ii] = True

            q.tasks.append(task)

        for priority_int in PriorityIntToName.keys():
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")

    def test_insert_task_id_to_subqueue(self):
        """Test inserting an object into a subqueue"""
        q = Queue(1, "q1")
        resources = Resources(1, 1, 1)

        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )
            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")
            q.insert_task_id_to_subqueue(ii, priority_int)
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")

            q.tasks.append(task)

        self.assertEqual(len(q), 5, msg="wrong queue length")

    def test_pop_task_id_from_subqueue(self):
        """Test popping an object from a subqueue via object id"""

        q = Queue(1, "q1")

        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName):
            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")
            q.insert_task_id_to_subqueue(ii, priority_int)
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")
            q.pop_task_id_from_subqueue(ii, priority_int)
            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")

        self.assertEqual(len(q), 0, msg="wrong queue length")

    def test_append(self):
        """Test inserting an object into a queue at the right (end of the queue)"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )

            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")
            q.append(task)

            self.assertEqual(len(q), ii + 1, msg="wrong queue length")
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")

    def test_append_left(self):
        """Test inserting an object into a queue at the right (beginning of the queue)"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )

            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")
            q.append_left(task)

            self.assertEqual(len(q), ii + 1, msg="wrong queue length")
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")

    def test_append_right(self):
        """Test inserting an object into a queue at the right (end of the queue)"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )

            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")
            q.append_right(task)

            self.assertEqual(len(q), ii + 1, msg="wrong queue length")
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")

    def test_pop(self):
        """Test popping an object from a queue by using object id"""
        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for priority_int in PriorityIntToName.keys():
            task = Task(
                priority_int,
                priority_int,
                resources,
                "some-content",
                123,
            )

            q.append(task)

        n = len(q)
        for ii, priority_int in enumerate(PriorityIntToName.keys()):
            self.assertEqual(len(q), n - ii, msg="wrong queue length")
            self.assertEqual(q.subq_len(priority_int), 1, msg="wrong sub queue length")
            q.pop(priority_int)
            self.assertEqual(q.subq_len(priority_int), 0, msg="wrong sub queue length")
            self.assertEqual(len(q), n - ii - 1, msg="wrong queue length")

    def test_pop_right(self):
        """Test popping an object from a queue from right (end of the queue)"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for priority_int in PriorityIntToName.keys():
            task = Task(
                priority_int,
                priority_int,
                resources,
                "some-content",
                123,
            )

            q.append(task)

        n = len(q)
        ii = 0
        while len(q) > 0:
            self.assertEqual(len(q), n - ii, msg="wrong queue length")
            node = q.pop_right()
            self.assertEqual(
                q.subq_len(node.item.priority), 0, msg="wrong sub queue length"
            )
            self.assertEqual(len(q), n - ii - 1, msg="wrong sub queue length")
            ii += 1

        self.assertEqual(len(q), 0, msg="wrong queue length")

    def test_pop_left(self):
        """Test popping an object from a queue from left (beginning of the queue)"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for priority_int in PriorityIntToName.keys():
            task = Task(
                priority_int,
                priority_int,
                resources,
                "some-content",
                123,
            )

            q.append(task)

        n = len(q)
        ii = 0
        while len(q) > 0:
            self.assertEqual(len(q), n - ii, msg="wrong queue length")
            node = q.pop_left()
            self.assertEqual(
                q.subq_len(node.item.priority), 0, msg="wrong sub queue length"
            )
            self.assertEqual(len(q), n - ii - 1, msg="wrong sub queue length")
            ii += 1

        self.assertEqual(len(q), 0, msg="wrong queue length")

    def test_insert_at_index(self):
        """Test inserting an object into a queue at index"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for priority_int in PriorityIntToName.keys():
            task = Task(
                priority_int,
                priority_int,
                resources,
                "some-content",
                123,
            )

            q.append(task)

        self.assertEqual(len(q), len(PriorityIntToName), msg="wrong queue length")

        task = Task(
            100,
            priority_int,
            resources,
            "some-content",
            123,
        )
        q.insert_at_index(3, task)

        self.assertEqual(len(q), len(PriorityIntToName) + 1, msg="wrong queue length")
        self.assertEqual(q.subq_len(task.priority), 2, msg="wrong subqueue length")

    def test_pop_at_index(self):
        """Test popping an object from at index"""

        q = Queue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(q), 0, msg="wrong queue length")

        for priority_int in PriorityIntToName.keys():
            task = Task(
                priority_int,
                priority_int,
                resources,
                "some-content",
                123,
            )

            q.append(task)

        self.assertEqual(len(q), len(PriorityIntToName), msg="wrong queue length")

        node = q.pop_at_index(3)

        self.assertEqual(len(q), len(PriorityIntToName) - 1, msg="wrong queue length")
        self.assertEqual(q.subq_len(node.item.priority), 0, msg="wrong subqueue length")


class TestTaskQueue(unittest.TestCase):
    def test_is_valid_with_resources(self):
        """Test checking whether the consumer has available resources for a task"""
        tq = TaskQueue(1, "q1")
        available_resources = Resources(100, 100, 10)

        invalid_resources = [
            Resources(101, 10, 1),
            Resources(10, 101, 1),
            Resources(10, 1, 11),
        ]

        valid_resources = [
            Resources(100, 10, 1),
            Resources(100, 100, 1),
            Resources(100, 100, 10),
            Resources(10, 100, 1),
            Resources(10, 1, 10),
        ]

        for item in invalid_resources:
            task = Task(1, 1, item, "content", 123)
            self.assertFalse(
                tq.is_valid_with_resources(task, available_resources),
                msg="task resources are valid",
            )

        for item in valid_resources:
            task = Task(1, 1, item, "content", 123)
            self.assertTrue(
                tq.is_valid_with_resources(task, available_resources),
                msg="task resources are valid",
            )

    def test_append(self):
        """Test appending tasks to a queue"""
        tq = TaskQueue(1, "q1")

        resources = Resources(1, 1, 1)
        self.assertEqual(len(tq), 0, msg="wrong queue length")

        for ii, priority_int in enumerate(PriorityIntToName):
            task = Task(
                ii,
                priority_int,
                resources,
                "some-content",
                123,
            )

            self.assertEqual(tq.subq_len(priority_int), 0, msg="wrong sub queue length")
            tq.add_task(task)

            self.assertEqual(len(tq), ii + 1, msg="wrong queue length")
            self.assertEqual(tq.subq_len(priority_int), 1, msg="wrong sub queue length")

    def test_get_task_from_subq(self):
        """Test getting tasks from subqueue"""

        tq = TaskQueue(1, "q1")
        available_resources = Resources(10, 10, 10)

        # get tasks with valid resources
        task_resources = Resources(5, 5, 5)
        self.assertEqual(len(tq), 0, msg="wrong queue length")

        ii = 0
        for priority_int in PriorityIntToName:
            self.assertEqual(tq.subq_len(priority_int), 0, msg="wrong sub queue length")
            for _ in range(3):
                task = Task(
                    ii,
                    priority_int,
                    task_resources,
                    "some-content",
                    123,
                )
                ii += 1
                tq.add_task(task)

            self.assertEqual(tq.subq_len(priority_int), 3, msg="wrong sub queue length")

        self.assertEqual(len(tq), 15, msg="wrong queue length")

        n = len(tq)
        ii = 0
        for priority_int in PriorityIntToName:
            task = tq.get_task_from_subq(priority_int, available_resources)

            self.assertEqual(tq.subq_len(priority_int), 2, msg="wrong sub queue length")
            self.assertEqual(len(tq), n - ii - 1)
            ii += 1

        # get tasks with valid resources
        resources = Resources(1, 1, 1)
        n = len(tq)
        for priority_int in PriorityIntToName:
            task = tq.get_task_from_subq(priority_int, resources)

            self.assertFalse(task, msg="task is not False")
            self.assertEqual(tq.subq_len(priority_int), 2, msg="wrong sub queue length")
            self.assertEqual(len(tq), n)

    def test_get_task(self):
        """Check functionality of get_task with constant resources for every priority"""

        tq = TaskQueue(1, "q1")
        task_resources = {
            1: Resources(100, 100, 10),
            2: Resources(50, 50, 10),
            3: Resources(10, 10, 0),
            4: Resources(5, 5, 0),
            5: Resources(2, 2, 0),
        }

        self.assertEqual(len(tq), 0, msg="wrong queue length")

        tasks = defaultdict(list)

        ii = 0
        for priority_int in PriorityIntToName:
            self.assertEqual(tq.subq_len(priority_int), 0, msg="wrong sub queue length")
            curr_resources = task_resources[priority_int]
            for _ in range(5):
                task = Task(
                    ii,
                    priority_int,
                    curr_resources,
                    "some-content",
                    123,
                )
                ii += 1
                tq.add_task(task)
                tasks[priority_int].append(task)

            self.assertEqual(tq.subq_len(priority_int), 5, msg="wrong sub queue length")

        self.assertEqual(len(tq), 25, msg="wrong queue length")

        n = len(tq)
        ii = 0
        for priority_int in tasks.keys():
            curr_resources = task_resources[priority_int]
            t1 = tq.get_task(curr_resources)
            t2 = tq.get_task(curr_resources)

            self.assertEqual(tq.subq_len(priority_int), 3, msg="wrong sub queue length")
            self.assertEqual(len(tq), n - 2 * (ii + 1))

            self.assertEqual(
                t1,
                tasks[priority_int][0],
                msg="retrieved and added tasks are different",
            )
            self.assertEqual(
                t2,
                tasks[priority_int][1],
                msg="retrieved and added tasks are different",
            )
            ii += 1

    def test_get_task_with_varying_task_resources_for_priority(self):
        """Check functionality of get_task with constant resources for every priority"""

        tq = TaskQueue(1, "q1")
        task_resources = {
            1: Resources(100, 100, 10),
            2: Resources(50, 50, 10),
            3: Resources(10, 10, 0),
            4: Resources(5, 5, 0),
            5: Resources(2, 2, 0),
        }

        self.assertEqual(len(tq), 0, msg="wrong queue length")

        ii = 0
        for _ in range(5):
            for priority_int in PriorityIntToName:
                curr_resources = task_resources[priority_int]
                task = Task(
                    ii,
                    priority_int,
                    curr_resources,
                    "some-content",
                    123,
                )
                ii += 1
                tq.add_task(task)

        for priority_int in PriorityIntToName.keys():
            self.assertEqual(tq.subq_len(priority_int), 5, msg="wrong sub queue length")

        self.assertEqual(len(tq), 25, msg="wrong queue length")

        n = len(tq)
        ii = 0
        for priority_int in PriorityIntToName.keys():
            curr_resources = task_resources[priority_int]
            tq.get_task(curr_resources)
            tq.get_task(curr_resources)

            self.assertEqual(tq.subq_len(priority_int), 3, msg="wrong sub queue length")
            self.assertEqual(len(tq), n - 2 * (ii + 1))
            ii += 1

    def test_get_no_task_due_to_low_available_resources(self):
        """Test getting no task since consumer does not fit task resources"""
        tq = TaskQueue(1, "q1")
        task_resources = Resources(3, 3, 3)
        tasks = []

        for priority_int in PriorityIntToName:
            self.assertEqual(tq.subq_len(priority_int), 0, msg="wrong sub queue length")
            task = Task(
                priority_int,
                priority_int,
                task_resources,
                "some-content",
                123,
            )
            tq.add_task(task)
            tasks.append(task)
            self.assertEqual(tq.subq_len(priority_int), 1, msg="wrong sub queue length")

        self.assertEqual(len(tq), 5, msg="wrong queue length")

        ii = 1
        for _ in range(1, 3):
            available_resources = Resources(ii, ii, ii)
            t = tq.get_task(available_resources)

            self.assertEqual(len(tq), 5, msg="wrong queue length")
            self.assertIsNone(t, msg="retreived task is not None")
            ii += 1

        ii = 3
        available_resources = Resources(ii, ii, ii)
        t = tq.get_task(available_resources)
        self.assertEqual(t, tasks[0], msg="retreived and added tasks are not the same")
        self.assertEqual(len(tq), 4, msg="wrong queue length")


class TestTaskQueueWithManyTasks(unittest.TestCase):
    def add_tasks_to_queue(self, tq: TaskQueue, ntasks: int) -> [Task]:
        tasks = []
        for task_id in range(1, ntasks + 1):
            priority_int = 5 if task_id % 5 == 0 else task_id % 5
            task_resources = Resources(task_id, task_id, task_id)
            task = Task(
                task_id,
                priority_int,
                task_resources,
                "some-content",
                123,
            )
            tq.add_task(task)
            tasks.append(task)

        return tasks

    def get_tasks_from_queue(
        self, tq: TaskQueue, ntasks: int, available_resources: Resources
    ) -> [Task]:
        tasks = []
        for _ in range(ntasks):
            task = tq.get_task(available_resources)
            if task is None:
                return tasks

            tasks.append(task)

        return tasks

    def test_task_queue_with_many_tasks(self):
        tq = TaskQueue(1, "q1")
        # add tasks
        ntasks = 10000

        self.add_tasks_to_queue(tq, ntasks)
        self.assertEqual(len(tq), ntasks, msg="wrong queue length")

        # get not full list
        n = 2000
        available_resources = Resources(n, n, n)
        tasks = self.get_tasks_from_queue(tq, 5000, available_resources)

        self.assertEqual(len(tq), ntasks - n, msg="wrong queue length")
        self.assertEqual(len(tasks), n, msg="wrong tasks length")

        # get full list
        n2 = 200
        available_resources = Resources(100 * n2, 100 * n2, 100 * n2)
        tasks = self.get_tasks_from_queue(tq, 5000, available_resources)
