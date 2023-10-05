# tests.py
import unittest


def inc(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(inc(3), 4)
        self.assertEqual(inc(0), 1)
        self.assertEqual(inc(-9), -8)

    def test_with_error(self):
        self.assertEqual(inc(8), 5, msg=f"Ожидаемое значение не равно полученному")


if __name__ == "__main__":
    unittest.main()
