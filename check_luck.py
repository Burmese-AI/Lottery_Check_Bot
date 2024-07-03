import pandas as pd
from lottery_request import request_lottery_number

def check_prize(lottery_number: str, prize_numbers: pd.DataFrame, prize_index: int) -> bool:
    
    prize_numbers = prize_numbers.iloc[prize_index, 2:].dropna().astype(str)
    value_check = prize_numbers.str.contains(lottery_number, regex=True)
    return value_check.any()


def check_prizes(lottery_number: str, prize_numbers: pd.DataFrame) -> list:
    
    prizes_won = []

    if check_prize(lottery_number, prize_numbers, 0):
        prizes_won.append(f"First Prize:{prize_numbers.iloc[0,1]} ")

    if check_prize(lottery_number, prize_numbers, 4):
        prizes_won.append(f"First Neighbour Prize:{prize_numbers.iloc[4,1]}")

    if check_prize(lottery_number, prize_numbers, 5):
        prizes_won.append(f"Second Prize:{prize_numbers.iloc[5,1]}")

    if check_prize(lottery_number, prize_numbers, 6):
        prizes_won.append(f"Third Prize:{prize_numbers.iloc[6,1]}")

    if check_prize(lottery_number, prize_numbers, 7):
        prizes_won.append(f"Fourth Prize:{prize_numbers.iloc[7,1]}")

    if check_prize(lottery_number, prize_numbers, 8):
        prizes_won.append(f"Fifth Prize:{prize_numbers.iloc[8,1]}")

    if check_prize(lottery_number[:-3], prize_numbers, 1):
        prizes_won.append(f"Three Digit Prefix Prize:{prize_numbers.iloc[1,1]}")

    if check_prize(lottery_number[-3:], prize_numbers, 2):
        prizes_won.append(f"Three Digit Suffix Prize:{prize_numbers.iloc[2,1]}")

    if check_prize(lottery_number[-2:], prize_numbers, 3):
        prizes_won.append(f"Two Digit Suffix Prize:{prize_numbers.iloc[3,1]}")

    return prizes_won

def prize_report(lottery_number, prize_data: pd.DataFrame) -> str:
    prizes_won = check_prizes(lottery_number, prize_data)

    if prizes_won:
        result = "Congratulations! You won the following prizes:\n"
        result += "\n".join([f"- {prize}" for prize in prizes_won])
    else:
        result = "May you be lucky next time"

    return result
