import random


class Idiot:
    cards_deck, user_range, comp_range = {}, {'cards': {}, 'active': True}, {'cards': {},
                                                                             'active': False}  # колода, карты пользователя, карты компьютера
    actions = {'n': 'бито, следующий ход', 't': 'не могу отбить, взял'}  # доступные опции; @todo перевести, подкинуть
    card_types = ['Черви', 'Бубны', 'Трефы', 'Пики']
    cards_quality = {'Шестёрка': 0, 'Семёрка': 1, 'Восьмёрка': 2, 'Девятка': 3, 'Десятка': 4, 'Валет': 5, 'Дама': 6,
                     'Король': 7, 'Туз': 8}
    cards_count_set = 6  # по сколько карт сдаём
    set_cards = {}  # все карты кона
    set_count = 0  # какой по счёту кон

    def __init__(self):
        for type in self.card_types:
            self.cards_deck[type] = list(self.cards_quality.keys())

        print(f'\n__Тусуем колоду, раскидываем картишки: козырь {random.choice(self.card_types)}__\n')
        self._new_set_init()

        # @todo определить, кто ходит - найти в картах самый маленький козырь
        self.user_step()

    # ход игрока
    def user_step(self):

        if len(self.user_range['cards'].keys()) == 0:
            print("___!!!__Вы выиграли!__!!!___")
            exit(8)

        print("__Доступные карты__")
        for key, card in self.user_range['cards'].items():
            print(key, '-', ' '.join(card['name']))

        print("__Доступные действия__")
        for x, y in self.actions.items():
            print(f"{x} - {y}")

        set_action = 'Ваш ход' if self.user_range['active'] else 'Вы отбиваетесь'
        step = input(f'\n{set_action}: выберите карту по номеру или действие ')

        # обработка ввода
        if step == 'n':
            if len(self.set_cards.keys()) > 0:
                print('__Бито, следующий ход__')
                self.set_cards.clear()
                return self.user_step()
            else:
                raise Exception('Нет карт для сброса')
        elif step == 't':
            if len(self.set_cards.keys()) > 0:
                print('__Взял__', self.user_range['cards'])
                comp_card = self.set_cards[f'comp_{self.set_count}']
                self.user_range['cards'].update({self.set_count: comp_card})
                self.set_cards.clear()
                return self.comp_step()
            else:
                raise Exception('Нет карт к принятию')
        elif step.isdigit():
            key = int(step)
            if key in list(self.user_range['cards'].keys()):
                self.set_cards[f"user_{self.set_count}"] = self.user_range['cards'].pop(key, None)
                print('__Вы сходили картой__', self.set_cards)
                # Пользователь отбивается или ходит
                if self.user_range['active']:
                    return self.comp_step()
                else:
                    if self._check_step() and self._new_set_init():
                        self.user_range['active'], self.comp_range['active'] = True, False
                        return self.user_step()
            else:
                raise Exception('У Вас нет такой карты!')
        else:
            raise Exception('Не нашлось доступного действия: пожалуйста, повторите')

    # ход компьютера
    def comp_step(self):
        if len(self.comp_range['cards'].keys()) == 0:
            print("___!!!__Компьтер выиграл!__!!!___")
            exit(8)

        print('\n__Ходит компьютер__')
        comp_cards = self.comp_range['cards']

        try:
            if self.user_range['active']:
                user_card = self.set_cards[f'user_{self.set_count}']
                user_card_type = user_card['name'][1]
                user_card_quality = user_card['quality']

                comp_card_answer = next(
                    x for x in comp_cards.values() if
                    x['quality'] > user_card_quality and x['name'][1] == user_card_type
                )
                print('__Компьютер отбивается картой__', comp_card_answer)
                self.set_cards[f"comp_{self.set_count}"] = comp_card_answer
                print('__Карты кона__', self.set_cards)
                self._check_step()

            if self._new_set_init():
                self.user_range['active'], self.comp_range['active'] = False, True
                comp_card = random.choice(list(self.comp_range['cards'].keys()))
                set_card_key = f"comp_{self.set_count}"
                self.set_cards[set_card_key] = self.comp_range['cards'].pop(comp_card, None)
                print('__Компьютер сходил картой__')
                print(
                    f'{self.set_cards[set_card_key]["name"][0]}'
                    f' {self.set_cards[set_card_key]["name"][1]}'
                    f' - {self.set_cards[set_card_key]["quality"]}\n'
                )

                return self.user_step()
        except StopIteration:
            print('__Нечем биться, компьютер берёт__')
            self.comp_range['cards'].update({self.set_count: user_card})
            if self._new_set_init():
                return self.user_step()
        except Exception as e:
            raise e

    # сдать карты в начале, добрать после кона
    def _get_cards(self, cards_range):
        i = 0
        # если карты ещё есть, сдавать
        while len(cards_range['cards'].items()) < self.cards_count_set:
            new_type = self._check_cards_deck()
            if not new_type:
                print('__Колода закончилась: играем с оставшимися картами__')
                return
            else:
                random.shuffle(self.cards_deck[new_type])
                new_quality = self.cards_deck[new_type].pop()
                cards_range['cards'][i] = {'name': (new_quality, new_type), 'quality': self.cards_quality[new_quality]}
                i += 1

        return cards_range

    # действия в начале нового кона
    def _new_set_init(self):
        self.set_count += 1
        self._get_cards(self.user_range)
        self._get_cards(self.comp_range)
        self.set_cards.clear()

        print('Мои карты: ', self.user_range)
        print('Карты компьютера: ', self.comp_range)
        print('Колода: ', self.cards_deck)
        print('\n__Кон № {}__\n'.format(self.set_count))

        return True

    # проверить, не закончились ли карты в масти, выбрать новую масть, если да
    def _check_cards_deck(self):
        new_type = random.choice(self.card_types) if len(self.card_types) > 0 else False
        if new_type and len(self.cards_deck[new_type]) == 0:
            print('__Карты масти {}  закончились__'.format(new_type))
            self.cards_deck.pop(new_type)
            self.card_types.remove(new_type)
            return self._check_cards_deck()

        return new_type

    # как играть
    def _check_step(self):
        active_key = 'user' if self.user_range['active'] else 'comp'
        active_card = self.set_cards.pop(f'{active_key}_{self.set_count}')
        cards_for_compare = [active_card, list(self.set_cards.values())[0]]
        is_quality = cards_for_compare[0]['quality'] < cards_for_compare[1]['quality']
        is_type = cards_for_compare[0]['name'][1] == cards_for_compare[1]['name'][1]

        if not is_quality:
            raise Exception('Карта не бьётся по величине')
        elif not is_type:
            # @todo добавить поддержку козырей
            raise Exception('Карта не бьётся по масти')
        elif is_quality and is_type:
            print('Карта бита, следующий кон')
            return True

        return False


i = Idiot()
