import time

from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'App01bConsentAndCheck'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    confirmConsent = models.IntegerField(blank=False, choices=[[0, '0'], [1, '1']], label='Do you want to participate?',
                                  attrs={"invisible": True})


def wait_for_all(group: Group):
    pass



class ConsentFormB2(Page):
    form_model = 'player'
    form_fields = ['confirmConsent']


    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.confirmConsent == 0:
            return 'App07ConsentThankYou'
        else:
            return 'App01cConsentAndCheck'


page_sequence = [ConsentFormB2]
# From Bella:
# New page sequence:
# page_sequence = [EligibilityCheck, ConsentFormA, ConsentFormA2, ConsentFormB, [ConsentFormB2],
#                  EnterProlificId, GeneralInformation, GeneralInformation2, AudioVideoCheck, AudioVideoCheck2,
#                  AudioVideoCheck3]
# I created a new page called "Eligibility Check", as it seems to be a new one added to the experiment.
# I split the ConsentFormA into ConsentFormA and ConsentFormA2, because the content of ConsentFormA was separated into
# two different pages. It needs to be added to the page sequence of the Python file.
# I also added the page ConsentFormB2, however I put it in brackets in the page sequence above, because ConsentFormB2
# must be displayed to users ONLY if they click "NO".
# The page GeneralInformation now must go after ConsentFormB2.
# Also added the page GeneralInformation2 right after GeneralInformation, because the study information has been split
# into two pages (first page with general info, and the second one with payment information).
# The pages PartsRoundsGroups and VVC0 seem to have been removed from the experiment.
# The page AudioVideoCheck seems to now be split into 3 different pages.

# NOTE FOR BELLA: Put the right page if the user says 'No'! ! ! ! You will need to create a new app (with the folder
# and all for it)!
