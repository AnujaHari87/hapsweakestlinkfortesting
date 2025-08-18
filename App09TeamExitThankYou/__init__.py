
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'App09TeamExitThankYou'
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


class MyWaitPage_TechProblem(WaitPage):
    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_TechProblem.html'


page_sequence = [MyWaitPage_TechProblem, ThankYouExit]
