# AutoRecording

This script records my Maths' lessons with OBS/crontab.
The script will parse ics calendar and make crons job accordly, calendar must be named "mycal.ics" and must be located into a 'CALs' folder.  
Ref https://icspy.readthedocs.io/en/stable/


AutoRecording run  with AutoClassJoiner ( https://github.com/GoldenbyteGH/AutoClassJoiner ) executed simultaneously by crontab

Example

`
0 1 * * * /bin/bash ClassRecorder.sh & #STATIC_PYTHON_CRON_CLEANER
mm1 HH DD MM * export DISPLAY=:1 && XDG_RUNTIME_DIR=/run/user/1000 obs --startrecording --minimize-to-tray #DYNAMIC START- 'FISICA GENERALE I'
mm2 HH DD MM * export DISPLAY=:1 && /bin/bash ClassJoiner.sh #DYNAMIC JOIN - 'FISICA GENERALE I'
mm3 HH DD MM * killall obs #DYNAMIC STOP- 'FISICA GENERALE I'
`

Crontab file is rewrited every day at 01:00 by ClassRecorder.sh.

Other jobs are scheduled based calendar.ics and LinkCourses.json


ClassRecorder.sh simply contain
`
/venv_path/bin/python /project_path/AutoRecording/main.py
`
