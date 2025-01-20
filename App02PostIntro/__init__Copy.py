from otree.api import *


import os

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = '02_Post_Intro'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass




def wait_for_all(group: Group):
    pass


def goal_wait_for_all(group: Group):
    pass


def make_image_data(image_names):
    return [dict(name=name, path='images/{}'.format(name)) for name in image_names]


def make_field(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label=label,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    ProlificId = models.StringField(label='Prolific ID')
    holidays_1 = make_field('Sun, sea, and beach holiday.')
    holidays_2 = make_field('Party holiday.')
    holidays_3 = make_field('Winter sports holiday.')
    holidays_4 = make_field('City trip.')
    holidays_5 = make_field('Backpacking holiday.')
    holidays_6 = make_field('Excursion.')
    holidays_7 = make_field('Camping holiday.')
    holidays_8 = make_field('Cruise holiday.')
    comp1_check = models.IntegerField(initial=0)
    comp2_check = models.IntegerField(initial=0)
    comp3_check = models.IntegerField(initial=0)
    comp4_check = models.IntegerField(initial=0)
    comprehension1 = models.IntegerField(
        label='<br><strong>What would be your compensation if you work 0 hours on Project A '
              'and the lowest contribution of a team member to Project A is 10 hours?</strong>', min=0, max=240)
    comprehension2 = models.IntegerField(
        label='<br><strong>What would be your compensation if you work 20 hours on Project A '
              'and the lowest contribution of a team member to Project A is 10 hours?</strong>', min=0, max=240)
    comprehension3 = models.IntegerField(
        label='<br><strong>What would be your compensation if you work 40 hours on Project A '
              'and the lowest contribution of a team member to Project A is 30 hours?</strong>', min=0, max=240)

    comprehension4a = models.BooleanField(
        default=False,
        label='',
        widget=widgets.CheckboxInput,
        blank=True
    )

    comprehension4b = models.BooleanField(
        default=False,
        label='',
        widget=widgets.CheckboxInput,
        blank=True
    )
    comprehension4c = models.BooleanField(
        default=False,
        label='',
        widget=widgets.CheckboxInput,
        blank=True
    )
    is_dropout = models.BooleanField(
        default=False,
        label='',
        blank=True
    )


def comprehension1_error_message(player: Player, value):
    if value != 200:
        player.comp1_check += 1
        if player.comp1_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        if player.comp1_check >= 2:
            return "Unfortunately, that's incorrect. The correct answer is <strong>200</strong>."
    return None  # Allow the participant to try again if they haven't clicked incorrectly twice


def comprehension2_error_message(player: Player, value):
    if value != 160:
        player.comp2_check += 1
        if player.comp2_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp2_check >= 2:
            return "Unfortunately, that's incorrect. The correct answer is <strong>160</strong>."
    return None


def comprehension3_error_message(player: Player, value):
    if value != 180:
        player.comp3_check += 1
        if player.comp3_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp3_check >= 2:
            return "Unfortunately, that's incorrect. The correct answer is <strong>180</strong>."
    return None


def comprehension4a_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."
    return None


def comprehension4b_error_message(player: Player, value):
    if value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."
    return None


def comprehension4c_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."
    return None


class EnterProlificId(Page):
    form_model = 'player'
    form_fields = ['ProlificId']


class PartsRoundsGroups(Page):
    form_model = 'player'


def group_by_arrival_time_method(subsession, waiting_players):
    print('in group_by_arrival_time_method')
    players_consent = [p for p in waiting_players if
                       p.participant.vars['consent'] == 1 and
                       p.participant.vars['micAndCameraCheck'] == 0
                       and p.participant.vars['numberVideo'] == 2 and p.participant.vars['colorVideo'] == 3]
    print(len(players_consent))
    if len(players_consent) >= 4:
        print('about to create a group')
        return [players_consent[0], players_consent[1], players_consent[2], players_consent[3]]


class MyWaitPage(WaitPage):
    group_by_arrival_time = True
    body_text = "Please wait until your team members arrive."

    def vars_for_template(self):
        waiting_players = self.session.get_participants()
        players_consent = [p for p in waiting_players if
                           p.vars.get('consent') == 1 and
                           p.vars.get('micAndCameraCheck') == 0
                           and p.vars.get('numberVideo') == 2 and p.vars.get('colorVideo') == 3]

        if len(players_consent) % 3 == 0:
            waiting_count = 4
        else:
            waiting_count = len(players_consent) % 4

        return {
            'waiting_count': waiting_count,
            'reload_interval': 5000,  # 5000 milliseconds = 5 seconds
        }

    def get_template_name(self):
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage2.html'

    def js_vars(self):
        waiting_players = self.session.get_participants()
        players_consent = [p for p in waiting_players if
                           p.vars.get('consent') == 1 and
                           p.vars.get('micAndCameraCheck') == 0
                           and p.vars.get('numberVideo') == 2 and p.vars.get('colorVideo') == 3]
        waiting_count = min(len(players_consent), 4)
        return {
            'waiting_count': waiting_count,
            'reload_interval': 5000  # 5000 milliseconds = 5 seconds
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
        import time
        start_time = time.time()
        group.session.vars['group_matrix'] = group.subsession.get_group_matrix()
        end_time = time.time()
        duration = end_time - start_time
        print(f"after_all_players_arrive took {duration} seconds")

class DescriptionVideoCommunication(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        import random
        holidays = ['holidays_1', 'holidays_2', 'holidays_3', 'holidays_4',
                    'holidays_5', 'holidays_6', 'holidays_7', 'holidays_8']
        random.shuffle(holidays)
        return holidays


class DescriptionVideoCommunication1(Page):
    form_model = 'player'


class GroupWaitPage(WaitPage):
    body_text = 'Please wait until all players in your group have entered the test video meeting.'
    after_all_players_arrive = goal_wait_for_all


class WaitBeforeVideoTest(WaitPage):
    after_all_players_arrive = goal_wait_for_all
    title_text = 'Please wait until all players have entered the test video meeting.'


class WaitBeforeVideo(WaitPage):
    after_all_players_arrive = goal_wait_for_all
    title_text = 'Please wait until all players have entered the video meeting.'


class VVC(Page):
    form_model = 'player'
    timeout_seconds = 600
    @staticmethod
    def vars_for_template(player: Player):
        optInConsent = player.participant.vars['optInConsent']
        return dict(optInConsent=optInConsent)


class VVC0(Page):
    form_model = 'group'
    timeout_seconds = 60


class EndVVC(Page):
    form_model = 'player'


class StudyIntroduction1(Page):
    form_model = 'player'


class StudyIntroduction2(Page):
    form_model = 'player'


class StudyIntroduction3(Page):
    form_model = 'player'


class StudyIntroduction4(Page):
    form_model = 'player'
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4a', 'comprehension4b',
                   'comprehension4c']


class Comprehension1(Page):
    form_model = 'player'
    form_fields = ['comprehension1']


class Comprehension2(Page):
    form_model = 'player'
    form_fields = ['comprehension2']


class Comprehension3(Page):
    form_model = 'player'
    form_fields = ['comprehension3']


class Comprehension4(Page):
    form_model = 'player'
    form_fields = ['comprehension4a', 'comprehension4b', 'comprehension4c']


page_sequence = [MyWaitPage, EnterProlificId, PartsRoundsGroups, DescriptionVideoCommunication, GroupWaitPage, VVC0,
                 DescriptionVideoCommunication1,
                 WaitBeforeVideo, VVC,
                 StudyIntroduction2, StudyIntroduction3, Comprehension1, Comprehension2, Comprehension3, Comprehension4]
