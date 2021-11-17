# This is a ecording script to record Maths' lessons

#The script will parse ics calendar and make crons job accordly.

# https://icspy.readthedocs.io/en/stable/

#Import a calendar from a file
import os
from ics import Calendar
from crontab import CronTab
from datetime import date
from functions import listToString,CheckCoursesList
import configparser


#Il nostro Timezone è UTC+1, quindi aggiungo 1 alle varie date di gcal
TimeZome=1

# read user info
config = configparser.ConfigParser()
config.read('config.ini')

calendar = os.path.join("CALs","mycal_nov.ics")

with open (calendar, "r") as myfile:
    data=myfile.readlines()

strcal = listToString(data)

c= Calendar(strcal)

#OBS USER
cron = CronTab(user=config['Account']['user'])

# schedule OBS RECORDING EVENT
for i in range(len(c.events)):
    e = list(c.timeline)[i]

    dtoday = date.today()
    if str(dtoday) == str(e.begin.format('YYYY-MM-DD')):
        # if 'ANALISI'in str(e.name):
        #     print('ok')

        if CheckCoursesList(str(e.name)) == True:

            #CREAZIONE JOB RECORDING
            job = cron.new(command="export DISPLAY=:0 && obs -m --startrecording #DYNAMIC START- '{}'".format(e.name))
            job.day.on(str(dtoday.day))
            job.month.on(str(dtoday.month))
            job.hour.on(str(int(e.begin.format('HH'))+TimeZome))
            job.minutes.on(e.begin.format('mm'))
            cron.write()


            # CREAZIONE JOB STOP RECORDING
            job = cron.new(command="killall obs #DYNAMIC STOP- '{}'".format(e.name))
            job.day.on(str(dtoday.day))
            job.month.on(str(dtoday.month))
            job.hour.on(str(int(e.end.format('HH'))+TimeZome))
            job.minutes.on(e.end.format('mm'))
            cron.write()




