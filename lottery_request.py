import requests
import pandas as pd
from os import getenv

def request_lottery_number(url: str, date: str) -> pd.DataFrame:
    lottery_url = url
    lottery_api_key = getenv("Thai_Lottery_API_Key")
    
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
        lottery_dataframe = pd.DataFrame(lottery_data)
        return lottery_dataframe
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


url = "https://thai-lottery1.p.rapidapi.com/index3"
date = "01072024"
df = request_lottery_number(url, date)
print(df)
