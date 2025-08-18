from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'App05Payoff'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class PayoffInformation(Page):
    form_model = 'player'


class ProlificPayoff(Page):
    form_model = 'player'


class ThankYou(Page):
    form_model = 'player'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group_matrix_comm = player.session.vars.get('group_matrix')
        player.in_round(1).group.subsession.set_group_matrix(group_matrix_comm)


page_sequence = [ThankYou]
