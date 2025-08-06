import pandas as pd
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--date', type=str, required=True)
    args = parser.parse_args()

    filepath = args.file
    print(f"Reading data from {filepath}")
    data = pd.read_excel(filepath)

    page_column = 'participant._current_page_name'
    date_column = 'participant.time_started_utc'
    last_page = 'QuestEnd'
    wait_page = 'MyWaitPage_TechProblem'
    wati_page_2 = 'MyWaitPageStage2Instructions'

    target_columns = [
        "participant.id_in_session",
        "participant._current_app_name",
        "participant._current_page_name",
        "participant.payoff",
        "participant.is_dropout",
        "App03WeakestLink.1.group.id_in_subsession",
        "participant.payoff_round",
        "App01cConsentAndCheck.1.player.ProlificId"
    ]

    # convert string to datetime in pandas dataframe
    data[date_column] = pd.to_datetime(data[date_column], utc=True)
    data_sub = data[data[date_column].dt.date == pd.to_datetime(args.date).date()]

    # get data based on pages
    data_of_interest = []
    
    for page in [last_page, wait_page, wati_page_2]:
        tmp = data_sub[data_sub[page_column] == page]
        data_of_interest.append(tmp)

    data_of_interest = pd.concat(data_of_interest)

    data_of_interest['In GBP'] = data_of_interest['participant.payoff'] * 0.02
    
    print(data_of_interest[target_columns + ['In GBP']])


