from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'App01PreIntro'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def continue_function(group: Group):
    for player in group.get_players():
        player.payoff = 0


def wait_for_all(group: Group):
    pass


def goal_wait_for_all(group: Group):
    pass


class Player(BasePlayer):
    ProlificId = models.StringField(label='Prolific ID')

    audioCheck = models.IntegerField(blank=True, initial=0, choices=[[0, '0'], [1, '1']], label='Audio Output',
                                     attrs={"invisible": True})
    micCheck = models.IntegerField(blank=True, initial=0, choices=[[0, '0'], [1, '1']], label='Microphone Input',
                                   attrs={"invisible": True})
    cameraCheck = models.IntegerField(blank=True, initial=0, choices=[[0, '0'], [1, '1']], label='Camera View',
                                      attrs={"invisible": True})
    consent = models.IntegerField(blank=True, initial=0, choices=[[0, '0'], [1, '1']], label='Consent',
                                  attrs={"invisible": True})
    optInConsent = models.IntegerField(blank=True, initial=0, choices=[[0, '0'], [1, '1']], label='Opt-In Consent',
                                       attrs={"invisible": True})


class EnterProlificId(Page):
    form_model = 'player'
    form_fields = ['ProlificId']


class ConsentForm(Page):
    form_model = 'player'
    form_fields = ['consent', 'optInConsent']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.consent == 0:
            return 'App07ConsentThankYou'


class AudioVideoCheck(Page):
    form_model = 'player'
    form_fields = ['cameraCheck', 'audioCheck', 'micCheck']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.audioCheck == 0 or player.micCheck == 0 or player.cameraCheck == 0:
            return 'App06ThankYou'


class GeneralInformation(Page):
    form_model = 'player'


class PartsRoundsGroups(Page):
    form_model = 'player'


class WaitBeforeQuestionnaire(WaitPage):
    after_all_players_arrive = wait_for_all
    title_text = 'Please wait till other players are ready'


class DescriptionInterventions(Page):
    form_model = 'player'


class Interventions(Page):
    form_model = 'player'


page_sequence = [EnterProlificId, ConsentForm, AudioVideoCheck, GeneralInformation,
                 PartsRoundsGroups, WaitBeforeQuestionnaire, DescriptionInterventions, Interventions]
