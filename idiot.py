import random


class Idiot:
    cards_deck, user_range, comp_range = {}, {}, {}
    card_types = ['Черви', 'Бубны', 'Трефы', 'Пики']
    cards_quality = {0: 'Шестёрка', 1: 'Семёрка', 2: 'Восьмёрка', 3: 'Девятка', 4: 'Десятка', 5: 'Валет', 6: 'Дама', 7: 'Король', 8: 'Туз'}
    # card_types = ['hearts', 'diamonds', 'spades', 'clubs']
    # cards_quality = {0: 'six', 1: 'seven', 2: 'eight', 3: 'nine', 4: 'ten', 5: 'jack', 6: 'queen', 7: 'king', 8: 'ace'}
    cards_count_set = 6

    def __init__(self):
        for type in self.card_types:
            self.cards_deck[type] = list(self.cards_quality.values())

        print(f'\nТусуем колоду, раскидываем картишки: козырь {random.choice(self.card_types)}\n')

        self.user_range = self._get_cards(self.user_range)
        self.comp_range = self._get_cards(self.comp_range)

        print('Мои карты', self.user_range)
        print('Карты компьютера', self.comp_range)
        print('Колода', self.cards_deck)

    def _get_cards(self, cards_range):
        while len(cards_range.items()) < self.cards_count_set:
            new_type = random.choice(self.card_types)
            random.shuffle(self.cards_deck[new_type])
            new_quality = self.cards_deck[new_type].pop()
            cards_range[new_quality] = new_type

        return cards_range

    def user_step(self):
        pass

    def comp_step(self):
        pass


idiot = Idiot()
