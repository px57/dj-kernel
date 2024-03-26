
import pprint

class TTest:
    def setUp(self) -> None:
        for a in range(10):
            pprint.pprint ('#' * 40, self._testMethodName)
        return super().setUp()