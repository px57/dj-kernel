

class TTest:
    def setUp(self) -> None:
        for a in range(10):
            print ('#' * 40, self._testMethodName)
        return super().setUp()