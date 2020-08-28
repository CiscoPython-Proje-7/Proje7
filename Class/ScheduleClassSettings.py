import json

class ScheduleClassSettings:
    def __init__(self):
        with open('schedule_class_settings.json') as json_file:
            self.settings = json.load(json_file)

    def getSetting(self, key):
        return self.settings[key]

def getSetting(key):
    with open('schedule_class_settings.json') as json_file:
        settings = json.load(json_file)
    return settings[key]

def getSettings():
    with open('schedule_class_settings.json') as json_file:
        settings = json.load(json_file)
    return settings

def setSettings(key, value, secondKey=False):
    settings = getSettings()
    if secondKey:
        settings[key][secondKey] = value
    else:
        settings[key] = value
    with open('schedule_class_settings.json', 'w') as json_file:
        json_file.write(json.dumps(settings))

# Default Settings
# {
#     "form_background": "black", 
#     "form_transparency": 0.7, 
#     "class_name_font_style": "calibri 18 bold", 
#     "class_name_font_color": "#e84a5f", 
#     "remaining_time_font_style": "calibri 18 bold", 
#     "remaining_time_font_color": "white", 
#     "day_name_font_style": "calibri 18 bold", 
#     "day_name_font_color": "#e84a5f",
#     "curent_time_font_style": "calibri 18 bold", 
#     "curent_time_font_color": "white",
#     "finished_lesson_color": "#4a4a4a", 
#     "finished_break_color": "#505050", 
#     "lesson_color": "#fd5e53",
#     "break_color": "#8cba51",
#     "selected_class": "9-A",
#     "time_offset": -8,
#     "day_offset": 0
# }
