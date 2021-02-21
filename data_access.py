# https://www.youtube.com/watch?v=T1vqS1NL89E&ab_channel=PythonEngineer
# https://github.com/python-engineer/python-knowledge/blob/master/googlesheets.py
# https://www.youtube.com/watch?v=cnPlKLEGR7E&list=WL&index=17&ab_channel=TechWithTim
# https://www.techwithtim.net/tutorials/google-sheets-python-api-tutorial/

from datetime import datetime
import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key("19dLgpGsLAW4K4yiSdbpsA-njCGiDwhiYXa3uaWFJbsY")
worksheet = sh.sheet1

week_column = worksheet.col_values(5)  # list of weeks column
# dictionary to recognize which day is today
days_dict = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
lesson_today = []  # list which will save the row of data from google sheet


def get_lessons(week):
    lesson_today.clear()  # clear previous data
    counter = 0  # counter for moving along rows
    for i in week_column:
        counter += 1
        if i == week:
            if worksheet.cell(counter, 1).value == days_dict[datetime.today().isoweekday()]:
                lesson_today.append(worksheet.row_values(counter))


get_lessons("парний")
print(lesson_today)


def insert_data(data_list):
    for i in range(0, len(data_list)):
        worksheet.update_cell(i + 2, 7, data_list[i])


def get_users_id():
    return worksheet.col_values(7)[1:]


def time_before_lesson(lesson_time):
    return str(datetime.strptime(lesson_time, "%H:%M") - datetime.strptime("00:10", "%H:%M"))[:-3]
