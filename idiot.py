import random
import sys


class Idiot:
    cards_deck, user_range, comp_range = {}, {'cards': {}, 'active': True}, {'cards': {}, 'active': False}  # колода, карты пользователя, карты компьютера
    actions = {'n': 'бито, следующий ход', 't': 'не могу отбить, взял'} # доступные опции; @todo перевести, подкинуть
    card_types = ['Черви', 'Бубны', 'Трефы', 'Пики']
    cards_quality = {'Шестёрка': 0, 'Семёрка': 1, 'Восьмёрка': 2, 'Девятка': 3, 'Десятка': 4, 'Валет': 5, 'Дама': 6,
                     'Король': 7, 'Туз': 8}
    cards_count_set = 6  # по сколько карт сдаём
    set_cards = {}  # все карты кона
    set_count = 1 # какой по счёту кон

    def __init__(self):
        for type in self.card_types:
            self.cards_deck[type] = list(self.cards_quality.keys())

        print(f'\nТусуем колоду, раскидываем картишки: козырь {random.choice(self.card_types)}\n')

        self._get_cards(self.user_range)
        self._get_cards(self.comp_range)

        # @todo определить, кто ходит - найти в картах самый маленький козырь
        try:
            self.start()
        except Exception as e:
            print("Ошибка! ", e)

    def start(self):
        print('Я: ', self.user_range)
        print('Компьютер: ', self.comp_range)
        print('Колода: ', self.cards_deck)
        print('\n__Кон № {}__\n'.format(self.set_count))

        for x, y in self.actions.items():
            print(f"{x} - {y}")
        step = input('\nВыберите карту по номеру или действие ')

        if step == 'n':
            self.set_cards = {}
        elif step == 't':
            self.user_range['cards'] = {**self.user_range['cards'], **self.set_cards}
            print('__Взял__', self.user_range['cards'])
        elif step.isdigit():
            key = int(step)
            if key in list(self.user_range['cards'].keys()):
                # извлечь из моей колоды карту
                self.set_cards[f"user_{self.set_count}"] = self.user_range['cards'][key]
                self.comp_range['active'], self.user_range['active'] = True, False
                print('__Вы сходили картой__', self.set_cards)
            else:
                raise Exception('У Вас нет такой карты!')
        else:
            raise Exception('Не нашлось доступного действия: пожалуйста, повторите')

        return self.comp_step()

    def comp_step(self):
        print('\n__Ходит компьютер__')
        print('__Карты кона__', self.set_cards)
        # здесь будет ход - отбиться или взять

        self.user_range['active'], self.comp_range['active'] = True, False
        if self._new_set_init():
            return self.start()

    # сдать карты в начале, добрать после кона
    def _get_cards(self, cards_range):
        self._check_cards_deck()
        i = 0
        # если карты ещё есть, сдавать
        while len(cards_range['cards'].items()) < self.cards_count_set:
            new_type = random.choice(self.card_types) # self._check_cards_deck()
            random.shuffle(self.cards_deck[new_type])
            new_quality = self.cards_deck[new_type].pop()
            cards_range['cards'][i] = {'name': (new_type, new_quality), 'quality': self.cards_quality[new_quality]}
            i += 1

        return cards_range

    def _new_set_init(self):
        self.set_count += 1
        self._get_cards(self.user_range)
        self._get_cards(self.comp_range)

        return True

    def _check_cards_deck(self):
        # проверить, не закончились ли карты в масти, выбрать новую масть, если да
        # если все масти закончились, раздача карт завершается, игра идёт до последней карты
        pass


i = Idiot()
