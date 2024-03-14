from utils.helpers import getProvince
# -----------------------
# Senior Software Developer
# Sandman Software Systems Inc.
# Quezon City, Philippines
# ₱30,000.00 - ₱40,000.00 / month
# Full time
# Remote
# Recruiter was hiring 5 hours ago
# Apply before 30 Jan
# Associate / Supervisor
# -----------------------
# Software Developer Intern
# Likha-iT Inc.
# Makati, Philippines
# Salary Undisclosed
# Full time
# Recruiter was hiring 5 days ago
# Apply before 29 Apr
# Internship / OJT
# -----------------------

# normalizedData:dict = {
#     "job_title" : "Software Developer Intern",
#     "location" : "Makati, Philippines",
#     "salary" : "Salary Undisclosed",
#     "job_level" : "Internship / OJT",
#     "employment_type" : "Full time",
# }

# normalizedData:dict = {
#     "job_title" : "Senior Software Developer",
#     "location" : "Quezon City, Philippines",
#     "salary" : "₱30,000.00 - ₱40,000.00 / month",
#     "job_level" : "Associate / Supervisor",
#     "employment_type" : "Full time",
# }

def normalizeData(stringData:str):
    normalizedData:dict = {
        "job_title":"",
        "location":"",
        "salary":"",
        "job_level":"",
        "employment_type":"",
    }
    dataList = stringData.splitlines()
    for index,data in enumerate(dataList):
        if(index == 0):
            normalizedData["job_title"] = data
        elif(index == 2):
            normalizedData["location"] = getProvince(data) 
        elif(index == 3):
            normalizedData["salary"] = data
        elif(index ==4):
            normalizedData["employment_type"] = data
        elif(index == len(dataList)-1):
            normalizedData["job_level"] = data
    return normalizedData;
    
