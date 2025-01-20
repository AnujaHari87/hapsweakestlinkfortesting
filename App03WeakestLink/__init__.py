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


class C(BaseConstants):
    NAME_IN_URL = 'App03WeakestLink'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 5
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
    ownDecision = make_field("Please choose one")
    payoff_hypo = models.IntegerField()
    is_dropout = models.BooleanField(
        default=False,
        label='',
        blank=True
    )


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

    @staticmethod
    def live_method(player: Player, data):
        if "ownDecision" in data:
            player.ownDecision = data["ownDecision"]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_num=player.round_number)


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

    def get_template_name(self):
        return 'global/MyWaitPage.html'

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
            p.payoff_hypo = C.ENDOWMENT + (6 * group.groupMin) - (5 * p.ownDecision)

        # Additional logic for round number 5
        if group.round_number == 5:
            print('we are getting here')
            group.randomNumber = random.choice(range(1, 6))
            for p in group.get_players():
                p_past = p.in_round(group.randomNumber)
                g_past = group.in_round(group.randomNumber)
                p.payoff = C.ENDOWMENT + (6 * g_past.groupMin) - (5 * p_past.ownDecision)
                part = p.participant
                part.payoff_ppg = p.payoff
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


class Description(Page):
    form_model = 'player'

    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        if ('is_dropout' in participant.vars):
            print(participant.vars['is_dropout'])
        print('Dropout In Description')
        if 'is_dropout' in participant.vars and participant.vars['is_dropout'] is True:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        if timeout_happened:
            player.ownDecision = 40
            player.participant.vars['is_dropout'] = True
            player.is_dropout = True

        group_matrix_comm = player.session.vars.get('group_matrix')
        player.in_round(player.round_number).group.subsession.set_group_matrix(group_matrix_comm)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_num=player.round_number)


page_sequence = [Description, Decision, CalculatePayoff, Results]
