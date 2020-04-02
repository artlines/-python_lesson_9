import os
import random
import json

class Idiot:
    __EX_OK__ = 0
    __EX_SOFTWARE__ = 8

    cards_deck, user_range, comp_range = {}, {'cards': {}, 'active': True}, {'cards': {}, 'active': False}  # колода, карты пользователя, карты компьютера
    actions = {'n': 'бито, следующий ход', 't': 'не могу отбить, взял', 'd': 'завершить игру'}  # доступные опции; @todo перевести, подкинуть
    card_types = ['Черви', 'Бубны', 'Трефы', 'Пики']
    cards_quality = {'Шестёрка': 0, 'Семёрка': 1, 'Восьмёрка': 2, 'Девятка': 3, 'Десятка': 4, 'Валет': 5, 'Дама': 6,
                     'Король': 7, 'Туз': 8}
    cards_count_set = 0  # по сколько карт сдаём
    set_cards = {}  # все карты кона
    set_count = 0  # какой по счёту кон
    data_source = 'data.json'

    def __init__(self, count):
        self.cards_count_set = count

        if os.path.exists(self.data_source) and os.path.getsize(self.data_source) > 0:
            self.load_data()

        for type in self.card_types:
            self.cards_deck[type] = list(self.cards_quality.keys())

        print('\n[Ход игры]', f'__Тусуем колоду, раскидываем картишки__\n')
        self._new_set_init()
        # @todo определить, кто ходит - найти в картах самый маленький козырь

    # ход игрока
    def user_step(self):
        if len(self.user_range['cards'].keys()) == 0:
            print('[Ход игры]', "___!!!__Вы выиграли!__!!!___")
            exit(self.__EX_OK__)

        print("__Доступные карты__")
        for key, card in self.user_range['cards'].items():
            print(f'№{key}: {" ".join(card["name"])} - {card["quality"]}')

        print("\n__Доступные действия__")
        for x, y in self.actions.items():
            print(f"{x} - {y}")

        set_action = 'Ваш ход' if self.user_range['active'] else 'Вы отбиваетесь'
        step = input(f'\n[Ход игры] {set_action}: выберите карту по номеру или действие ')

        # обработка ввода
        if step == 'n':
            if len(self.set_cards.keys()) == 0:
                raise Exception('Нет карт для сброса')

            print('[Ход игры]', '__Бито, следующий ход__')
            self.set_cards.clear()
            return self.user_step()

        elif step == 'd':
            print('[Ход игры]', "Игра закончена")
            open(self.data_source, 'w').close()
            exit(self.__EX_OK__)

        elif step == 't':
            if len(self.set_cards.keys()) == 0:
                raise Exception('Нет карт к принятию')

            print('__Взял__', self.user_range['cards'])
            comp_card = self.set_cards[f'comp_{self.set_count}']
            self.user_range['cards'].update({self.set_count: comp_card})
            self.set_cards.clear()
            return self.comp_step()

        elif step.isdigit():
            key = int(step)
            if key in list(self.user_range['cards'].keys()):
                user_card = self.user_range['cards'].pop(key, None)
                self.set_cards[f"user_{self.set_count}"] = user_card
                self.print_step(user_card)

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
            print('[Ход игры]', "___!!!__Компьтер выиграл!__!!!___")
            exit(os.EX_OK)

        print('\n[Ход игры]', '__Ходит компьютер__')
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

                self.print_step(comp_card_answer)
                self.set_cards[f"comp_{self.set_count}"] = comp_card_answer
                self._check_step()

            if self._new_set_init():
                self.user_range['active'], self.comp_range['active'] = False, True
                comp_card = random.choice(list(self.comp_range['cards'].keys()))
                set_card_key = f"comp_{self.set_count}"
                self.set_cards[set_card_key] = self.comp_range['cards'].pop(comp_card, None)
                print('[Ход игры]', '__Компьютер сходил картой__')
                self.print_step(self.set_cards[set_card_key])

                return self.user_step()
        except StopIteration:
            print('[Ход игры]', '__Нечем биться, компьютер берёт__')
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
            print('[Ход игры]', 'Карта бита, следующий кон')
            return True

        return False

    # сохранить данные в файл
    def save_data(self):
        data = {
            'cards_deck': self.cards_deck,
            'user_range': self.user_range,
            'comp_range': self.comp_range,
            'card_types': self.card_types,
            'set_cards' : self.set_cards,
            'set_count' : self.set_count
        }
        with open(self.data_source, 'w', encoding='utf8') as file:
            json_str = json.dumps(data, indent=4, ensure_ascii=False)
            file.write(json_str)

        return True

    # прочитать данные из файла
    def load_data(self):
        fields = ['cards_deck', 'user_range', 'comp_range', 'card_types', 'set_cards', 'set_count']
        with open(self.data_source, encoding='utf-8') as file:
            data = json.load(file, object_hook=lambda d: {int(k) if k.isdigit() else k: v for k, v in d.items()})

        for field in fields:
            setattr(__class__, field, data[field])

        return True

    @staticmethod
    def print_step(card):
        print(
            '[Ход игры]',
            '__Вы сходили картой__',
            f'{card["name"][0]}'
            f' {card["name"][1]}'
            f' - {card["quality"]}\n'
        )

        return True
