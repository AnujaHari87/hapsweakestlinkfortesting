import os
import pandas as pd
import argparse
from pathlib import Path
from sys import platform



def start_file(path: str):
    """Opens file with default app

    Usage:
    >>> start_file("my_file.xslx")
    """
    if platform.startswith(("cywin", "win32")):
        os.startfile(path)
    elif platform.startswith("linux"):
        os.system(f"xgd-open {os.path.abspath(path)}")
    elif platform.startswith("darwin"):
        os.system(f"open {os.path.abspath(path)}")

def custom_id(row: pd.Series) -> str:

    num = row["CappedGBP"]
    num_formatted = f"{num:.2f}"

    return row['App01cConsentAndCheck.1.player.ProlificId'] + "," + num_formatted


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--date', type=str, required=True)
    args = parser.parse_args()

    filepath = args.file
    print(f"Reading data from {filepath}")
    data = pd.read_csv(filepath, sep=',')

    page_column = 'participant._current_page_name'
    date_column = 'participant.time_started_utc'
    last_page = 'QuestEnd'
    wait_page = 'MyWaitPage_TechProblem'
    wait_page_2 = 'MyWaitPageStage2Instructions'
    thank_you_exit_page = 'ThankYouExit'

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
    
    for page in [last_page, wait_page, wait_page_2, thank_you_exit_page]:

        tmp = data_sub[data_sub[page_column] == page]

        if page == thank_you_exit_page:
            mask = tmp['participant._current_app_name'].isin(['App10TeamExitThankYou', 'App09TeamExitThankYou'])
            tmp = tmp[mask]
            
        data_of_interest.append(tmp)

    data_of_interest = pd.concat(data_of_interest)

    data_of_interest['In GBP'] = data_of_interest['participant.payoff'] * 0.02
    data_of_interest['CappedGBP'] = data_of_interest['In GBP'].apply(lambda x: x if x <= 6 else x - 6)
    data_of_interest['CustomID'] = [custom_id(row) for _, row in data_of_interest.iterrows()]


    # update target columns
    target_columns.extend(['In GBP', 'CappedGBP', "CustomID"])

    payoff_data_file = Path(args.file).parent / f'{args.date}_payoff.xlsx'
    data_of_interest[target_columns].to_excel(payoff_data_file, index=False)

    start_file(str(payoff_data_file))

