class IQueue:
    def __init__(self, maxlen=None):
        self._maxlen = maxlen
        self.queue = []

    def __iter__(self):
        self._index = -1
        return self

    def __next__(self):
        self._index += 1
        if self._index >= len(self.queue):
            raise StopIteration()
        return self.queue[self._index]

    def __repr__(self):
        return '<IQueue object>'

    def put(self, item):
        if self.is_full():
            raise Exception('queue is full')
        self.queue.append(item)

    def pop(self):
        if self.is_empty():
            raise Exception('queue is empty')
        result = self.queue[0]
        self.queue.pop(0)
        return result

    @property
    def length(self):
        return len(self.queue)

    def is_full(self):
        if not self._maxlen:
            return False
        if self.length >= self._maxlen:
            return True
        return False

    def is_empty(self):
        if self.length == 0:
            return True
        return False

# ################ Unit Test ###################### #

if __name__ == '__main__':
    import unittest

    class UnitTestIQueue(unittest.TestCase):
        def setUp(self):
            pass

        def tearDown(self):
            pass

        def testPutAndPop(self):
            q = IQueue()
            q.put(1)
            self.assertEqual(1, q.pop())

        def testFull(self):
            q = IQueue(1)
            q.put(1)
            self.assertRaises(Exception, q.put, 1)

        def testEmpty(self):
            q = IQueue()
            self.assertRaises(Exception, q.pop)

        def testLength(self):
            q = IQueue()
            for i in range(4):
                q.put(i)
            self.assertEqual(len(q.queue), q.length)

    unittest.main()
