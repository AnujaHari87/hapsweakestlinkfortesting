import time
import re
import random

from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = '02_Post_Intro'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    nasa_values = dict(
        C1=['Very_low', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Very_high'],
        C2=['Very_Low', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Very_high']
    )

    nasa_values_processed = {
        'C1': [{'value': p, 'label': p.replace('_', ' ').title()} for p in nasa_values['C1']],
        'C2': [{'value': p, 'label': p.replace('_', ' ').title()} for p in nasa_values['C2']]
    }


class Subsession(BaseSubsession):
    waitCount = models.IntegerField(initial=0)


class Group(BaseGroup):
    randomNumberTreatment = models.IntegerField()


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

def make_field5(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label=label,
        widget=widgets.RadioSelect,
    )

def make_field2(label):
    return models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label=label,
        widget=widgets.RadioSelect,
    )

def make_field4(label):
    return models.IntegerField(
        choices=[0,1,2,3],
        label=label,
        widget=widgets.RadioSelect,
    )

def make_field20(label):
    return models.IntegerField(
        choices=[ 1, 2, 3,4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

class Player(BasePlayer):
    self_cons_1 = make_field4('I am always trying to figure myself out.')
    self_cons_2 = make_field4('I think about myself a lot.')
    self_cons_3 = make_field4('I often daydream about myself.')
    self_cons_4 = make_field4('I never take a hard look at myself.')
    self_cons_5 = make_field4('I generally pay attention to my inner feelings.')
    self_cons_6 = make_field4('I am constantly thinking about my reasons for doing things.')
    self_cons_7 = make_field4('I sometimes step back (in my mind) in order to examine myself from a distance.')
    self_cons_8 = make_field4('I am quick to notice changes in my mood.')
    self_cons_9 = make_field4('I know the way my mind works when I work through a problem.')
    self_cons_10 = make_field4('I am concerned about my style of doing things.')
    self_cons_11 = make_field4('I care a lot about how I present myself to others.')
    self_cons_12 = make_field4('I am self-conscious about the way I look.')
    self_cons_13 = make_field4('I usually worry about making a good impression.')
    self_cons_14 = make_field4('Before I leave my house. I check how I look.')
    self_cons_15 = make_field4('I am concerned about what other people think of me.')
    self_cons_16 = make_field4('I am usually aware of my appearance.')
    self_cons_17 = make_field4('It takes me time to get over my shyness in new situations.')
    self_cons_18 = make_field4('It is hard for me to work when someone is watching me.')
    self_cons_19 = make_field4('I get embarrassed very easily.')
    self_cons_20 = make_field4('It is easy for me to talk to strangers.')
    self_cons_21 = make_field4('I feel nervous when I speak in front of a group.')
    self_cons_22 = make_field4('Large groups make me nervous.')

    risk = make_field2("")
    holidays_1 = make_field('Sun, sea, and beach vacation.')
    holidays_2 = make_field('Party vacation.')
    holidays_3 = make_field('Winter sports vacation.')
    holidays_4 = make_field('City trip.')
    holidays_5 = make_field('Backpacking vacation.')
    holidays_6 = make_field('Excursion.')
    holidays_7 = make_field('Camping vacation.')
    holidays_8 = make_field('Cruise vacation.')
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


    seeHear = models.IntegerField(blank=True, choices=[[0, '0'], [1, '1'], [2, '2']], label='',
                                         attrs={"invisible": True},  default = 2)
    attentionCheck = models.IntegerField(blank=True, choices=[[0, '0'], [1, '1']], label='',
                                  attrs={"invisible": True}, default=0)

    groupExit = models.BooleanField(
        default=False,
        label='',
        blank=True
    )
    treatmentNumber = models.IntegerField(initial=0, blank=True)

    nasatlx1 = make_field20('How mentally demanding was the task?')
    nasatlx2 = make_field20('How hurried or rushed was the pace of the task?')

    vcSelfFocAtt1 = make_field5('I was focusing on what I would say or do next.')
    vcSelfFocAtt2 = make_field5('I was focusing on the impression I was making on the other persons.')
    vcSelfFocAtt3 = make_field5('I was focusing on my level of anxiety.')
    vcSelfFocAtt4 = make_field5('I was focusing on my internal bodily reactions (for example, heart rate).')
    vcSelfFocAtt5 = make_field5('I was focusing on past social failures.')


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

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            print('In MyWaitPageStage2Instructions')
            player.is_dropout = True
            return 1  # instant timeout, 1 second
        else:
            return 15 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting dropout to true in MyWaitPageStage2Instructions')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    #def app_after_this_page(player: Player, upcoming_apps):
     #   if player.is_dropout:
      #      return 'App08DropoutThankYou'


class MyWaitPage_PreVirtualMeeting(WaitPage):
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_PreVirtualMeeting.html'

    def vars_for_template(player):
        no_dropout = all(p.is_dropout is False for p in player.group.get_players())
        return dict(no_dropout =no_dropout)

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


    @staticmethod
    def after_all_players_arrive(group: Group):
        import time
        start_time = time.time()
        group.session.vars['group_matrix'] = group.subsession.get_group_matrix()
        end_time = time.time()
        duration = end_time - start_time
        print(f"after_all_players_arrive took {duration} seconds")
        group.randomNumberTreatment = random.choice(range(1, 4))
        for p in group.get_players():
            p.treatmentNumber = group.randomNumberTreatment

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts>0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'

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

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'


def waiting_too_long(player):
    participant = player.participant

    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.vars['wait_page_arrival'] > 15 * 60


def group_by_arrival_time_method(subsession, waiting_players):
    print("number of players waiting:", len(waiting_players))

    for player in waiting_players:
        player.waitpage_too_long = waiting_too_long(player)
        if (player.waitpage_too_long):
            player.payoff = 50
          #  player.is_dropout = True
            player.participant.payoff_ppg = 50

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

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'

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

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'


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
    
    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            print('In VVC0')
            player.is_dropout = True
            return 1  # instant timeout, 1 second
        else:
            return 3 * 60


    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'



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

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'

class PreVideoQuestionnaire1(Page):
    form_model = 'player'
    form_fields = [
        'self_cons_1', 'self_cons_2', 'self_cons_3', 'self_cons_4', 'self_cons_5',
        'self_cons_6', 'self_cons_7', 'self_cons_8', 'self_cons_9', 'self_cons_10',
        'self_cons_11'
    ]

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in PreVideoQuestionnaire1')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'

class PreVideoQuestionnaire1a(Page):
    form_model = 'player'
    form_fields = [
       'self_cons_12', 'self_cons_13', 'self_cons_14', 'self_cons_15',
        'self_cons_16', 'self_cons_17', 'self_cons_18', 'self_cons_19', 'self_cons_20',
        'self_cons_21', 'self_cons_22'
    ]

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in PreVideoQuestionnaire1a')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts > 0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'

class PreVideoQuestionnaire2(Page):
        form_model = 'player'
        form_fields = ['risk']
        def get_timeout_seconds(player):
            participant = player.participant
            if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
                return 1  # instant timeout, 1 second
            else:
                return 5 * 60

        def before_next_page(player, timeout_happened):
            if timeout_happened:
                print('Setting to true in PreVideoQuestionnaire2')
                player.participant.vars['is_dropout'] = True
                player.is_dropout = True

        def vars_for_template(player: Player):
            if 'is_dropout' in player.participant.vars:
                is_dropout = player.participant.vars['is_dropout']
            else:
                is_dropout = False
            return dict(is_dropout=is_dropout)

        def app_after_this_page(player: Player, upcoming_apps):
            num_dropouts = sum(p.is_dropout for p in player.group.get_players())
            if num_dropouts > 0:
                for p in player.group.get_players():
                    p.payoff = 75.00
                    p.participant.payoff_ppg = 75.00
                return 'App10TeamExitThankYou'

class WaitBeforeVideo(WaitPage):
    after_all_players_arrive = goal_wait_for_all
    title_text = 'Please wait until all players have entered the video meeting.'



class VVC(Page):
    form_model = 'player'
    timeout_seconds = 540
    form_fields = ['seeHear', 'treatmentNumber','attentionCheck']

    @staticmethod
    def vars_for_template(player: Player):
        optInConsent = player.participant.vars['optInConsent']

        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(optInConsent=optInConsent,
                    is_dropout=is_dropout)


    def is_displayed(player: Player):
      num_dropouts = sum(p.is_dropout for p in player.group.get_players())
      return num_dropouts < 2

    def app_after_this_page(player: Player, upcoming_apps):
        num_dropouts = sum(p.is_dropout for p in player.group.get_players())
        if num_dropouts>0:
            for p in player.group.get_players():
                p.payoff = 75.00
                p.participant.payoff_ppg = 75.00
            return 'App10TeamExitThankYou'

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



class MyWaitPagePostVVC(WaitPage):
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def after_all_players_arrive(group: Group):
        groupReady = all(p.seeHear is not None and (p.seeHear ==1 or p.seeHear ==2) for p in group.get_players())
        groupAttentionCheck = all(p.attentionCheck is not None and (p.attentionCheck ==1) for p in group.get_players())

        for p in group.get_players():
            p.groupExit = not groupReady or not groupAttentionCheck
       
    def app_after_this_page(player: Player, upcoming_apps):
            if player.groupExit:
                player.payoff = 150
                player.participant.payoff_ppg = 150
                return 'App09TeamExitThankYou'

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            print('In MyWaitPagePostVVC')
            player.is_dropout = True
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in MyWaitPagePostVVC')
            print('Setting dropout to true in MyWaitPagePostVVC')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True
            player.payoff = 0

    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout)


class MyWaitPage_PostTechCheck(WaitPage):
    body_text = "Please wait until your team members arrive."

    @staticmethod
    def get_template_name():
        # Use a standard oTree template and modify it with JavaScript
        return 'global/MyWaitPage_PostTechCheck.html'

    def is_displayed(player):
        return player.groupExit == False

    def vars_for_template(player):
        no_dropout = all(p.is_dropout is False for p in player.group.get_players())
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(is_dropout=is_dropout,no_dropout =no_dropout)

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            print('In MyWaitPagePostVVC')
            player.is_dropout = True
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting dropout to true in MyWaitPage_PostTechCheck')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True


class VideoConSelfFocAttn(Page):
    form_model = 'player'
    form_fields = ['vcSelfFocAtt1','vcSelfFocAtt2', 'vcSelfFocAtt3', 'vcSelfFocAtt4', 'vcSelfFocAtt5']

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
            print('Setting to true in VideoConSelfFocAttn')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True


class NasaTLX(Page):
    form_model = 'player'
    form_fields = ['nasatlx1','nasatlx2']

    @staticmethod
    def vars_for_template(player: Player):
        if 'is_dropout' in player.participant.vars:
            is_dropout = player.participant.vars['is_dropout']
        else:
            is_dropout = False
        return dict(
            C.nasa_values_processed,
            is_dropout=is_dropout
        )

    def get_timeout_seconds(player):
        participant = player.participant
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('Setting to true in NasaTLX')
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True



class DescriptionThankYou(Page):
    form_model = 'player'

    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        if ('is_dropout' in participant.vars):
            print(participant.vars['is_dropout'])
        print('Dropout In DescriptionThankYou')
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True


page_sequence = [MyWaitPageStage2Instructions, PartsRoundsGroups, PreVideoQuestionnaire1, PreVideoQuestionnaire1a,
                 PreVideoQuestionnaire2, DescriptionVideoCommunication, GenInstructions1, DescriptionVideoCommunication1,VVC0,
                  MyWaitPage_PreVirtualMeeting, VVC, MyWaitPagePostVVC,MyWaitPage_PostTechCheck,VideoConSelfFocAttn, NasaTLX,
                  StudyIntroduction1, StudyIntroduction2, StudyIntroduction3, Comprehension1, Comprehension2,
                  Comprehension3, Comprehension4, DescriptionThankYou]

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