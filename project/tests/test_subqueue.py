import unittest
from project.subqueue import SubQueue


class TestSubQueue(unittest.TestCase):
    def test_popleft(self):
        """Test popping an object from the left of the SubQueue"""
        subqueue = SubQueue(
            name="somename",
            tasks={
                "t1": 1,
                "t2": 2,
                "t3": 3,
            },
        )

        key, data = subqueue.popleft()
        self.assertEqual("t1", key, msg="wrong key popped from the subqueue")
        self.assertEqual(1, data, msg="wrong value popped from the subqueue")

        self.assertEqual(
            len(subqueue.tasks), 2, msg="wrong count after a pop from the subqueue"
        )

        keys = ["t2", "t3"]
        for ii, k in enumerate(subqueue.tasks.keys()):
            self.assertEqual(keys[ii], k)

    def test_popright(self):
        """Test popping an object from the right of the SubQueue"""
        subqueue = SubQueue(
            name="somename",
            tasks={
                "t1": 1,
                "t2": 2,
                "t3": 3,
            },
        )

        key, data = subqueue.popright()
        self.assertEqual("t3", key, msg="wrong key popped from the subqueue")
        self.assertEqual(3, data, msg="wrong value popped from the subqueue")

        self.assertEqual(
            len(subqueue.tasks), 2, msg="wrong count after a pop from the subqueue"
        )

        keys = ["t1", "t2"]
        for ii, k in enumerate(subqueue.tasks.keys()):
            self.assertEqual(keys[ii], k)
