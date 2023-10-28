from datetime import datetime


def format_date(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


Custom_Filters = {"format_date": format_date}
