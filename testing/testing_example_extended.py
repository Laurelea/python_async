import unittest


def inc(x):
    return x + 1


class MyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("Run before all tests...")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Run after all tests...")

    def setUp(self) -> None:
        print("Run before each test..")

    def tearDown(self) -> None:
        print("Run after each test..")

    def test_simple(self):
        self.assertEqual(inc(3), 4)
        self.assertEqual(inc(0), 1)
        self.assertEqual(inc(-9), -8)

    @unittest.skip("demonstration")
    def test_extra(self):
        self.assertEqual(inc(20), 21)

    def test_with_error(self):
        self.assertEqual(inc(8), 5, msg="Ожидаемое значение не равно полученному")


if __name__ == "__main__":
    unittest.main()
