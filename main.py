import Settings
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

    global last_lesson_finished, first_run

    # If the last lesson is not finished
    if not last_lesson_finished:

        # Calculate the total number of seconds since the start of the first lesson
        estimated_total_seconds = int((current_date_time - first_lesson_starting_time).total_seconds())

        # Calculate and display progress bar for current time
        progress_bar_size = (estimated_total_seconds / total_school_day_seconds) * timeline_size
        x0, y0, x1, y1 = canvas.coords(progress_bar)
        x1 = x0 + progress_bar_size 
        canvas.coords(progress_bar, x0, y0, x1, y1)

        # Loop for each lesson and break rectangles
        for rectangle in rectangles:
            rx0, ry0, rx1, ry1 = canvas.coords(rectangle)
            global last_completed_rectangle_x1

            # Change the last finished lesson/break color
            if x1 > rx1 and rx1 > last_completed_rectangle_x1 and (current_time.split(':')[2] == '00' or first_run):
                if canvas.itemcget(rectangle, 'fill') == settings['lesson_color']:
                    canvas.itemconfigure(rectangle, fill=settings['finished_lesson_color'])
                    if not first_run:
                        play(True)
                else:
                    canvas.itemconfigure(rectangle, fill=settings['finished_break_color'])
                    if not first_run:
                        play(False)
                global completed_lesson_break_count
                completed_lesson_break_count += 1
                last_completed_rectangle_x1 = rx1

                if completed_lesson_break_count == len(todays_timeslots):
                    last_lesson_finished = True
                    break

            # Get the current lesson or breaks ending time
            end_time = datetime.strptime(current_date + todays_timeslots[completed_lesson_break_count].split('-')[1], '%Y-%m-%d %H:%M')

            # Calculate the remaining seconds for the lesson or break
            remaining_seconds = int((end_time - current_date_time).total_seconds()) + 1

            # Display remaining time in MM:SS format
            remaining_time_text ='{:02}:{:02}'.format(remaining_seconds % 3600 // 60, remaining_seconds % 60)
            canvas.itemconfigure(text_remaining_time, text=remaining_time_text)
    
    if first_run:
        first_run = False

    # Recursively call this function every 1 second
    form.after(1000, time)

# This function calculates the x coords of a given time in HH:MM format
def get_x_from_time(t):
    timeline_time = datetime.strptime(current_date + t, '%Y-%m-%d %H:%M')
    estimated_timeline_time = timeline_time - first_lesson_starting_time
    estimated_timeline_seconds = estimated_timeline_time.total_seconds()
    return int(timeline_left_x + (estimated_timeline_seconds / total_school_day_seconds) * timeline_size)

# This function calculates the center x coords of a rectangle by given timeslot index
def get_center_x(i):
    starting_x = get_x_from_time(todays_timeslots[i].split('-')[0])
    finishing_x = get_x_from_time(todays_timeslots[i].split('-')[1])
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

def play(isLesson):
    if isLesson:
        pygame.mixer.music.load("sounds/notification_1.mp3")
    else:
        pygame.mixer.music.load("sounds/notification_2.mp3")
    pygame.mixer.music.play(loops=0)

form = Tk()

# Get application settings
settings = Settings.getSettings()

# Open local JSON file
# with open('weekly_schedule.json') as json_file:
#     data = json.load(json_file)

# Open remote JSON file
with requests.get("https://api.jsonbin.io/b/5f429a1d514ec5112d0ca631") as response:
    data = response.json()

# Make window allways on top and make it black and transparent
form.protocol("WM_DELETE_WINDOW", disable_event)
form.wm_attributes("-topmost", 1)
form.wm_attributes("-alpha", settings['form_transparency'])
form['bg'] = settings['form_background']

# Get os screen width and height
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()

# Set app windows screen width and height
window_height = 50
window_width = screen_width

# Get taskbar y coordinate
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
taskBar_y_coordinate = work_area[3]

# Set app x and y coordinates
x_coordinate = 0
y_coordinate = taskBar_y_coordinate - window_height

# Place the app window on right above the taskbar and make it unresizable and borderless
form.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
form.resizable(False, False)
form.overrideredirect(True)

pygame.mixer.init()

canvas = Canvas(form, width=window_width - 4, height=window_height - 2, background=settings['form_background'], highlightthickness=0)
canvas.pack()

# Get the number af day in week
day = datetime.today().weekday() - 6

# Create text for displaying remaining time on the left and current time on the right of timeline
top_margin = 24
selected_class = settings['selected_class']
selected_class_data = get_selected_class_data(selected_class)
class_name = canvas.create_text(34, top_margin - 10, fill=settings['class_name_font_color'], font=settings['class_name_font_style'], text=selected_class)
text_remaining_time = canvas.create_text(34, top_margin + 10, fill=settings['remaining_time_font_color'], font=settings['remaining_time_font_style'])
day_name = canvas.create_text(window_width - 60, top_margin - 10, fill=settings['day_name_font_color'], font=settings['day_name_font_style'], text=data['days'][day]['day'])
text_current_time = canvas.create_text(window_width - 60, top_margin + 10, fill=settings['curent_time_font_color'], font=settings['curent_time_font_style'])

# Get selected classes lessons for today
todays_lessons = selected_class_data['lessons']

# Get lesson/break starting and ending times for selected class
todays_timeslots = selected_class_data['timeslots']

# Get current date in YY-MM-DD format
current_date = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day) + ' '

# Get the number of lessons per day and set timeline coords
lessons_per_day = len(todays_lessons)
timeline_left_x = 70
timeline_right_x = 1800
timeline_size = timeline_right_x - timeline_left_x

# 
first_lesson_starting_time = datetime.strptime(current_date + todays_timeslots[0].split('-')[0], '%Y-%m-%d %H:%M')
last_lesson_finishing_time = datetime.strptime(current_date + todays_timeslots[len(todays_timeslots)-1].split('-')[1], '%Y-%m-%d %H:%M')
total_school_day_time = last_lesson_finishing_time - first_lesson_starting_time
total_school_day_seconds = total_school_day_time.total_seconds()

# Create progress bar at the bottom of timeline
progress_bar = canvas.create_rectangle(timeline_left_x, 41, timeline_left_x + 1, 48, fill='#ff0000')

# Create a rectangle for each lesson and break
rectangles = []
for i in range(lessons_per_day):

    # Get center x coords for every timeslots (lesson/break)
    center_x = get_center_x(i*2)

    # Get center x coords for every timeslots (lesson/break)
    left_x = get_x_from_time(todays_timeslots[i*2].split('-')[0])
    right_x = get_x_from_time(todays_timeslots[i*2].split('-')[1])

    # Create a rectangle for each lesson
    rectangles.append(canvas.create_rectangle(left_x, 2, right_x, 40, fill=settings['lesson_color']))

    # Create texts for lesson numbers and lesson titles
    canvas.create_text(center_x, 10, text='{}. Ders'.format(i+1), fill='black', font='calibri 14')
    canvas.create_text(center_x, 30, text=todays_lessons[i], fill='black', font='calibri 18 bold')

    # Create texts for lesson starting time on the left and lesson ending time on the right of rectangles 
    canvas.create_text(left_x + 20, 32, text=todays_timeslots[i*2].split('-')[0], fill='black', font='calibri 12')
    canvas.create_text(right_x - 20, 32, text=todays_timeslots[i*2].split('-')[1], fill='black', font='calibri 12')

    # Create a rectangle for each break
    if i < lessons_per_day - 1:
        rectangles.append(canvas.create_rectangle(get_x_from_time(todays_timeslots[i*2+1].split('-')[0]), 2, get_x_from_time(todays_timeslots[i*2+1].split('-')[1]), 40, fill=settings['break_color']))
    

completed_lesson_break_count = 0
last_completed_rectangle_x1 = 0
last_lesson_finished = False
first_run = True

time()

form.mainloop()