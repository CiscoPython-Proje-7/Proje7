from tkinter import * 
from tkinter.ttk import *
from win32api import GetMonitorInfo, MonitorFromPoint
from time import strftime
from datetime import datetime

def time():
    # Get the time in HH:MM:SS format
    current_time = strftime('%H:%M:%S')

    # Display the time
    canvas.itemconfigure(text_current_time, text=current_time)

    # Get the current time
    # current_date_time = datetime.strptime(current_date + current_time, '%Y-%m-%d %H:%M:%S')

    global last_lesson_finished

    # If the last lesson is not finished
    if not last_lesson_finished:

        # Calculate the total number of seconds since the start of the first lesson
        estimated_total_seconds = int((datetime.now() - first_lesson_starting_time).total_seconds())

        # Calculate and display progress bar for current time
        progress_bar_size = (estimated_total_seconds / total_school_day_seconds) * timeline_size
        x0, y0, x1, y1 = canvas.coords(progress_bar)
        x1 = x0 + progress_bar_size 
        canvas.coords(progress_bar, x0, y0, x1, y1)

        # Loop for each lesson and break rectangles
        for rectangle in rectangles:
            rx0, ry0, rx1, ry1 = canvas.coords(rectangle)
            global last_completed_rectangle_x1

            # Make the last finished lesson/break gray
            if x1 > rx1 and rx1 > last_completed_rectangle_x1:
                canvas.itemconfigure(rectangle, fill='#505050')
                global completed_lesson_break_count
                completed_lesson_break_count += 1
                last_completed_rectangle_x1 = rx1
                if completed_lesson_break_count == len(todays_timeslots):
                    last_lesson_finished = True
                    break

            # Get the current lesson or breaks ending time
            end_time = datetime.strptime(current_date + todays_timeslots[completed_lesson_break_count].split('-')[1], '%Y-%m-%d %H:%M')

            # Calculate the remaining seconds for the lesson or break
            remaining_seconds = int((end_time - datetime.now()).total_seconds()) + 1

            # Display remaining time in MM:SS format
            remaining_time_text ='{:02}:{:02}'.format(remaining_seconds % 3600 // 60, remaining_seconds % 60)
            canvas.itemconfigure(text_remaining_time, text=remaining_time_text)

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

form = Tk()

# This function can be used for closing the app
def close_program():
    form.destroy()

# Prevent app closing
def disable_event():
    pass

# Make window allways on top and make it black and transparent
form.protocol("WM_DELETE_WINDOW", disable_event)
form.wm_attributes("-topmost", 1)
form.wm_attributes("-alpha", 0.7)
form['bg'] = 'black'

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

canvas = Canvas(form, width=window_width - 4, height=window_height - 2, background='black', highlightthickness=0)
canvas.pack()

# Create text for displaying remaining time on the left and current time on the right of timeline
top_margin = 24
text_remaining_time = canvas.create_text(64, top_margin, fill='red', font='calibri 42 bold')
text_current_time = canvas.create_text(window_width-104, top_margin, fill='white', font='calibri 42 bold')

todays_lessons = ['MAT', 'MAT', 'MAT', 'PTM', 'PTM', 'PTM', 'COG', 'COG']
todays_timeslots = ['8:00-8:40',
                    '8:40-8:50', 
                    '8:50-9:30', 
                    '9:30-9:40', 
                    '9:40-10:20',
                    '10:20-10:30',  
                    '10:30-11:10', 
                    '11:10-11:20', 
                    '11:20-12:00', 
                    '12:00-13:00', 
                    '13:00-13:40', 
                    '13:40-13:50', 
                    '13:50-14:30', 
                    '14:30-14:40', 
                    '14:40-15:20']

# todays_lessons = ['PTM', 'PTM', 'PTM']
# todays_timeslots = ['18:50-19:30',
#                     '19:30-19:40', 
#                     '19:40-20:20', 
#                     '20:20-20:30', 
#                     '20:30-21:10']

# Get current date in YY-MM-DD format
current_date = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day) + ' '

# Get the number of lessons per day and set timeline coords
lessons_per_day = len(todays_lessons)
timeline_left_x = 134
timeline_right_x = 1718
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
    rectangles.append(canvas.create_rectangle(left_x, 2, right_x, 40, fill='#e8505b'))

    # Create texts for lesson numbers and lesson titles
    canvas.create_text(center_x, 10, text='{}. Ders'.format(i+1), fill='black', font='calibri 14')
    canvas.create_text(center_x, 30, text=todays_lessons[i], fill='black', font='calibri 18 bold')

    # Create texts for lesson starting time on the left and lesson ending time on the right of rectangles 
    canvas.create_text(left_x + 20, 32, text=todays_timeslots[i*2].split('-')[0], fill='black', font='calibri 12')
    canvas.create_text(right_x - 20, 32, text=todays_timeslots[i*2].split('-')[1], fill='black', font='calibri 12')

    # Create a rectangle for each break
    if i < lessons_per_day - 1:
        rectangles.append(canvas.create_rectangle(get_x_from_time(todays_timeslots[i*2+1].split('-')[0]), 2, get_x_from_time(todays_timeslots[i*2+1].split('-')[1]), 40, fill='#bac964'))
    

completed_lesson_break_count = 0
last_completed_rectangle_x1 = 0
last_lesson_finished = False

time()

form.mainloop()