import unittest

class TestMassiveChanges(unittest.TestCase):
    def setUp(self) -> None:
        self.path1 = r""
        self.path2 = r""
        self.path3 = r""

    def test_1(self):
        self.assertIsNone(self.path1)

    def test_2(self):
        self.assertIsNone(self.path2)

    def test_3(self):
        self.assertIsNone(self.path3)

if __name__ == '__main__':
    unittest.main()