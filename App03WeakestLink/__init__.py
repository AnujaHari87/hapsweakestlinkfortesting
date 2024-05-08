from otree.api import *
import random

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'App03WeakestLink'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 5
    ENDOWMENT = 200


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    groupMin = models.IntegerField(
        min=0, max=40, initial=40
    )

    randomNumber = models.IntegerField()




def wait_for_all(group: Group):
    pass



class Player(BasePlayer):
    ownDecision = models.IntegerField(
        blank=False, min=0, max=40
    )
    payoff_hypo = models.IntegerField()


class Instructions1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Decision(Page):
    @staticmethod
    def live_method(player: Player, data):
        if "ownDecision" in data:
            player.ownDecision = data["ownDecision"]
            group = player.group
            if player.ownDecision < group.groupMin:
                group.groupMin = player.ownDecision

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_num=player.round_number)


class CalculatePayoff(WaitPage):
    body_text = "Please wait until your team members have made their decision."

    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            p.payoff_hypo = C.ENDOWMENT + (6 * group.groupMin) - (5 * p.ownDecision)
        if group.round_number == 5:
            print('we are getting here')
            group.randomNumber = random.choice(range(1, 6))
            for p in group.get_players():
                p_past = p.in_round(group.randomNumber)
                g_past = group.in_round(group.randomNumber)
                p.payoff = C.ENDOWMENT + (6 * g_past.groupMin) - (5 * p_past.ownDecision)
                part = p.participant


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            groupMin=player.group.groupMin,
            payoff=player.payoff_hypo,
            endowment=C.ENDOWMENT,
            ownDecision=player.ownDecision,
            round_num=player.round_number
        )


page_sequence = [Decision, CalculatePayoff, Results]
