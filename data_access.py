# https://www.youtube.com/watch?v=T1vqS1NL89E&ab_channel=PythonEngineer
# https://github.com/python-engineer/python-knowledge/blob/master/googlesheets.py
# https://www.youtube.com/watch?v=cnPlKLEGR7E&list=WL&index=17&ab_channel=TechWithTim
# https://www.techwithtim.net/tutorials/google-sheets-python-api-tutorial/

from datetime import datetime

import gspread

gc = gspread.service_account(filename='credentials1.json')
sh = gc.open_by_key("19dLgpGsLAW4K4yiSdbpsA-njCGiDwhiYXa3uaWFJbsY")  # or by sheet name: gc.open("TestList")
worksheet = sh.sheet1

week_column = worksheet.col_values(5)

lesson_today = []


def get_data(week):
    lesson_today.clear()
    counter = 0
    for i in week_column:
        counter += 1

        if i == week:
            if datetime.today().isoweekday() == 1:
                if worksheet.cell(counter, 1).value == "monday":
                    lesson_today.append(worksheet.row_values(counter))
            elif datetime.today().isoweekday() == 2:
                if worksheet.cell(counter, 1).value == "tuesday":
                    lesson_today.append(worksheet.row_values(counter))
            elif datetime.today().isoweekday() == 3:
                if worksheet.cell(counter, 1).value == "wednesday":
                    lesson_today.append(worksheet.row_values(counter))
            elif datetime.today().isoweekday() == 4:
                if worksheet.cell(counter, 1).value == "thursday":
                    lesson_today.append(worksheet.row_values(counter))
            elif datetime.today().isoweekday() == 5:
                if worksheet.cell(counter, 1).value == "friday":
                    lesson_today.append(worksheet.row_values(counter))
            elif datetime.today().isoweekday() == 6:
                if worksheet.cell(counter, 1).value == "saturday":
                    lesson_today.append(worksheet.row_values(counter))
            elif datetime.today().isoweekday() == 7:
                if worksheet.cell(counter, 1).value == "sunday":
                    lesson_today.append(worksheet.row_values(counter))


def time_before_lesson(lesson_time):
    return str(datetime.strptime(lesson_time, "%H:%M") - datetime.strptime("00:10", "%H:%M"))[:-3]
