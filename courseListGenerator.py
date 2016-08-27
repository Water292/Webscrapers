from bs4 import BeautifulSoup
import requests
import json

fallCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm"
springCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm"

def updateCourseList(semester):
    with open("courseList.json", "r") as courses:
        allCourses = json.load(courses)
        courses.close()
    semesterCourses = list()
    url = fallCourseUrl if semester.startswith("fall") else springCourseUrl
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for row in soup.find_all("tr"):
        cells = row.findAll('td')
        course_id = cells[0].getText() 
        if course_id.isdigit(): semesterCourses.append(course_id) 
    allCourses[semester] = semesterCourses
    with open("courseList.json", "w") as courses:
        courses.write(json.dumps(allCourses, indent = 2))
        courses.close()
