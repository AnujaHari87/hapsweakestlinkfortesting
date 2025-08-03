import time

from otree.api import *
import re

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'App01cConsentAndCheck'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ProlificId = models.StringField(label='Please enter your Prolific ID so that we can pay you.')
    willingToInteract = models.IntegerField(blank=False, choices=[[0, '0'], [1, '1']], label='',
                                  attrs={"invisible": True})
    willingToBePaid = models.IntegerField(blank=False, choices=[[0, '0'], [1, '1']], label='',
                                            attrs={"invisible": True})
    camMicStatus = models.IntegerField(blank=False, choices=[[0, '0'], [1, '1']], label='',
                                            attrs={"invisible": True})
    colorVideo = models.IntegerField(blank=False, label="What color was mentioned in the video?",
                                     choices=[[0, 'Red'], [1, 'Blue'], [2, 'Green'], [3, 'Yellow']])
    numberVideo = models.IntegerField(blank=False, label="Which number was shown in the video?",
                                      choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']])
    is_dropout = models.BooleanField(
        default=False,
        label='',
        blank=True
    )

def ProlificId_error_message(player: Player, value):
    if not re.fullmatch(r'^[A-Za-z0-9]{24}$', value):
        return "Prolific ID must be exactly 24 alphanumeric characters (letters and numbers only)."
    return None

def wait_for_all(group: Group):
    pass


class EnterProlificId(Page):
    form_model = 'player'
    form_fields = ['ProlificId']


# NOTE FOR BELLA AND ANUJA: CHECK THE DROPOUT LOGIC !!!

class GeneralInformation(Page):
    form_model = 'player'



class GeneralInformation2(Page):
    form_model = 'player'



class AudioVideoCheck(Page):
    form_model = 'player'
    form_fields = ['willingToInteract', 'willingToBePaid', 'camMicStatus']

    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened:
            player.participant.vars['wait_page_arrival'] = time.time()



class AudioVideoCheck2(Page):
    form_model = 'player'

    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened:
            player.participant.vars['wait_page_arrival'] = time.time()

    @staticmethod
    def live_method(player, data):
        if 'internet_speed' in data:
            print( data['internet_speed'])
            print("internet speed for player " + str(player.id_in_group))


class AudioVideoCheck3(Page):
    form_model = 'player'
    form_fields = ['colorVideo', 'numberVideo']

    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened:
            player.participant.vars['colorVideo'] = player.colorVideo
            player.participant.vars['numberVideo'] = player.numberVideo
            player.participant.vars['wait_page_arrival'] = time.time()


    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.numberVideo != 2 or player.colorVideo != 3:
            return 'App06ThankYou'




page_sequence = [EnterProlificId, GeneralInformation, GeneralInformation2, AudioVideoCheck, AudioVideoCheck2,
                 AudioVideoCheck3]
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
