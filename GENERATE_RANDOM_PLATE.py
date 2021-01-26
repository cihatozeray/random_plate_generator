# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 00:09:34 2020

@author: Cihat Özeray

"""

import string
import random
import urllib.request
import pandas as pd
# import time


def get_data_from_web():
    """
    web scraping using urllib
    """
    # getting the html as a string:
    url = 'https://www.gib.gov.tr/plaka-harf-grubu'
    response = urllib.request.urlopen(url)
    content = response.read()
    content = str(content)
    # useful portion of the string is selected:
    temp_start = content.find("fileadmin/user_upload/Plaka_Harf/Adana.htm")
    temp_start -= 6
    temp_end = content.find("Harf/Rize.htm")
    temp_end += 14
    content = content[temp_start:temp_end]
    # generation of the url's from the raw string (each url represents a province)
    content_list = content.split("target=")
    url_list = []
    for i in content_list:
        j = i.find("href=")
        url_list.append(i[j:])

    url_list = [i.replace("href=", "").strip() for i in url_list]
    url_list = [i[1:-1] for i in url_list]

    url_list = ["http://www.gib.gov.tr/" + i for i in url_list]

    # necassary table from each url is saved into a dictinary
        # where keys represent the province codes

    provinces_dict = {}
    print("\n\ndownloading from 'www.gib.gov.tr' \n")

    for url_city in url_list:
        print("downloading ...  " + url_city[55:-4])
        # there were complications caused by the inputs 'NA' which
            #(keep_default_na' used for that purpose)
        df_temp = pd.read_html(url_city, keep_default_na=False)
        df_temp = df_temp[-1]
        province_code = df_temp.iat[2, 1]
        provinces_dict[province_code] = df_temp

    return provinces_dict


def data_cleansing(provinces_dict):
    """
    data cleansing using pandas dataframe
    """

    cleansed_provinces_dict = {}

    for df_temp in provinces_dict.values():
        # unrelated columns to the plate generation are dropped
        # df_temp.drop(df_temp.columns[[0, 6, 7]], axis=1, inplace=True)

        # these rows has missing information that cannot be filled by logic
        df_temp.dropna(thresh=3, inplace=True)

        # type conversion for data cleansing
        df_temp = df_temp[[1, 2, 3, 4, 5]].astype(str)

        # headings are dropped from each table
        df_temp = df_temp[df_temp[1].str.isnumeric()]

        # private plates and state official's plates are dropped
        df_temp = df_temp[df_temp[2].str.len() < 4]

        # unvalid letter entries are replaced with the logical twins
        df_temp = df_temp.replace("Â", "A", regex=True)

        # all of the rows in the dataframe are appended into a list
            # which will be used later as a rulebook
            # if the last item is missing, it could not be filled logically
            # and these rows are dropped
        plate_boundary_list = [list(i) for i in df_temp.itertuples(index=False) if i[-1] != "" \
                               and i[-1] is not None]

        # best guess when one of the letters is missing:
            # the other letter has taken as the only option available
            # existing letters are copied into missing ones:
        for i in plate_boundary_list:
            if i[3] == "":
                i[3] = i[1]
        province_code = int(plate_boundary_list[1][0])
        cleansed_provinces_dict[province_code] = [i[1:] for i in plate_boundary_list]


    return cleansed_provinces_dict


def generate_string_range():
    """
    generates a string range to choose from
    returns: List of strings
    """

    # from "A" to "ZZZ",  an ordered list is created for representing a string range

    # illegal letters are removed
    not_allowed = ["X", "W", "Q"]
    upper = [i for i in list(string.ascii_uppercase) if i not in not_allowed]

    string_list = upper.copy()

    for i in upper:
        for j in upper:
            temp = i + j
            string_list.append(temp)
    for i in upper:
        for j in upper + ["I", "O"]:
            for k in upper:
                temp = i + j + k
                string_list.append(temp)

    return string_list


def generate_random_plate(cleansed_provinces_dict, string_list):
    """
    generates a random plate within designated laws
    returns: String
    """

    province = random.randint(1, 81)
    district = random.randint(0, len(cleansed_provinces_dict[province])-1)
    constraint = cleansed_provinces_dict[province][district]
    lower_boundary = string_list.index(constraint[0])
    upper_boundary = string_list.index(constraint[2])
    plate_middle = string_list[random.randint(lower_boundary, upper_boundary)]
    plate_end_int = random.randint(int(constraint[1]), int(constraint[3]))

    province, plate_end = str(province), str(plate_end_int)
    province = "0" + province if len(province) == 1 else province

    plate = province + " " + plate_middle + " " + plate_end

    return plate


def test_letters(cleansed_provinces_dict, string_list):
    """
    Prints all of the strings available
    It is useful to test if data is missing or misread
    """
    for i in cleansed_provinces_dict.keys():
        for j in cleansed_provinces_dict[i]:
            for k in string_list[string_list.index(j[0]) : string_list.index(j[2]) + 1]:
                plate = str(i) + " " + k + " "
                print(plate)


def test_numbers(cleansed_provinces_dict):
    """
    Prints start and end points of the number range
    It is useful to test if data is missing or misread
    """
    for i in cleansed_provinces_dict.keys():
        for j in cleansed_provinces_dict[i]:
            if not j[1].isnumeric() or not j[3].isnumeric():
                print("ERROR")
            plate = str(i)  + " " + str(j[1]) + " " + str(j[3])
            print(plate)


def main():
    """
    main function:
        Calls necessary functions to print a random plate
        has tests for data acquisition and cleansing
        has a test for time it takes to execute
    """

    # t0 = time.time()

    global PROVINCES_DICT
    global CLEANSED_PROVINCES_DICT
    global STRING_LIST

    if "PROVINCES_DICT" not in globals():
        PROVINCES_DICT = get_data_from_web()
    if "CLEANSED_PROVINCES_DICT" not in globals():
        CLEANSED_PROVINCES_DICT = data_cleansing(PROVINCES_DICT)
    if "STRING_LIST" not in globals():
        STRING_LIST = generate_string_range()


    print("\n" + generate_random_plate(CLEANSED_PROVINCES_DICT, STRING_LIST))

    # test_letters(CLEANSED_PROVINCES_DICT, STRING_LIST)
    # test_numbers(CLEANSED_PROVINCES_DICT)

    # t1 = time.time()
    # print(t1-t0)


if __name__ == "__main__":
    main()
