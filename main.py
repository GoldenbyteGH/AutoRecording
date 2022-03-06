# This is a ecording script to record Maths' lessons

#The script will parse ics calendar and make crons job accordly.

# https://icspy.readthedocs.io/en/stable/
#https://obsproject.com/forum/threads/run-obs-and-start-streaming-automatically-audio-not-captured.150336/

#Import a calendar from a file
import json
import os
from ics import Calendar
from crontab import CronTab
from datetime import date
from functions import listToString,CheckCoursesList
import configparser


#UTC+1 -> Italy
TimeZome=1

if __name__ == '__main__':
    # read user info
    config = configparser.ConfigParser()
    config.read('/project_path/AutoRecording/config.ini')

    lessons_list=[]

    calendar = os.path.join("/project_path/AutoRecording/CALs","my_cal_50322.ics")

    with open (calendar, "r") as myfile:
        data=myfile.readlines()

    strcal = listToString(data)

    c= Calendar(strcal)
    #OBS USER
    cron = CronTab(user=config['Account']['user'])

    # CRONTAB CLEAN
    cron.remove_all()
    job = cron.new(command="/bin/bash ClassRecorder.sh & #STATIC_PYTHON_CRON_CLEANER")
    job.minutes.on('00')
    job.hour.on('01')
    cron.write()


    # schedule OBS RECORDING EVENT
    for i in range(len(c.events)):
        e = list(c.timeline)[i]

        dtoday = date.today()
        if str(dtoday) == str(e.begin.format('YYYY-MM-DD')):

            if CheckCoursesList(str(e.name)) == True:

                #JOB RECORDING
                job = cron.new(command="export DISPLAY=:1 && XDG_RUNTIME_DIR=/run/user/1000 obs --startrecording #DYNAMIC START- '{}'".format(e.name))
                job.day.on(str(dtoday.day))
                job.month.on(str(dtoday.month))
                job.hour.on(str(int(e.begin.format('HH'))+TimeZome))
                job.minutes.on(e.begin.format('mm'))

                #JOB JOIN LESSON
                job = cron.new(command="export DISPLAY=:1 && /bin/bash ClassJoiner.sh #DYNAMIC JOIN - '{}'".format(e.name))
                job.day.on(str(dtoday.day))
                job.month.on(str(dtoday.month))
                job.hour.on(str(int(e.begin.format('HH'))+TimeZome))
                job.minutes.on(str(int(e.begin.format('mm'))+1))        # avoid simultaneous jobs


                cron.write()
                # JOB STOP RECORDING
                job = cron.new(command="killall obs #DYNAMIC STOP- '{}'".format(e.name))
                job.day.on(str(dtoday.day))
                job.month.on(str(dtoday.month))
                job.hour.on(str(int(e.end.format('HH'))+TimeZome))
                job.minutes.on(e.end.format('mm'))
                cron.write()

                lesson_dict = {
                    "name": e.name,
                    "hour_start_time": str(int(e.begin.format('HH'))+TimeZome),
                    "minutes_start_time": e.begin.format('mm'),
                    "hour_end_time": str(int(e.end.format('HH'))+TimeZome),
                    "end_start_time": e.end.format('mm'),
                }
                lessons_list.append(lesson_dict)
                # LOG
                print("Cron salvato ->'{}'".format(e.name))

    with open(os.path.join(config['Account']['AutoClassJoiner_path'],'Classes_TMP_file.json'),'w') as outfile:
        json.dump(lessons_list,outfile)

    outfile.close()
