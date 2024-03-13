import re
import pandas as pd
from typing import Tuple, Callable


def get_date(text: str)-> str:
    """ Gets dates from text in the DD/MM/YYYY format,
    if only a YEAR(YYYY) is found then 01/01/YEAR is returned.
    Finally if no date is possible, a generic 01/01/1999 is used 
    """
    year_pattern = r'\b(\d{4})\b'
    date_pattern = r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b'
    get_year = lambda x: '01/01/' + (re.findall(year_pattern, x)[0] if re.findall(year_pattern, x) else '1999')
    res = re.findall(date_pattern, text)
    date_format = lambda x, y: "/".join(x[0]) if x and len(x[0]) > 1 else get_year(y)
    return date_format(res, text)

def get_time(text: str)-> str:
    """ Gets time from text in the HH:MM format,
    if none is found, 00:01 is used.
    """
    time_pattern = r'\b(\d{1,2}):(\d{2})\b'
    time_format = lambda x: ":".join(x[0]) if x and len(x[0]) > 1 else '00:01'
    res = re.findall(time_pattern, text)
    return time_format(res)

def break_up_datetime(datetime: str|None)-> Tuple[str|None]:
    """ Datetime 'possibly' contains DD/MM/YYYY 
    and HH:MM formats. Information is either
    captured or None returned.
    """
    if isinstance(datetime, str) and datetime:
        date = get_date(datetime)
        time = get_time(datetime)
        return date, time
    else:
        return None, None
    
def break_up_meta(text: str)-> Tuple[str|None]:
    """ Meta 'possiblly' contains user, datetime,
    and location information. Extracted if found,
    else None.
    """
    if isinstance(text, str):
        user, datetime, *locations = text.split('-')
        date, time = break_up_datetime(datetime)
        location = '-'.join(locations).strip()
        return user.strip(), date, time, location.strip()
    else:
        return None, None, None, None
    
def apply_break_up_meta(df: pd.DataFrame)-> Callable:
    """ Applies 'break_up_meta' function on pre-selected
    columns of a dataframe. Drops the no longer need
    'meta' column and re-indexes df.
    """
    new = df.copy()
    new[['user', 'date', 'time', 'location']] = new['meta'].apply(break_up_meta).apply(pd.Series)
    new.drop(columns=['meta'], inplace=True)
    new.reset_index(drop=True, inplace=True)
    return apply_get_gender(new)
    
def get_gender(text: str)-> str|None:
    """ If keyword is found in string, returns it,
    else None.
    """
    if isinstance(text, str):
        if 'male' in text:
            return 'male'
        elif 'female' in text:
            return 'female'
    return None

def apply_get_gender(df: pd.DataFrame)-> Callable:
    """ Applies 'get_gender' to 'gender' column
    in df.
    """
    new = df.copy()
    new['gender'] = new['gender'].apply(get_gender)
    return str_to_int(new)

def str_to_int(df: pd.DataFrame)-> Callable:
    """ Converts string values of pre-selected
    columns in a dataframe into integers.
    """
    new = df.copy()
    deal_with_int = lambda x: x if isinstance(x, int) else 0
    intify = lambda x: int(x.replace(" ", '')) if isinstance(x, str) else deal_with_int(x)
    targets = ['agree', 'deserved']
    new[targets] = new[targets].map(intify)
    return clean_user(new)

def clean_user(df: pd.DataFrame)-> Callable:
    """ Removes 'By' and ',' from 'user' column
    in a dataframe.
    """
    new = df.copy()
    new['user'] = new['user'].str.replace('By', '').str.replace(',', '').str.strip()
    return clean_body(new)

def clean_body(df: pd.DataFrame)-> Callable:
    """ Removes newlines (\n) and whitespaces from 
    the 'body' column in a dataframe.
    """
    new = df.copy()
    new['body'] = new['body'].str.replace('\n', '').str.strip()
    return lowering_text(new)

def lowering_text(df: pd.DataFrame)-> pd.DataFrame:
    """ Lowers text in pre-selected columns
    within a dataframe.
    """
    new = df.copy()
    targets = ['title', 'gender', 'body', 'user', 'location']
    lower_text = lambda x: x.lower() if isinstance(x, str) else None
    new[targets] = new[targets].map(lower_text)
    return new

def clean_raw(df: pd.DataFrame)-> Callable:
    """ Initial function in chain of functions. 
    Drops rows if 'meta' column has NaN, removes
    duplicates and re-indexes the dataframe.
    """
    new = df.copy()
    new.dropna(subset=['meta'], inplace=True)
    new.drop_duplicates()
    new.reset_index(drop=True, inplace=True)
    return apply_break_up_meta(new)