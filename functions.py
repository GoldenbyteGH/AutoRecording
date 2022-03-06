import yaml
from re import search

#Function to check yaml file
def CheckCoursesList(course):


    with open("/project_path/AutoRecording/courses.yaml", 'r') as c:
        out = yaml.load(c, Loader=yaml.FullLoader)
    for item in out['CoursesToRecord']['courses']:
        if search(item,course):
            return True
        else:
            continue

# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1
