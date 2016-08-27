from bs4 import BeautifulSoup
import requests

fall = list()

fallCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm"
fallCoursePage = requests.get(fallCourseUrl)

soup = BeautifulSoup(fallCoursePage.text, "html.parser")

for row in soup.find_all("tr"):
    cells = row.findAll('td')
    course_id = cells[0].getText() 
    if course_id.isdigit(): fall.append(course_id)

class Webscraper(object):
    def __init__(self):
        self.fallCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm"
        self.springCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm"
