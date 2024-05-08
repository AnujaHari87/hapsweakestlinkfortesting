from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'App04Questionnaires'
    players_per_group = 4
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


def make_field2(label):
    return models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label=label,
        widget=widgets.RadioSelect,
    )


def make_field3(label):
    return models.IntegerField(
        choices=[5, 10, 15, 20, 25, 30],
        label=label,
        widget=widgets.RadioSelect,
    )


def make_field4(label):
    return models.IntegerField(
        choices=[0, 1, 2, 3],
        label=label,
        widget=widgets.RadioSelect,
    )


def make_image_data(image_names):
    return [dict(name=name, path='images/{}'.format(name)) for name in image_names]


class Player(BasePlayer):
    payoff_quests = models.IntegerField()
    attention_check = models.IntegerField(initial=0)
    team_cohesion = models.StringField()
    social_cohesion_1 = make_field('I felt accepted by my team members.')
    social_cohesion_2 = make_field('I could trust my team members.')
    social_cohesion_3 = make_field('The members of my team liked each other.')
    social_cohesion_4 = make_field('The members of my team made an effort to understand the opinions of others.')
    social_cohesion_5 = make_field(
        'The members of my team seemed to make an effort to behave in a way that is acceptable to others.')
    social_cohesion_6 = make_field('The members of my team disclosed personal information or feelings.')
    attention1 = make_field(
        'Please select the option "strongly disagree" to show that you are answering the questions attentively.')

    risk = make_field2('Are you generally a risk-taking person or do you try to avoid risks?')

    time_1 = make_field2(
        'How much would you be willing to give up on something that benefits you today in order to benefit more in the future?')
    negative_rp_1 = make_field2(
        'How much would you be willing to punish someone who treated YOU unfairly, even if this would have negative consequences for you?')
    negative_rp_2 = make_field2(
        'How much would you be willing to punish someone who treated OTHERS unfairly, even if this would incur costs for you?')
    altruism_1 = make_field2(
        'How much would you be willing to give for a good cause, without expecting anything in return?')
    attention2 = make_field2('Please select the option "7" to show that you are answering the questions attentively.')

    positive_rp_1 = make_field2('If someone does me a favor, I am willing to reciprocate.')
    negative_rp_3 = make_field2(
        'If I am treated very unfairly, I will seek revenge at the first opportunity, even if it costs me to do so.')
    trust_1_positive = make_field2('I am convinced that most people have good intentions.')
    trust_2_negative = make_field2("You can't rely on anyone nowadays.")
    trust_3_positive = make_field2('In general, people can be trusted.')
    math = make_field2('I am good at mathematics.')
    time_2 = make_field2('I tend to procrastinate tasks, even though I know it would be better to do them right away.')
    attention3 = make_field2('Please select the option "3" to show that you are answering the questions attentively.')
    positive_rp_2 = make_field3("")
    altruism_2 = models.IntegerField(label="", min=0, max=1000)
    collective_orientation_1_p = make_field("I find working on team projects very satisfying.")
    collective_orientation_2_n = make_field(
        "I would rather take action on my own than to wait around for others' input.")
    collective_orientation_3_n = make_field(
        "I prefer to complete a task from beginning to end with no assistance from others.")
    collective_orientation_4_p = make_field("Teams usually work very effectively.")
    collective_orientation_5_n = make_field(
        "I think it is usually better to take the bull by the horns and do something yourself, rather than to wait for input from others.")
    collective_orientation_6_n = make_field("For most tasks, I would rather work alone than as part of a group.")
    collective_orientation_7_n = make_field(
        "I find it easy to negotiate with others who hold a different viewpoint than I hold.")
    collective_orientation_8_n = make_field("I can usually perform better when I work on my own.")
    collective_orientation_9_n = make_field(
        "I always ask for more information from others before making any important decision.")
    collective_orientation_10_n = make_field(
        "I find that it is often more productive to work on my own than with others.")
    collective_orientation_11_n = make_field(
        "When solving a problem, it is very important to make your own decision and stick by it.")
    collective_orientation_12_n = make_field(
        "If I disagree with other team members, I tend to go with my own gut feelings.")
    collective_orientation_13_n = make_field(
        "When I have a different opinion than another team member, I usually stick to my own opinion.")
    collective_orientation_14_n = make_field(
        "It is important to stick to your own decisions, even when others around you are trying to get you to change.")
    collective_orientation_15_n = make_field(
        "When others disagree, it is important to hold one's own ground and not give in.")
    attention4 = make_field(
        'Please select the option "strongly agree" to show that you are answering the questions attentively.')
    psychological_safety_1 = make_field('I am not afraid to be myself during the video meeting.')
    psychological_safety_2 = make_field('I am afraid to express my opinion in the meeting.')
    psychological_safety_3 = make_field('There is a threatening atmosphere in the meeting.')
    psychological_availability_1 = make_field(
        'I am confident that I am able to manage competing demands in a meeting.')
    psychological_availability_2 = make_field(
        'I am confident that I am able to deal with problems that arise in the meeting.')
    psychological_availability_3 = make_field(
        'I am confident that I am can think clearly in the meeting.')
    psychological_availability_4 = make_field(
        'I am confident that I am able to show the right emotions in the meeting.')
    psychological_availability_5 = make_field(
        'I am confident that I can cope with the physical demands of the meeting.')

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

    engagement_1 = make_field('In the meeting I am full of exuberant energy.')
    engagement_2 = make_field('The meeting is useful and meaningful.')
    engagement_3 = make_field('While I am in the meeting, time flies by.')
    engagement_4 = make_field('I feel fit and energetic during the meeting.')
    engagement_5 = make_field('I am enthusiastic about my meeting.')
    engagement_6 = make_field('While I am in the meeting, I forget everything around me.')
    engagement_7 = make_field('The meeting inspires me.')
    engagement_8 = make_field('When I get up in the morning, I look forward to my meetings.')
    engagement_9 = make_field('I feel happy when I work intensively during the meeting.')
    engagement_10 = make_field('I am proud of my work in the meeting.')
    engagement_11 = make_field('I am completely absorbed in my work in the meeting.')
    engagement_12 = make_field('When I am in the meeting, I can stay in it for a very long tine.')
    engagement_13 = make_field('The meeting is a challenge for me.')
    engagement_14 = make_field('The meeting carries me away.')
    engagement_15 = make_field('I am mentally very resilient in the meeting.')
    engagement_16 = make_field('I find it difficult to detach myself from the me.')
    engagement_17 = make_field('I always persevere in the meeting, even when things are not going so well.')
    engagement_18 = make_field(
        'Completing my task in the meeting is so engrossing that I forget everything else.')
    engagement_19 = make_field('I often think about other things when I am in the meeting.')
    engagement_20 = make_field('I am rarely distracted when I am in the meeting.')
    engagement_21 = make_field('Time passes quickly when I am in the meeting.')
    engagement_22 = make_field('I put a lot of effort into the meeting.')
    engagement_23 = make_field('I am excited when I do well in my meeting.')
    engagement_24 = make_field('I often feel emotionally detached from the meeting.')
    engagement_25 = make_field('My own feelings depend on how well I do in the meeting.')
    engagement_26 = make_field('I expend a lot of energy to get through the meeting.')
    engagement_27 = make_field('I stay until the work in the meeting is done.')
    engagement_28 = make_field('I avoid working overtime in the meeting whenever possible.')
    engagement_29 = make_field('I take work home from the meeting to complete it.')
    engagement_30 = make_field('I avoid working too hard in the meeting.')
    age = models.IntegerField(label='Please enter your <strong>age</strong>.', min=18, max=65)
    gender = models.IntegerField(label='<br>Please enter your <strong>gender</strong>.',
                                 choices=[[1, 'male'], [2, 'female'], [3, 'transgender'], [4, 'non-binary'],
                                          [5, 'prefer not to say']])
    ethnicity = models.IntegerField(
        label="<br>Please indicate which <strong>ethnicity</strong> you would <u>most likely</u> identify with.",
        choices=[[1, 'Asian or Pacific Islander'], [2, 'Black or African American'], [3, 'Hispanic or Latino'],
                 [4, 'White or Caucasian'], [5, 'Multiracial or Biracial'], [6, 'A race/ethnicity not listed here']])
    familiarity = models.IntegerField(
        label="<br>Please indicate whether you have <strong>encountered a member of your team before participating in this study</strong>.",
        choices=[[1, 'No, never met before'], [2, 'Yes, met in passing'],
                 [3, 'Yes, we are acquaintances']])

    education = models.IntegerField(
        label="<br>What is the highest level of education you have completed?</br>",
        choices=[[1, 'a'], [2, 'b'], [3, 'c'],
                 [4, 'd']])
    prolificPrevious = models.IntegerField(
        label="<br>How many studies have you done on Prolific in the last year?</br>",
        choices=[[1, 'a'], [2, 'b'], [3, 'c'],
                 [4, 'd']])
    random = models.CurrencyField()


# PAGES

class IntroPart3(Page):
    form_model = 'player'

class Quest02(Page):
    form_model = 'player'

    # usability, satisfaction, intention to use
    @staticmethod
    def get_form_fields(player):
        import random
        soco = ['social_cohesion_1', 'social_cohesion_2', 'social_cohesion_3', 'social_cohesion_4', 'social_cohesion_5',
                'social_cohesion_6', 'attention1']
        random.shuffle(soco)
        return soco

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention1 != 1:
            player.attention_check += 1


class Quest03(Page):
    form_model = 'player'
    form_fields = ['risk']


class Quest04(Page):
    form_model = 'player'
    form_fields = ['time_1', 'negative_rp_1', 'negative_rp_2', 'attention2', 'altruism_1']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention2 != 7:
            player.attention_check += 1


class Quest05(Page):
    form_model = 'player'
    form_fields = ['positive_rp_1', 'negative_rp_3', 'trust_1_positive', 'trust_2_negative', 'trust_3_positive',
                   'attention3', 'math', 'time_2']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention3 != 3:
            player.attention_check += 1


class Quest06(Page):
    form_model = 'player'
    form_fields = ['positive_rp_2']


class Quest07(Page):
    form_model = 'player'
    form_fields = ['altruism_2']


class Quest07a(Page):
    form_model = 'player'
    form_fields = ['big5_1', 'big5_2', 'big5_3', 'big5_4', 'big5_5',
                   'big5_6', 'big5_7', 'big5_8', 'big5_9', 'big5_10']


class Quest08(Page):
    form_model = 'player'

    # usability, satisfaction, intention to use
    @staticmethod
    def get_form_fields(player):
        import random
        collective = ['collective_orientation_1_p', 'collective_orientation_2_n', 'collective_orientation_3_n',
                      'collective_orientation_4_p', "collective_orientation_5_n", "collective_orientation_6_n",
                      "collective_orientation_7_n", "collective_orientation_8_n", "collective_orientation_9_n",
                      'collective_orientation_10_n', 'collective_orientation_11_n', 'collective_orientation_12_n',
                      'collective_orientation_13_n', 'collective_orientation_14_n', 'collective_orientation_15_n',
                      'attention4']
        random.shuffle(collective)
        return collective

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention4 != 5:
            player.attention_check += 1


class Quest09(Page):
    form_model = 'player'



class QuestDemographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'ethnicity', 'prolificPrevious', 'familiarity']


class QuestAR(Page):
    form_model = 'player'
    form_fields = ['attricativenessrating']

    @staticmethod
    def vars_for_template(player: Player):
        image_names = [
            'teamco1.png',
            'teamco2.png',
            'teamco3.png',
            'teamco4.png',
            'teamco5.png',
            'teamco6.png',

        ]
        return dict(image_data=make_image_data(image_names))


class Quest10(Page):
    form_model = 'player'
    form_fields = ['psychological_safety_1', 'psychological_safety_2', 'psychological_safety_3',
                   'psychological_availability_1', 'psychological_availability_2', 'psychological_availability_3',
                   'psychological_availability_4', 'psychological_availability_5']


class Quest11(Page):
    form_model = 'player'
    form_fields = ['engagement_1', 'engagement_2', 'engagement_3', 'engagement_4', 'engagement_5', 'engagement_6',
                   'engagement_7', 'engagement_8', 'engagement_9', 'engagement_10', 'engagement_11', 'engagement_12',
                   'engagement_13', 'engagement_14', 'engagement_15', 'engagement_16', 'engagement_17', 'engagement_18',
                   'engagement_19', 'engagement_20', 'engagement_21', 'engagement_22', 'engagement_23', 'engagement_24',
                   'engagement_25', 'engagement_26', 'engagement_27', 'engagement_28', 'engagement_29', 'engagement_30']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention_check <= 1:
            player.payoff_quests = 100
        else:
            player.payoff_quests = 0


class QuestEnd(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
            total_payoff=(200 + player.payoff_quests) * 0.03
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [IntroPart3, Quest02, Quest03, Quest04, Quest05, Quest06, Quest07, Quest07a, Quest08, Quest10, Quest11,
                 QuestDemographics, QuestEnd]
