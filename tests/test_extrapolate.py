from emission import Extrapolate


class TestExtrapolate:
    def test_create(self):
        obj = Extrapolate([1, 2, 3], [1, 2, 3])
        assert obj.extrap(3) == 3.0
        assert obj.extrap(5) == 5.0
