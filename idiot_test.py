from idiot import Idiot
import pytest
import mock
import builtins

class TestIdiot:

    # что вначале
    def setup(self):
        self.test_object = Idiot(8)
        open(self.test_object.data_source, 'w').close()

    # чем завершить
    def teardown(self):
        open(self.test_object.data_source, 'w').close()
        pass

    def test_init(self):
        assert self.test_object.cards_count_set == 8
        assert self.test_object.set_count == 1

    def test_user_step(self):
        with pytest.raises(SystemExit):
            with mock.patch.object(builtins, 'input', lambda _: 'd'):
                self.test_object.user_step()

    def test_actions(self):
        # with pytest.raises(TypeError):
        pass

# > 5 тестов, покрытие 100%, потестировать функции, порефакторить
# coverage run file
# coverage run --branch file
# coverage report
