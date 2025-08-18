from os import environ

from otree.settings import AUTH_LEVEL

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='weakestlinkdemo', num_demo_participants=6,
                        app_sequence=  ['App01ConsentAndCheck', 'App01bConsentAndCheck', 'App01cConsentAndCheck',
                                      'App02PostIntro',
                                      'App03WeakestLink', 'App04Questionnaires',  'App06ThankYou',
                                      'App07ConsentThankYou','App07bEligibilityThankYou','App08DropoutThankYou', 'App09TeamExitThankYou','App10TeamExitThankYou'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['optInConsent', 'consent',  'numberVideo', 'colorVideo','payoff_ppg', 'payoff_round', 'past_group_id', 'arrival_time', 'wait_page_arrival','is_dropout','dropout_count']
SESSION_FIELDS = ['group_matrix']
ROOMS = [
    dict(
        name='HapsPilot',
        display_name='HAPS Pilot'
    )]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'otreehapsserver3'
AUTH_LEVEL = 'STUDY'
SECRET_KEY = 'blahblah'
OTREE_REST_KEY = 'otreehapsserverrest3'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

OTREE_PRODUCTION=1
DEBUG = False
