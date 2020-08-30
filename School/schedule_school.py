import ScheduleSchoolSettings
import requests
import json
import pygame
from tkinter import * 
from tkinter.ttk import *
from win32api import GetMonitorInfo, MonitorFromPoint
from datetime import datetime, timedelta

# This function recursively calls itself every 1 second
def time():
    # Get the time in HH:MM:SS format
    current_time = '{:02}:{:02}:{:02}'.format(datetime.now().hour + settings['time_offset'], datetime.now().minute, datetime.now().second)

    # Display the time
    canvas.itemconfigure(text_current_time, text=current_time)

    # Get the current time
    current_date_time = datetime.strptime(current_date + current_time, '%Y-%m-%d %H:%M:%S')

    # Calculate the total number of seconds since the start of the first lesson
    estimated_total_seconds = int((current_date_time - school_starting_time).total_seconds())

    # Calculate and display progress bar for current time
    timeline_indicator_x = (estimated_total_seconds / total_school_day_seconds) * timeline_size + timeline_left_x
    x0, y0, x1, y1 = canvas.coords(timeline_indicator)
    x0 = timeline_indicator_x
    canvas.coords(timeline_indicator, x0, y0, x0 + 2, y1)


    i = 0
    last_checked_rectangle_index = -1
    for current_class in data['days'][day]['classes']:

        # Get selected classes lessons for today
        class_lessons = current_class['lessons']

        # Get the number of lessons per day and set timeline coords
        lessons_count = len(class_lessons)

        global last_lesson_finished

        # If the last lesson is not finished
        if not last_lesson_finished[i]:

            # Get lesson/break starting and ending times for selected class
            class_timeslots = current_class['timeslots']

            # test = canvas.itemcget(day_name, 'text')
            # if  len(test) < 120:
            #     #test = test + str(int(x0)) + '-' + str(int(rx1)) + '-' + str(int(last_completed_rectangle_x1[i])) + ' '
            #     test = test + ' ' + str(len(classes[0]))
            #     canvas.itemconfigure(day_name, text=test)

            # Loop for each lesson and break rectangles
            x = 0
            for r in range(last_checked_rectangle_index + 1, (i + 1) * (lessons_count * 2 - 1)):
   
                rx0, ry0, rx1, ry1 = canvas.coords(rectangles[r])
                global last_completed_rectangle_x1, first_run

                # Change the current lesson/break color
                if x0 > rx0 and x0 < rx1 and (current_time.split(':')[2] == '00' or first_run):
                    if canvas.itemcget(rectangles[r], 'fill') == settings['lesson_color'] and canvas.itemcget(rectangles[r], 'fill') != settings['current_lesson_color']:
                        canvas.itemconfigure(rectangles[r], fill=settings['current_lesson_color'])
                    elif canvas.itemcget(rectangles[r], 'fill') == settings['break_color'] and canvas.itemcget(rectangles[r], 'fill') != settings['current_break_color']:
                        canvas.itemconfigure(rectangles[r], fill=settings['current_break_color'])

                # Change the last finished lesson/break color
                if x0 > rx1 and rx1 > last_completed_rectangle_x1[i] and (current_time.split(':')[2] == '00' or first_run):

                    if canvas.itemcget(rectangles[r], 'fill') == settings['lesson_color']:
                        canvas.itemconfigure(rectangles[r], fill=settings['finished_lesson_color'])
                        if not first_run:
                            play()
                    else:
                        canvas.itemconfigure(rectangles[r], fill=settings['finished_break_color'])
                        if not first_run:
                            play()
                    global completed_lesson_break_count
                    completed_lesson_break_count[i] += 1
                    last_completed_rectangle_x1[i] = rx1

                    if completed_lesson_break_count[i] == len(class_timeslots):
                        last_lesson_finished[i] = True
                        break
            
        last_checked_rectangle_index += lessons_count * 2 - 1

        i = i + 1
    
    if first_run:
        first_run = False

    # Recursively call this function every 1 second
    form.after(1000, time)

# This function calculates the x coords of a given time in HH:MM format
def get_x_from_time(t):
    timeline_time = datetime.strptime(current_date + t, '%Y-%m-%d %H:%M')
    estimated_timeline_time = timeline_time - school_starting_time
    estimated_timeline_seconds = estimated_timeline_time.total_seconds()
    return int(timeline_left_x + (estimated_timeline_seconds / total_school_day_seconds) * timeline_size)

def get_school_starting_ending_time(day):
    min_time = datetime.strptime(current_date + '23:59', '%Y-%m-%d %H:%M')
    max_time = datetime.strptime(current_date + '00:01', '%Y-%m-%d %H:%M')

    for current_class in data['days'][day]['classes']:
        hour_minute_start = current_class['timeslots'][0].split('-')[0]
        start_time = datetime.strptime(current_date + hour_minute_start, '%Y-%m-%d %H:%M')
        if start_time < min_time:
            min_time = start_time

        hour_minute_end = current_class['timeslots'][-1].split('-')[1]
        end_time = datetime.strptime(current_date + hour_minute_end, '%Y-%m-%d %H:%M')
        if end_time > max_time:
            max_time = end_time

    return min_time, max_time

def set_hour_indicators(day):
    min_time, max_time = get_school_starting_ending_time(day)

    while min_time < max_time:
        if min_time.minute == 0 or min_time.minute == 30:
            hour_indicator_text = '{:02}:{:02}'.format(min_time.hour, min_time.minute)
            hour_indicator_x = get_x_from_time(hour_indicator_text)
            if min_time.minute == 0:
                canvas.create_rectangle(hour_indicator_x, title_height + top_bottom_margin, hour_indicator_x + 2, window_height - top_bottom_margin, fill=settings['hour_indicator_text_font_color'])
                canvas.create_text(hour_indicator_x, title_height + 10, fill=settings['hour_indicator_text_font_color'], font=settings['hour_indicator_text_font_style'], text=hour_indicator_text)
                canvas.create_text(hour_indicator_x, window_height - 10, fill=settings['hour_indicator_text_font_color'], font=settings['hour_indicator_text_font_style'], text=hour_indicator_text)
            else:
                canvas.create_rectangle(hour_indicator_x, title_height + top_bottom_margin, hour_indicator_x + 2, window_height - top_bottom_margin, fill=settings['half_hour_indicator_text_font_color'])
                canvas.create_text(hour_indicator_x, title_height + 10, fill=settings['half_hour_indicator_text_font_color'], font=settings['half_hour_indicator_text_font_style'], text=hour_indicator_text)
                canvas.create_text(hour_indicator_x, window_height - 10, fill=settings['half_hour_indicator_text_font_color'], font=settings['half_hour_indicator_text_font_style'], text=hour_indicator_text)
        min_time += timedelta(minutes=1)
    

# This function calculates the center x coords of a rectangle by given timeslot index
def get_center_x(i, timeslots):
    starting_x = get_x_from_time(timeslots[i].split('-')[0])
    finishing_x = get_x_from_time(timeslots[i].split('-')[1])
    half_width = int(finishing_x - starting_x) / 2
    center_x = starting_x + half_width
    return center_x

# Get the selected class data from JSON file
def get_selected_class_data(class_name):
    for current_class in data['days'][day]['classes']:
        if current_class['class'] == class_name:
            return current_class

# This function can be used for closing the app
def close_program():
    form.destroy()

# Prevent app closing
def disable_event():
    pass

def play():

    pygame.mixer.music.load("../sounds/notification_1.mp3")
    pygame.mixer.music.play(loops=0)

form = Tk()

# Get application settings
settings = ScheduleSchoolSettings.getSettings()

# Open local JSON file
with open('../data/weekly_schedule.json') as json_file:
    data = json.load(json_file)

# Open remote JSON file
# with requests.get("https://api.jsonbin.io/b/5f429a1d514ec5112d0ca631") as response:
#     data = response.json()

# Make window allways on top and make it black and transparent
form.protocol("WM_DELETE_WINDOW", disable_event)
form.wm_attributes("-topmost", 1)
form.wm_attributes("-alpha", settings['form_transparency'])
form['bg'] = settings['form_background']

# Get os screen width and height
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()

# Get taskbar y coordinate
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
taskBar_y_coordinate = work_area[3]

# Set app windows screen width and height
window_height = taskBar_y_coordinate 
window_width = screen_width

# Set app x and y coordinates
x_coordinate = 0
y_coordinate = 0

# Place the app window on right above the taskbar and make it unresizable and borderless
form.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
form.resizable(False, False)
form.overrideredirect(True)

pygame.mixer.init()

canvas = Canvas(form, width=window_width - 4, height=window_height - 2, background=settings['form_background'], highlightthickness=0)
canvas.pack()

# Get the number af day in week
day = datetime.today().weekday() + settings["day_offset"]

timeline_left_x = 100
timeline_right_x = screen_width - 4
timeline_size = timeline_right_x - timeline_left_x
title_height = settings['title_height']
top_bottom_margin = settings['top_bottom_margin']
rectangle_height = 38
rectangle_y_center = rectangle_height / 2
bar_spacing = 7
class_bar_height = rectangle_height + bar_spacing



# Create text for displaying remaining time on the left and current time on the right of timeline
rectangles = []
texts_remaining_time = []

day_name_text = data['days'][day]['day']
daynumber = datetime.today().day
month = datetime.today().month
year = datetime.today().year
title = '{:02}.{:02}.{} {}'.format(daynumber, month, year, day_name_text)
day_name = canvas.create_text(window_width / 2, title_height / 2 - 16, fill=settings['title_font_color'], font=settings['title_font_style'], text=title)
text_current_time = canvas.create_text(window_width / 2, title_height / 2 + 16, fill=settings['current_time_font_color'], font=settings['current_time_font_style'])

# Get current date in YY-MM-DD format
current_date = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day) + ' '


school_starting_time, school_ending_time = get_school_starting_ending_time(day)
total_school_day_time = school_ending_time - school_starting_time
total_school_day_seconds = total_school_day_time.total_seconds()

set_hour_indicators(day)

n = 0
class_count = len(data['days'][day]['classes'])
y = (window_height - title_height - rectangle_height - 2 * top_bottom_margin - 10) / (class_count - 1)

for current_class in data['days'][day]['classes']:

    current_row_y = title_height + top_bottom_margin + n * y + 5

    current_class_name = current_class['class']
    class_name = canvas.create_text(timeline_left_x / 2, current_row_y + rectangle_height / 2, fill=settings['class_name_font_color'], font=settings['class_name_font_style'], text=current_class_name)
    texts_remaining_time.append(canvas.create_text(timeline_left_x / 2, current_row_y + rectangle_height / 2, fill=settings['remaining_time_font_color'], font=settings['remaining_time_font_style']))

    # Get lesson/break starting and ending times for selected class
    class_timeslots = current_class['timeslots']

    # Get selected classes lessons for today
    class_lessons = current_class['lessons']

    # Get selected classes teachers for today
    class_teachers = current_class['teachers']

    # Get the number of lessons per day and set timeline coords
    lessons_count = len(class_lessons)

    # Create a rectangle for each lesson and break
    for i in range(lessons_count):

        # Get center x coords for every timeslots (lesson/break)
        center_x = get_center_x(i * 2, class_timeslots)

        # Get center x coords for every timeslots (lesson/break)
        left_x = get_x_from_time(class_timeslots[i*2].split('-')[0])
        right_x = get_x_from_time(class_timeslots[i*2].split('-')[1])

        # Create a rectangle for each lesson
        rectangles.append(canvas.create_rectangle(left_x, current_row_y, right_x, current_row_y + rectangle_height, fill=settings['lesson_color']))

        # Create texts for lesson numbers and lesson titles
        canvas.create_text(center_x, current_row_y + 5, text='{}. Ders'.format(i+1), fill='black', font='calibri 10')
        canvas.create_text(center_x, current_row_y + rectangle_y_center, text=class_lessons[i], fill='black', font='calibri 12 bold')
        canvas.create_text(center_x, current_row_y + 31, text=class_teachers[i], fill='black', font='calibri 10')

        # Create texts for lesson starting time on the left and lesson ending time on the right of rectangles 
        canvas.create_text(left_x + 16, current_row_y + rectangle_y_center, text=class_timeslots[i*2].split('-')[0], fill='black', font='calibri 10')
        canvas.create_text(right_x - 16, current_row_y + rectangle_y_center, text=class_timeslots[i*2].split('-')[1], fill='black', font='calibri 10')

        # Create a rectangle for each break
        if i < lessons_count - 1:
            rectangles.append(canvas.create_rectangle(get_x_from_time(class_timeslots[i*2+1].split('-')[0]), current_row_y, get_x_from_time(class_timeslots[i*2+1].split('-')[1]), current_row_y + rectangle_height, fill=settings['break_color']))
    
    n = n + 1

get_school_starting_ending_time(day)
# Create progress bar at the bottom of timeline
timeline_indicator = canvas.create_rectangle(timeline_left_x, title_height, timeline_left_x + 2, window_height, fill='#ff0000')

completed_lesson_break_count = [0] * class_count
last_completed_rectangle_x1 = [0] * class_count
last_lesson_finished = [False] * class_count
first_run = True

time()

form.mainloop()