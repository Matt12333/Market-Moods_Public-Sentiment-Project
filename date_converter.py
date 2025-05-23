from datetime import datetime, timedelta, date

def get_monday_of_week(input_date):
    
    return input_date - timedelta(days=input_date.weekday())

def get_friday_of_week(input_date):

    monday = get_monday_of_week(input_date)
    return monday + timedelta(days=4)


if __name__ == "__main__":
    input_date = date(2025, 5, 6)

    print(get_monday_of_week(input_date))
    print(get_friday_of_week(input_date))