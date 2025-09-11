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



def deduplicate_prolific_entries(df: pd.DataFrame, 
                                prolific_id_column: str, 
                                payout_column: str,
                                annotation_column: str) -> pd.DataFrame:
    """
    Removes duplicates based on prolific_id_column, keeping the row 
    with the highest payout, and annotates if that participant had duplicates.

    Args:
        df (pd.DataFrame): Input dataframe
        prolific_id_column (str): Column with participant IDs
        payout_column (str): Column indicating participant payout

    Returns:
        pd.DataFrame: Deduplicated dataframe with an annotation column
    """
    if prolific_id_column not in df.columns:
        raise ValueError(f"Column '{prolific_id_column}' not found in dataframe.")
    if payout_column not in df.columns:
        raise ValueError(f"Column '{payout_column}' not found in dataframe.")
    
    # Count occurrences per participant
    counts = df[prolific_id_column].value_counts()
    has_dupes = counts[counts > 1].index
    
    # Sort so highest payout is last
    df_sorted = df.sort_values(by=[prolific_id_column, payout_column])
    
    # Keep max payout per participant
    df_dedup = df_sorted.drop_duplicates(subset=[prolific_id_column], keep="last")
    
    # Annotate participants that had multiple entries
    df_dedup[annotation_column] = df_dedup[prolific_id_column].isin(has_dupes)
    
    return df_dedup


# Define a function to color rows
def highlight_row(row, bool_column: str, color: str = 'red'):

    if row[bool_column]:
        return [f'background-color: {color}'] * len(row)  # whole row red
    
    return [''] * len(row)

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

    prolific_id_column = "App01cConsentAndCheck.1.player.ProlificId"
    annotation_prolific_id_column = 'Annotation_ProlificID_Duplicates_Removed'
    annotation_payout_zero = 'Annotation_Payout_Zero'

    target_columns = [
        "participant.id_in_session",
        "participant._current_app_name",
        "participant._current_page_name",
        "participant.payoff",
        "participant.is_dropout",
        "App03WeakestLink.1.group.id_in_subsession",
        "participant.payoff_round",
        prolific_id_column,
        annotation_prolific_id_column,
        annotation_payout_zero
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

    payout_column = 'CappedGBP'
    data_of_interest['In GBP'] = data_of_interest['participant.payoff'] * 0.02
    data_of_interest[payout_column] = data_of_interest['In GBP'].apply(lambda x: x if x <= 6 else x - 6)
    data_of_interest['CustomID'] = [custom_id(row) for _, row in data_of_interest.iterrows()]

    data_of_interest = deduplicate_prolific_entries(
        data_of_interest,
        prolific_id_column,
        payout_column,
        annotation_prolific_id_column
    )

    data_of_interest[annotation_payout_zero] = data_of_interest[payout_column] == 0


    # update target columns
    target_columns.extend(['In GBP', payout_column, "CustomID"])
    
    # Apply styling
    data_of_interest = data_of_interest[target_columns]
    highlight_row_tmp = lambda x: highlight_row(x, annotation_payout_zero)
    styled = data_of_interest.style.apply(highlight_row_tmp, axis=1)

    highlight_row_tmp = lambda x: highlight_row(x, annotation_prolific_id_column)
    styled = styled.apply(highlight_row_tmp, axis=1)

    payoff_data_file = Path(args.file).parent / f'{args.date}_payoff.xlsx'

    styled.to_excel(payoff_data_file, index=False)

    start_file(str(payoff_data_file))

