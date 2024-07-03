import requests
import pandas as pd
from os import getenv

# Define the prize list
prize_list = [
    "FIRST_Prize:6,000,000 Baht",
    "Three_digit_Prefix:4,000 Baht",
    "Three_digit_Suffix:4,000 Baht",
    "Two_digit_Suffix:2,000 Baht",
    "First_Prize_Neighbors:100,000 Baht",
    "Second_Prize:200,000 Baht",
    "Third_Prize:80,000 Baht",
    "Fourth_Prize:40,000 Baht",
    "Fifth_Prize:20,000 Baht"
]

# Create a DataFrame from the prize list
prize_dataframe = pd.DataFrame(prize_list, columns=['Prize_info'])
prize_dataframe[['Prize', 'Reward(Baht)']] = prize_dataframe['Prize_info'].str.split(":", expand=True)
prize_dataframe['Reward(Baht)'] = prize_dataframe['Reward(Baht)'].str.replace('Baht', "").str.replace(",", "").astype(int)
prize_dataframe.drop(columns=['Prize_info'], inplace=True)

def request_lottery_number(url: str, date: str) -> pd.DataFrame:
    lottery_url = url
    lottery_api_key = getenv("Thai_Lottery_API_Key")

    if not lottery_api_key:
        print("Error: Missing Thai Lottery API Key.")
        return pd.DataFrame()

    headers = {
        "x-rapidapi-key": lottery_api_key,
        "x-rapidapi-host": "thai-lottery1.p.rapidapi.com"
    }

    # Calculate the Thai year and format the date correctly
    year = int(date[-4:]) + 543
    thai_date = date[:-4] + str(year)  # Format as ddmmyyyy (e.g., 01072567)

    querystring = {"date": thai_date}

    try:
        response = requests.get(lottery_url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad status codes
        lottery_data = response.json()

        # Create a DataFrame from the lottery data
        raw_lottery_dataframe = pd.DataFrame(lottery_data)

        # Identify the first column's name (prize_with_thai)
        prize_with_thai = raw_lottery_dataframe.columns[0]
        
        # Drop the identified column
        raw_lottery_dataframe.drop(columns=[prize_with_thai], inplace=True)

        # Concatenate the prize_dataframe with raw_lottery_dataframe
        lottery_dataframe = pd.concat([prize_dataframe, raw_lottery_dataframe], axis=1)
        return lottery_dataframe
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


