from otree.api import *
import random

c = cu

doc = ''


def make_field(label):
    return models.IntegerField(
        choices=[0, 10, 20, 30, 40],
        label=label,
        widget=widgets.RadioSelect,
    )
def make_field_h(label):
    return models.IntegerField(
        choices=[0, 10, 20, 30, 40],
        label=label,
        widget=widgets.RadioSelectHorizontal
    )

def make_field7(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label=label,
        widget=widgets.RadioSelectHorizontal
    )


class C(BaseConstants):
    NAME_IN_URL = 'App03WeakestLink'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
    ENDOWMENT = 200


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    groupMin = models.IntegerField(
        min=0, max=40, initial=40
    )
    print('recreates group')
    randomNumber = models.IntegerField()


class Player(BasePlayer):
    ownDecision = make_field("") # ANUJA (Done): There is no longer any "Please choose one" in the texts, so I just left some empty quotation marks, if that's OK?
    payoff_hypo = models.IntegerField()
    is_dropout = models.BooleanField(
        default=False,
        label='',
        blank=True
    )
    belief1_1 = make_field_h("What is your best guess on the minimum hours that your team members contributed to Project A in this round?")
    belief2_1 = make_field7("How confident are you in your guess? <br/>(1: not all, 7: very much so)")
    belief1_10 = make_field_h("What is your best guess on the minimum hours that your team members contributed to Project A in this round?")
    belief2_10 = make_field7("How confident are you in your guess? <br/>(1: not all, 7: very much so)")
    # ANUJA: I'm not sure where in the code exactly, but the calculation of the payout for the participant will need to be changed to match the new compensation table.


class Decision(Page):
    form_model = 'player'
    form_fields = ['ownDecision']

    @staticmethod
    def get_timeout_seconds(player):
        if ('is_dropout' in player.participant.vars):
            print(player.participant.vars['is_dropout'])
        print('In Decision')
        if 'is_dropout' in player.participant.vars and player.participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 3 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.ownDecision = 40
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

        group_matrix_comm = player.session.vars.get('group_matrix')
        player.in_round(player.round_number).group.subsession.set_group_matrix(group_matrix_comm)

    @staticmethod
    def live_method(player: Player, data):
        if "ownDecision" in data:
            player.ownDecision = data["ownDecision"]

    @staticmethod
    def vars_for_template(player: Player):
        dropout_count = sum(1 for p in player.group.get_players() if p.participant.vars.get('is_dropout'))
        return dict(round_num=player.round_number, dropout_count = dropout_count)

class Beliefs1(Page):
    form_model = 'player'
    form_fields = ['belief1_1','belief2_1']

    def is_displayed(player):
        return player.group.round_number == 1

    @staticmethod
    def get_timeout_seconds(player):
        if ('is_dropout' in player.participant.vars):
            print(player.participant.vars['is_dropout'])
        print('In Decision')
        if 'is_dropout' in player.participant.vars and player.participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 3 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

        group_matrix_comm = player.session.vars.get('group_matrix')
        player.in_round(player.round_number).group.subsession.set_group_matrix(group_matrix_comm)


    @staticmethod
    def vars_for_template(player: Player):
        dropout_count = sum(1 for p in player.group.get_players() if p.participant.vars.get('is_dropout'))
        return dict(round_num=player.round_number, dropout_count = dropout_count,horizontal_radio_buttons=True)


class Beliefs10(Page):
    form_model = 'player'
    form_fields = ['belief1_10', 'belief2_10']

    def is_displayed(player):
        return player.group.round_number == 10

    @staticmethod
    def get_timeout_seconds(player):
        if ('is_dropout' in player.participant.vars):
            print(player.participant.vars['is_dropout'])
        print('In Decision')
        if 'is_dropout' in player.participant.vars and player.participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 3 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

        group_matrix_comm = player.session.vars.get('group_matrix')
        player.in_round(player.round_number).group.subsession.set_group_matrix(group_matrix_comm)

    @staticmethod
    def vars_for_template(player: Player):
        dropout_count = sum(1 for p in player.group.get_players() if p.participant.vars.get('is_dropout'))
        return dict(round_num=player.round_number, dropout_count=dropout_count)

class CalculatePayoff(WaitPage):
    body_text = "Please wait until your team members have made their decision."

    def vars_for_template(self):
        # Get the number of players who have arrived (decided) in the group
        arrived_players = [p for p in self.group.get_players() if p.field_maybe_none('ownDecision') is not None]
        waiting_count = len(arrived_players)

        return {
            'reload_interval': 5000,  # 5000 milliseconds = 5 seconds
            'waiting_count': waiting_count
        }

    # ANUJA: Had to split the page MyWaitPage in two, because the two Waiting Pages of this section are now different.
    # Named the 1st one “MyWaitPage_Description” and added this in the following snippet of code (hope that’s correct):
    def get_template_name(player):
        if player.group.round_number == 1:
            return 'global/MyWaitPage_Description.html'
        else:
            return 'global/MyWaitPage_Decision.html'

    def js_vars(self):
        return {
            'reload_interval': 5000  # 5000 milliseconds = 5 seconds
        }

    @staticmethod
    def get_timeout_seconds(player):
        if ('is_dropout' in player.participant.vars):
            print(player.participant.vars['is_dropout'])
        print('In CalculatePayoff')
        if 'is_dropout' in player.participant.vars and player.participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 3 * 60

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.ownDecision = 40
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

    @staticmethod
    def after_all_players_arrive(group: Group):
        # Calculate group minimum and individual payoffs
        group.groupMin = min(p.ownDecision for p in group.get_players())

        for p in group.get_players():
            p.payoff_hypo = C.ENDOWMENT + (10 * group.groupMin) - (5 * p.ownDecision)

        # Additional logic for round number 5
        if group.round_number == 10:
            print('we are getting here')
            group.randomNumber = random.choice(range(1, 11))
            for p in group.get_players():
                if p.is_dropout:
                    p.payoff = 0
                    part = p.participant
                    part.payoff_ppg = p.payoff
                    part.payoff_round = group.randomNumber
                else:
                    p_past = p.in_round(group.randomNumber)
                    g_past = group.in_round(group.randomNumber)
                    p.payoff = C.ENDOWMENT + (10 * g_past.groupMin) - (5 * p_past.ownDecision) + 300
                    part = p.participant
                    part.payoff_ppg = p.payoff - 300
                    part.payoff_round = group.randomNumber


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        dropout_count = sum(1 for p in group.get_players() if p.participant.vars.get('is_dropout'))

        return dict(
            groupMin=player.group.groupMin,
            payoff=player.payoff_hypo,
            endowment=C.ENDOWMENT,
            ownDecision=player.ownDecision,
            round_num=player.round_number,
            dropout_count=dropout_count
        )

    @staticmethod
    def get_timeout_seconds(player):
        if 'is_dropout' in player.participant.vars:
            print(player.participant.vars['is_dropout'])
        print('In Results')
        if 'is_dropout' in player.participant.vars and player.participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 3 * 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.ownDecision = 40
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True




page_sequence = [Decision, CalculatePayoff, Beliefs1, Beliefs10, Results]


# NOTES FOR ANUJA FROM BELLA:
#      - Created a MyWaitPage_Description to go after the Description page above, and a MyWaitPage_Decision to go after
#        the decision page above. You might need to please double check that I connected the pages correctly.
#        PS: The only difference in the text is in the first sentence: "finished with reading the instructions and
#            answering the comprehension questions" in page MyWaitPage_Description, and it's changed to "finished with
#            their decision" in the page MyWaitPage_Decision. So perhaps alternatively, this could maybe even be a
#            variable if it's easier to implement?