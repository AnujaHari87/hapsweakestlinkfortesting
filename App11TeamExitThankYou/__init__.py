
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'App11TeamExitThankYou'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
class ThankYouExit(Page):
    form_model = 'player'



page_sequence = [ThankYouExit]
