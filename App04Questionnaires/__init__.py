from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'App04Questionnaires'
    players_per_group = 3
    num_rounds = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label=label,
        widget=widgets.RadioSelect,
    )


def make_field7(label):
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


def make_field3(label):
    return models.IntegerField(
        choices=[0, 5, 10, 15, 20, 25, 30],
        label=label,
        widget=widgets.RadioSelect,
    )


def make_field4(label):
    return models.IntegerField(
        choices=[0, 1, 2, 3],
        label=label,
        widget=widgets.RadioSelect,
    )

def make_field21(label):
    return models.IntegerField(
        choices=[ 1, 2, 3,4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )
def make_image_data(image_names):
    return [dict(name=name, path='images/{}'.format(name)) for name in image_names]


class Player(BasePlayer):
    team_cohesion = models.StringField()
    payoff_quests = models.IntegerField()
    attention_check = models.IntegerField(initial=0)
    social_cohesion_short = make_field7('')


    negative_rp_1 = make_field2(
        'How willing are you to punish someone who treats you unfairly, even if there may be costs for you?')
    negative_rp_2 = make_field2(
        'How willing are you to punish someone who treats others unfairly, even if there may be costs for you?')
    attention2 = make_field('Please select the option "4" to show that you are answering the questions attentively.')
    attention1 = make_field('Please select the option "1" to show that you are answering the questions attentively.')

    positive_rp_1 = make_field2('When someone does me a favor, I am willing to return it.')
    negative_rp_3 = make_field2(
        'If I am treated very unjustly, I will take revenge at the first occasion, even if there is a cost to do so.')
    attention3 = make_field2('Please select the option "3" to show that you are answering the questions attentively.')
    positive_rp_2 = make_field3("")

    big5_1 = make_field(
        'I see myself as someone who is reserved.')
    big5_2 = make_field(
        'I see myself as someone who is generally trusting.')
    big5_3 = make_field(
        'I see myself as someone who tends to be lazy.')
    big5_4 = make_field(
        'I see myself as someone who is relaxed, handles stress well.')
    big5_5 = make_field(
        'I see myself as someone who has few artistic interests.')
    big5_6 = make_field(
        'I see myself as someone who is outgoing, sociable.')
    big5_7 = make_field(
        'I see myself as someone who tends to find fault with others.')
    big5_8 = make_field(
        'I see myself as someone who does a thorough job.')
    big5_9 = make_field(
        'I see myself as someone who gets nervous easily.')
    big5_10 = make_field(
        'I see myself as someone who has an active imagination.')

    age = models.IntegerField(label='What is your <strong>age</strong> (years)? <br/>(Please enter a valid age between 18 and 65.)', min=18, max=66, error_messages = {
        'min_value': 'Please enter an age of at least 18.',
        'max_value': 'Please enter an age of 65 or less.',
        'invalid': 'Please enter a valid age between 18 and 65.',
    }
    )
    gender = models.IntegerField(label='<br>Which <strong>gender</strong> do you identify with?', blank=False,
                                 choices=[[1, 'male'], [2, 'female'], [3, 'other']])
    ethnicity = models.IntegerField(
        label="<br>Which of the following <b>ethnicities</b> best describes you?<br/>", blank=False,
        choices=[[1, 'White'], [2, 'Black'], [3, 'Asian'],
                 [4, 'Mixed'], [5, 'Other'], [6, 'Prefer not to say']])
    
    education = models.IntegerField(
        label="<br>What is the highest level of <b>education</b> you have completed?</br>",
        choices=[[1, 'less than High School'], [2, 'High School/GED'], [3, 'Some College'],
                 [4, '2-year College degree'], [5, '4-year College degree'],
                 [6, 'Master’s degree'], [7, 'Doctoral degree or Professional Degree (JD, MD)']])

    prolificdays_month = models.IntegerField(
        label="<br>How many days per month do you typically use Prolific?</br> (Please enter a valid number between 0 and 31.)",
        min=0, max=31)
    prolifichours_day = models.IntegerField(
        label="<br>On the days when you use Prolific, how many hours do you typically spend on it?</br> (Please enter a valid number between 1 and 24.)",
        min=1, max=24)
    prolificprimary_income = models.IntegerField(label="Is Prolific your primary source of income?", blank=False,
                                                 choices=[[1, 'Yes'], [2, 'No'], [3, 'Other, please specify']])
    other_income_specify = models.StringField(
        blank=True,
        label=""
    )
    us_state = models.StringField(
        choices=[
            [1, 'Alabama'], [2, 'Alaska'], [3, 'Arizona'], [4, 'Arkansas'],
            [5, 'California'], [6, 'Colorado'], [7, 'Connecticut'], [8, 'Delaware'],
            [9, 'Florida'], [10, 'Georgia'], [11, 'Hawaii'], [12, 'Idaho'],
            [13, 'Illinois'], [14, 'Indiana'], [15, 'Iowa'], [16, 'Kansas'],
            [17, 'Kentucky'], [18, 'Louisiana'], [19, 'Maine'], [20, 'Maryland'],
            [21, 'Massachusetts'], [22, 'Michigan'], [23, 'Minnesota'], [24, 'Mississippi'],
            [25, 'Missouri'], [26, 'Montana'], [27, 'Nebraska'], [28, 'Nevada'],
            [29, 'New Hampshire'], [30, 'New Jersey'], [31, 'New Mexico'], [32, 'New York'],
            [33, 'North Carolina'], [34, 'North Dakota'], [35, 'Ohio'], [36, 'Oklahoma'],
            [37, 'Oregon'], [38, 'Pennsylvania'], [39, 'Rhode Island'], [40, 'South Carolina'],
            [41, 'South Dakota'], [42, 'Tennessee'], [43, 'Texas'], [44, 'Utah'],
            [45, 'Vermont'], [46, 'Virginia'], [47, 'Washington'], [48, 'West Virginia'],
            [49, 'Wisconsin'], [50, 'Wyoming']
        ],
        label="<br>Which U.S state do you currently live in? <br/>"
    )
    other_gender_specify = models.StringField(
        blank=True,
        label=""
    )
    other_ethnicity_specify = models.StringField(
        blank=True,
        label=""
    )
    interperstrust1 = make_field('I am convinced that most people have good intentions.')
    interperstrust2 = make_field('You can\'t rely on anyone these days.')
    interperstrust3 = make_field('In general, people can be trusted.')
    appearance = make_field2 ('How satisfied are you with your appearance right now?')





# PAGES


def age_error_message(player: Player, value):
    if value < 18 or value > 66:
            return "You need to be between 18 years and 66 years to participate."
    return None

class IntroPart3(Page):
    form_model = 'player'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group_matrix_comm = player.session.vars.get('group_matrix')
        player.in_round(1).group.subsession.set_group_matrix(group_matrix_comm)


class Quest01(Page):
    form_model = 'player'
    form_fields = ['team_cohesion']

    def vars_for_template(self: Player):
        image_names = [
            'Picture1.png',
            'Picture2.png',
            'Picture3.png',
            'Picture4.png',
            'Picture5.png',
            'Picture6.png',
            'Picture7.png'
        ]
        return dict(image_data=make_image_data(image_names))


class Quest02(Page):
    form_model = 'player'
    form_fields = ['social_cohesion_short']
    # usability, satisfaction, intention to use


class Quest03(Page):
    form_model = 'player'
    form_fields = ['interperstrust1','attention2','interperstrust2','interperstrust3' ]

    def before_next_page(player: Player, timeout_happened):
        if player.attention2 != 4:
            player.attention_check += 1



class Quest05(Page):
    form_model = 'player'
    form_fields = ['positive_rp_1', 'negative_rp_3' ]




class Quest04(Page):
    form_model = 'player'
    form_fields = [ 'negative_rp_1', 'negative_rp_2']




class Quest07(Page):
    form_model = 'player'
    form_fields = ['positive_rp_2']


class Quest07a(Page):
    form_model = 'player'
    form_fields = ['big5_1', 'big5_2', 'big5_3', 'big5_4', 'big5_5', 'attention1',
                   'big5_6', 'big5_7', 'big5_8', 'big5_9', 'big5_10' ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention1 != 1:
            player.attention_check += 1


class Quest08(Page):
    form_model = 'player'
    form_fields = ['appearance']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention_check <= 1:
            player.payoff_quests = 100
        else:
            player.payoff_quests = 0




class QuestDemographics(Page):
    form_model = 'player'
    form_fields = [ 'prolificdays_month',
                   'prolifichours_day', 'prolificprimary_income', 'other_income_specify',
                     'us_state',  'gender', 'age', 'education', 'ethnicity', 'other_ethnicity_specify', 'other_gender_specify']


class QuestEnd(Page):

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        return dict(
            total_payoff_ecu=(200 + participant.payoff_ppg),
            payoff_bonus = (participant.payoff_ppg * 0.02),
            total_payoff=6 + (participant.payoff_ppg) * 0.02
        )


page_sequence = [IntroPart3, Quest01, Quest02, Quest03,  Quest05, Quest04, Quest07, Quest07a, Quest08, QuestDemographics, QuestEnd]
