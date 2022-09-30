from datetime import datetime
import re
import pandas as pd

__all__ = ["convert_header_to_df"]

GMAIL_TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
DATE_AMPM = "%Y_%m %d_%p"
DECIMAL = re.compile(r"\d+\.?\d+")
NAME_FROM = re.compile(r'(?<=")(.*?)(?=")')  # "([\"'])(?:(?=(\\?))\2.)*?\1"


def check_validity(sdf):
    s, d, f = sdf
    if DECIMAL.search(s) and NAME_FROM:
        try:
            datetime.strptime(d, GMAIL_TIME_FORMAT)
            return True
        except:
            pass
    return False


def list_to_df(body_heats_list):
    return pd.DataFrame(
        [sdf for sdf in body_heats_list if check_validity(sdf)],
        columns=["Subject", "Date", "From"],
    )


def sub_to_tmp(subj):
    temp = float(DECIMAL.search(subj).group(0))
    return temp if temp < 100 else temp / 10


def date_and_ampm(date):
    return datetime.strptime(date, GMAIL_TIME_FORMAT).strftime(DATE_AMPM).split()


def from_to_name(From):
    return NAME_FROM.search(From).group(0)


def convert_header_to_df(__headers_data):
    body_heats_df = list_to_df(__headers_data)
    df = pd.DataFrame(
        body_heats_df["Date"].apply(date_and_ampm).tolist(), columns=["YM", "DT"]
    )
    df["Name"] = body_heats_df["From"].apply(from_to_name)
    df["Temp"] = body_heats_df["Subject"].apply(sub_to_tmp)
    return df
