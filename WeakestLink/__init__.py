
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'WeakestLink'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 5
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def calculateminchoice(group: Group):
    players = group.get_players()
    choices = [p.roundChoice for p in players]
    min_choice = min(choices)
    payoffTable = {1: [70, 0, 0, 0, 0,0,0],
                      2: [60,80,0, 0, 0,0,0],
                      3: [50,70,90, 0,0,0,0],
                      4: [40,60,80,100,0,0,0],
                      5: [30,50,70,90,110,0,0],
                      6: [20,40,60,80,100,120,0],
                      7: [10,30,50,70,90,110,130]}
    for player in players:
        player.minChoice = min_choice
        player.payoff = payoffTable[player.roundChoice][min_choice]
    
def wait_for_all(group: Group):
    pass
class Player(BasePlayer):
    roundChoice = models.IntegerField(initial=1, label='Your choice:', max=7, min=1)
    minChoice = models.IntegerField(initial=0)
class WaitBefore(WaitPage):
    after_all_players_arrive = wait_for_all
class WeakestLink1(Page):
    form_model = 'player'
    form_fields = ['roundChoice']
class WaitingScreen(WaitPage):
    after_all_players_arrive = calculateminchoice
    title_text = 'Weakest Link (Waiting screen)'
    body_text = 'Your choice has been reported.\u200b  Please wait until the other two participants have reported their choice.'
class Resultpage(Page):
    form_model = 'group'
page_sequence = [WaitBefore, WeakestLink1, WaitingScreen, Resultpage]
