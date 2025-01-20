import time

from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = '02_Post_Intro'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    waitCount = models.IntegerField(initial=0)


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

def make_field2(label):
    return models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label=label,
        widget=widgets.RadioSelect,
    )

class Player(BasePlayer):
    ProlificId = models.StringField(label='Prolific ID')
    riskFalk = make_field2(' ')

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
    waitpage_too_long = models.BooleanField(
        default=False,
        label='',
        blank=True
    )
    micCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )

    cameraCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )
    team1MicCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )
    team2MicCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )
    team3MicCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )

    team1CameraCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )
    team2CameraCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )
    team3CameraCheck = models.BooleanField(
        blank=True,
        label='',
        widget=widgets.CheckboxInput
    )
    groupExit = models.BooleanField(
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


class MyWaitPage(WaitPage):
    group_by_arrival_time = True
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage2.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        import time
        start_time = time.time()
        group.session.vars['group_matrix'] = group.subsession.get_group_matrix()
        end_time = time.time()
        duration = end_time - start_time
        print(f"after_all_players_arrive took {duration} seconds")


class EnterProlificId(Page):
    form_model = 'player'
    form_fields = ['ProlificId']

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            print('In PartsRoundsGroups')
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in PartsRoundsGroups')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class PartsRoundsGroups(Page):
    form_model = 'player'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            print('In PartsRoundsGroups')
            player.is_dropout = True
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in PartsRoundsGroups')
            print('Setting dropout to true in PartsRoundsGroups')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


def waiting_too_long(player):
    participant = player.participant

    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.vars['wait_page_arrival'] > 5 * 60


def group_by_arrival_time_method(subsession, waiting_players):
    print("number of players waiting:", len(waiting_players))

    for player in waiting_players:
        player.waitpage_too_long = waiting_too_long(player)
    subsession.waitCount = len(waiting_players)
    if len(waiting_players) >= 4:
        print('about to create a group')
        return waiting_players[:4]


class DescriptionVideoCommunication(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        import random
        holidays = ['holidays_1', 'holidays_2', 'holidays_3', 'holidays_4',
                    'holidays_5', 'holidays_6', 'holidays_7', 'holidays_8']
        random.shuffle(holidays)
        return holidays

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in DescriptionVideoCommunication')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

class PreVideoQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['riskFalk']

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in PreVideoQuestionnaire')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

class WaitBeforeVideoTest(WaitPage):
    title_text = 'Please wait until all players have entered the test video meeting.'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in WaitBeforeVideoTest')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True


class VVC0(Page):
    form_model = 'player'
    form_fields = ['micCheck', 'cameraCheck', 'team1MicCheck', 'team2MicCheck', 'team3MicCheck',
                   'team1CameraCheck', 'team2CameraCheck', 'team3CameraCheck']

    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened:
            player.participant.vars['cameraCheck'] = player.cameraCheck
            player.participant.vars['micCheck'] = player.micCheck
            player.participant.vars['wait_page_arrival'] = time.time()

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False

        is_dropout1 = player.group.get_player_by_id(1).is_dropout
        is_dropout2 = player.group.get_player_by_id(2).is_dropout
        is_dropout3 = player.group.get_player_by_id(3).is_dropout
        is_dropout4 = player.group.get_player_by_id(4).is_dropout
        return dict(
            dropouts={
                player.group.get_player_by_id(1).is_dropout,
                player.group.get_player_by_id(2).is_dropout,
                player.group.get_player_by_id(3).is_dropout,
                player.group.get_player_by_id(4).is_dropout},
            is_dropout=is_dropout,
            is_dropout1=is_dropout1,
            is_dropout2=is_dropout2,
            is_dropout3=is_dropout3,
            is_dropout4=is_dropout4
        )

        return dict(is_dropout=is_dropout)


class GroupWaitPage(WaitPage):
    body_text = 'Please wait until all players in your group have completed the test video meeting.'

    def after_all_players_arrive(group: Group):

        for p in group.get_players():  # Assuming group.get_players() returns a list of players
            print(p.id_in_group)
            checks = [p.group.get_player_by_id(1).cameraCheck,
                      p.group.get_player_by_id(1).micCheck,
                      p.group.get_player_by_id(2).team1CameraCheck,
                      p.group.get_player_by_id(2).team1MicCheck,
                      p.group.get_player_by_id(3).team2CameraCheck,
                      p.group.get_player_by_id(3).team2MicCheck,
                      p.group.get_player_by_id(4).team3CameraCheck,
                      p.group.get_player_by_id(4).team3MicCheck,
                      ]
            if p.is_dropout is False:
                # Remove checks based on dropout status
                if p.group.get_player_by_id(1).is_dropout is True:
                    checks.remove(p.group.get_player_by_id(1).cameraCheck)
                    checks.remove(p.group.get_player_by_id(1).micCheck)

                if p.group.get_player_by_id(2).is_dropout is True:
                    checks.remove(p.group.get_player_by_id(2).team1CameraCheck)
                    checks.remove(p.group.get_player_by_id(2).team1MicCheck)

                if p.group.get_player_by_id(3).is_dropout is True:
                    checks.remove(p.group.get_player_by_id(3).team2CameraCheck)
                    checks.remove(p.group.get_player_by_id(3).team2MicCheck)

                if p.group.get_player_by_id(4).is_dropout is True:
                    checks.remove(p.group.get_player_by_id(4).team3CameraCheck)
                    checks.remove(p.group.get_player_by_id(4).team3MicCheck)

                # Check if all remaining checks are set to 0
                if any(check == 0 for check in checks):
                    for player in p.get_players():
                        player.groupExit = True

    def app_after_this_page(player: Player, upcoming_apps):
        if player.groupExit:
            return 'App09TeamExitThankYou'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in WaitBeforeVideoTest')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True


class DescriptionVideoCommunication1(Page):
    form_model = 'player'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in DescriptionVideoCommunication1')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class WaitBeforeVideo(WaitPage):
    after_all_players_arrive = goal_wait_for_all
    title_text = 'Please wait until all players have entered the video meeting.'


class VVC(Page):
    form_model = 'player'
    timeout_seconds = 660

    @staticmethod
    def vars_for_template(player: Player):
        optInConsent = player.participant.vars['optInConsent']
        return dict(optInConsent=optInConsent)

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class StudyIntroduction2(Page):
    form_model = 'player'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in StudyIntroduction2')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class StudyIntroduction3(Page):
    form_model = 'player'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in StudyIntroduction3')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class Comprehension1(Page):
    form_model = 'player'
    form_fields = ['comprehension1']

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class Comprehension2(Page):
    form_model = 'player'
    form_fields = ['comprehension2']

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in Comprehension2')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class Comprehension3(Page):
    form_model = 'player'
    form_fields = ['comprehension3']

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in Comprehension3')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class Comprehension4(Page):
    form_model = 'player'
    form_fields = ['comprehension4a', 'comprehension4b', 'comprehension4c']

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in Comprehension4')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


page_sequence = [MyWaitPage, EnterProlificId, PartsRoundsGroups, PreVideoQuestionnaire,
                 DescriptionVideoCommunication,
                 # WaitBeforeVideoTest,
                 # VVC0,
                 #GroupWaitPage,
                 DescriptionVideoCommunication1, WaitBeforeVideo, VVC, StudyIntroduction2,
                 StudyIntroduction3, Comprehension1, Comprehension2, Comprehension3, Comprehension4]
