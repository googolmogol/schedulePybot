# https://www.youtube.com/watch?v=T1vqS1NL89E&ab_channel=PythonEngineer
# https://github.com/python-engineer/python-knowledge/blob/master/googlesheets.py
# https://www.youtube.com/watch?v=cnPlKLEGR7E&list=WL&index=17&ab_channel=TechWithTim
# https://www.techwithtim.net/tutorials/google-sheets-python-api-tutorial/

# open/create/delete new sheets tutorial
# https://github.com/burnash/gspread

from datetime import datetime
import gspread

gc = gspread.service_account(filename='restfiles/cred.json')
sh = gc.open_by_key("19dLgpGsLAW4K4yiSdbpsA-njCGiDwhiYXa3uaWFJbsY")
worksheet = sh.sheet1
worksheet2 = sh.worksheet("users")

# dictionary to recognize which day is today
days_dict = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
lesson_to_change = []  # list which will save the row of data from google sheet
row_index_to_change = []


# function parsing lesson row
def get_lessons_row(week, day, row_index):
    week_column = worksheet.col_values(5)  # list of weeks column

    row_index_to_change.clear()
    lesson_to_change.clear()  # clear previous data
    counter = 0  # counter for moving along rows
    for i in week_column:
        counter += 1
        if i == week:
            if worksheet.cell(counter, 1).value == days_dict[day]:
                lesson_to_change.append(worksheet.row_values(counter))
                if row_index:
                    row_index_to_change.append(counter)
    print('row_index_to_change:', row_index_to_change)
    return lesson_to_change


def insert_users(data_list):
    for i in range(0, len(data_list)):
        worksheet2.update_cell(i + 2, 1, data_list[i])


def update_data(row, col, value):
    worksheet.update_cell(row, col, value)


def add_new_lesson(user_step):
    worksheet.append_row(user_step)


def get_users_id():
    return worksheet2.col_values(1)[1:]


def time_before_lesson(lesson_time):
    return str(datetime.strptime(lesson_time, "%H:%M") - datetime.strptime("00:10", "%H:%M"))[:-3]

