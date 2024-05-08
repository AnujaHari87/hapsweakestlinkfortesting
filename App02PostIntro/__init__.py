from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = '01_Post_Intro'
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


def make_image_data(image_names):
    return [dict(name=name, path='images/{}'.format(name)) for name in image_names]


def make_field(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label=label,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    team_cohesion = models.StringField()
    holidays_1 = make_field('Sun, Sea, and Beach holiday.')
    holidays_2 = make_field('Party holiday.')
    holidays_3 = make_field('Winter sports holiday.')
    holidays_4 = make_field('City trip.')
    holidays_5 = make_field('Backpacking holiday.')
    holidays_6 = make_field('Excursion.')
    holidays_7 = make_field('Camping holiday.')
    holidays_8 = make_field('Cruise vacation.')
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


def comprehension1_error_message(player: Player, value):
    if value != 200:
        player.comp1_check += 1
        return "Unfortunately, that's incorrect. The correct answer is <strong>200</strong>."


def comprehension2_error_message(player: Player, value):
    if value != 160:
        player.comp2_check += 1
        return "Unfortunately, that's incorrect. The correct answer is <strong>160</strong>."


def comprehension3_error_message(player: Player, value):
    if value != 180:
        player.comp3_check += 1
        return "Unfortunately, that's incorrect. The correct answer is <strong>180</strong>."


def comprehension4a_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."


def comprehension4b_error_message(player: Player, value):
    if value:
        player.comp4_check += 1
        return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."


def comprehension4c_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."


class DescriptionVideoCommunication(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        import random
        holidays = ['holidays_1', 'holidays_2', 'holidays_3', 'holidays_4',
                    'holidays_5', 'holidays_6', 'holidays_7']
        random.shuffle(holidays)
        return holidays


class WaitBeforeVideo(WaitPage):
    after_all_players_arrive = goal_wait_for_all
    title_text = 'Please wait till all players have entered the meeting.'


class VVC(Page):
    form_model = 'group'
    timeout_seconds = 60


class EndVVC(Page):
    form_model = 'player'
    form_fields = ['team_cohesion']

    def vars_for_template(self: Player):
        image_names = [
            'Inclusion1.jpg',
            'Inclusion2.jpg',
            'Inclusion3.jpg',
            'Inclusion4.jpg',
            'Inclusion5.jpg',
            'Inclusion6.jpg'
        ]
        return dict(image_data=make_image_data(image_names))


class StudyIntroduction1(Page):
    form_model = 'player'


class StudyIntroduction2(Page):
    form_model = 'player'


class StudyIntroduction3(Page):
    form_model = 'player'
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4a', 'comprehension4b',
                   'comprehension4c']


page_sequence = [DescriptionVideoCommunication, WaitBeforeVideo, VVC, EndVVC, StudyIntroduction1, StudyIntroduction2,
                 StudyIntroduction3]
