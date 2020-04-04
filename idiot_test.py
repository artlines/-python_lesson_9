from idiot import Idiot
import pytest
import mock
import builtins
import os


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
                assert os.path.exists(self.test_object.data_source) and os.path.getsize(
                    self.test_object.data_source) == 0

        with mock.patch.object(builtins, 'input', lambda _: 'n'):
            assert self.test_object.set_cards == {}

    def test_comp_step(self):
        assert self.test_object.user_range['active'] == True
        assert len(list(self.test_object.set_cards.keys())) == 0

        with pytest.raises(SystemExit):
            with mock.patch.object(builtins, 'input', lambda _: 'd'):
                self.test_object.comp_step()
                assert os.path.exists(self.test_object.data_source) and os.path.getsize(
                    self.test_object.data_source) == 0

        assert self.test_object.comp_range['active'] == True
        assert len(list(self.test_object.set_cards.keys())) > 0

