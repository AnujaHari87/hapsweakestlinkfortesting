import time

from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = '02_Post_Intro'
    PLAYERS_PER_GROUP = 3
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
        label='<br><strong>What would your payoff be if you contribute 0 hours to Project A '
              'and the minimum number of hours contributed to Project A by any team member other than yourself '
              'is 10 hours?</strong>', min=0, max=400)
    comprehension2 = models.IntegerField(
        label='<br><strong>What would your payoff be if you contribute 20 hours to Project A and the minimum '
              'number of hours contributed to Project A by any team member other than yourself is 10 hours?</strong>',
              min=0, max=400)
    comprehension3 = models.IntegerField(
        label='<br><strong>What would your payoff be if you contribute 40 hours to Project A and the minimum '
              'number of hours contributed to Project A by any team member other than yourself is 30 hours?</strong>',
              min=0, max=400)

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
    no_dropout = models.BooleanField(
        default=False,
        label='',
        blank=True
    )
    group_see_hear = models.BooleanField(
        default=True,
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


    seeHear = models.IntegerField(blank=False, choices=[[0, '0'], [1, '1']], label='',
                                         attrs={"invisible": True})

    groupExit = models.BooleanField(
        default=False,
        label='',
        blank=True
    )


def comprehension1_error_message(player: Player, value):
    if value != 200:
        player.comp1_check += 1
        if player.comp1_check == 1:
            return "Unfortunately, your answer is not correct. Please try again."
        if player.comp1_check >= 2:
            return "Unfortunately, your answer is not correct. The correct answer is <strong>200</strong>. <strong>Please enter the correct answer</strong> and click the \"Next\" button to proceed."
    return None  # Allow the participant to try again if they have clicked incorrectly twice


def comprehension2_error_message(player: Player, value):
    if value != 200:
        player.comp2_check += 1
        if player.comp2_check == 1:
            return "Unfortunately, your answer is not correct. Please try again."
        elif player.comp2_check >= 2:
            return "Unfortunately, your answer is not correct. The correct answer is <strong>200</strong>. <strong>Please enter the correct answer</strong> and click the \"Next\" button to proceed."
    return None


def comprehension3_error_message(player: Player, value):
    if value != 300:
        player.comp3_check += 1
        if player.comp3_check == 1:
            return "Unfortunately, your answer is not correct. Please try again."
        elif player.comp3_check >= 2:
            return "Unfortunately, your answer is not correct. The correct answer is <strong>300</strong>. <strong>Please enter the correct answer</strong> and click the \"Next\" button to proceed."
    return None


def comprehension4a_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, your answer is not correct. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, your answer is not correct. The correct answer is that your payoff depends on the <strong>number of hours you contribute to Project A</strong> and the <strong>minimum number of hours contributed to Project A by a team member other than yourself</strong>. <strong>Please select the correct answers and click the \"Next\" button to proceed.</strong>"
    return None


def comprehension4b_error_message(player: Player, value):
    if value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, your answer is not correct. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, your answer is not correct. The correct answer is that your payoff depends on the <strong>number of hours you contribute to Project A</strong> and the <strong>minimum number of hours contributed to Project A by a team member other than yourself</strong>. <strong>Please select the correct answers and click the Next button to proceed.</strong>"
    return None


def comprehension4c_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, your answer is not correct. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, your answer is not correct. The correct answer is that your payoff depends on the <strong>number of hours you contribute to Project A</strong> and the <strong>minimum number of hours contributed to Project A by a team member other than yourself</strong>. <strong>Please select the correct answers and click the Next button to proceed.</strong>"
    return None


class MyWaitPageStage2Instructions(WaitPage):
    group_by_arrival_time = True
    body_text = "Please wait until your team members arrive."
    @staticmethod
    def vars_for_template(player):
        return dict(waiting_count=player.subsession.waitCount)


    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_Stage2Instructions.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        import time
        start_time = time.time()
        group.session.vars['group_matrix'] = group.subsession.get_group_matrix()
        end_time = time.time()
        duration = end_time - start_time
        print(f"after_all_players_arrive took {duration} seconds")

class MyWaitPage_PreVirtualMeeting(WaitPage):
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_PreVirtualMeeting.html'

    def vars_for_template(player):
        no_dropout = all(p.is_dropout is False for p in player.group.get_players())
        return dict(no_dropout =no_dropout)


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
    if len(waiting_players) >= 3:
        print('about to create a group')
        return waiting_players[:3]


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

class GenInstructions1(Page):
    form_model = 'player'
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
            print('Setting to true in GenInstructions1')
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

        return dict(
            dropouts={
                player.group.get_player_by_id(1).is_dropout,
                player.group.get_player_by_id(2).is_dropout,
                player.group.get_player_by_id(3).is_dropout},
            is_dropout=is_dropout,
            is_dropout1=is_dropout1,
            is_dropout2=is_dropout2,
            is_dropout3=is_dropout3
        )

        return dict(is_dropout=is_dropout)


class GroupWaitPage(WaitPage):
    body_text = 'Please wait until all players in your group have completed the test video meeting.'

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
    timeout_seconds = 600

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


class StudyIntroduction1(Page):
    form_model = 'player'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in StudyIntroduction1')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

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

class PostVVCQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['seeHear']
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
            print('Setting to true in PostVVCQuestionnaire')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def app_after_this_page(player, upcoming_apps):
        if player.seeHear==False:
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True
            for p in player.group.get_players(): p.is_dropout = True
            return 'App09TeamExitThankYou'



class MyWaitPage_TechProblem(WaitPage):
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_TechProblem.html'


    def is_displayed(player):
        player.group_see_hear = player.group_see_hear  and (player.seeHear)
        return player.seeHear == False

    def app_after_this_page(player, upcoming_apps):
        if not player.group_see_hear:
            return 'App09TeamExitThankYou'

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        is_dropout = is_dropout and player.seeHear
        return dict(is_dropout=is_dropout)



class MyWaitPage_PostTechCheck(WaitPage):
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_PostTechCheck.html'

    def is_displayed(player):
        player.group_see_hear = player.group_see_hear and (player.seeHear)
        return player.seeHear == True

    def vars_for_template(player):
        no_dropout = all(p.is_dropout is False and p.group_see_hear is True for p in player.group.get_players())
        return dict(no_dropout =no_dropout,
                    group_see_hear =  player.group_see_hear)


page_sequence = [MyWaitPageStage2Instructions, PartsRoundsGroups, DescriptionVideoCommunication, GenInstructions1, DescriptionVideoCommunication1,
                  MyWaitPage_PreVirtualMeeting, VVC, PostVVCQuestionnaire,MyWaitPage_TechProblem,MyWaitPage_PostTechCheck,
                  StudyIntroduction1, StudyIntroduction2, StudyIntroduction3, Comprehension1, Comprehension2,
                  Comprehension3, Comprehension4]

# Comments from Bella:
# The page sequence needs to be updated to be the following:
# page_sequence = [MyWaitPage_Stage2Instructions (optional add-on for the waiting time above 5 minutes),
#                  PartsRoundsGroups, DescriptionVideoCommunication, GenInstructions1, DescriptionVideoCommunication1,
#                  MyWaitPage_PreVirtualMeeting, VVC, PostVVCQuestionnaire, [TechProblem and/or PostTechCheck],
#                  StudyIntroduction1, StudyIntroduction2, StudyIntroduction3, Comprehension1, Comprehension2,
#                  Comprehension3, Comprehension4]
# IMPORTANT NOTES:
#     - There are now only 3 team members per group.
#     - The DescriptionVideoCommunication page where the team members get to know each other will now last 7, instead
#       of 8 minutes.
#
# NEW NOTES FOR ANUJA FROM BELLA:
#     - I tried to implement the checkbox on page GenInstructions1, but needs to be checked by Anuja (Done).
#     - I tried to implement the two radio buttons on page _templates.global.TechProblem, but need to be checked also.
#     - I also tried to add the two pages PostVVCQuestionnaire and _templates.global.MyWaitPage_TechProblem in their
#       Python files, but also needs to be checked if it was done correctly.