from bs4 import BeautifulSoup
import requests
import json
import copy

fallCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm"
springCourseUrl = "https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm"

class Webscrapers():
    @staticmethod  
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

    @staticmethod
    def updateEceAreaCourses(tag, areaOrder, req):
        requirements = {'DeviceSciences': list(),
            'SignalsAndSystems': list(),
            'Circuits': list(),
            'HardwareSystems': list(),
            'SoftwareSystems': list()}
        if (req == 'coverage'): 
            requirements['UndergraduateProjects'] = list()
            requirements['ProfessionalPolicy'] = list()
        areaTables = tag.findAll('table')
        for i in range(len(areaTables)):
            area = areaOrder[i]
            for row in areaTables[i].findAll('tr'):
                cells = row.findAll('td')
                course_id = cells[0].getText().replace('-', '')
                if course_id.isdigit(): 
                    requirements[area].append(course_id)
        return requirements

    @staticmethod
    def eceCourseUpdate():
        # with open("courseList.json", "r") as courses:
        #     allCourses = json.load(courses)
        #     courses.close()
        # allCourses["Requirements"]["CIT"]["ECE"] = dict()
        ece = dict()
        eceUrl = "https://ece.cmu.edu/programs-admissions/bachelors/academic-guide"
        page = requests.get(eceUrl)
        soup = BeautifulSoup(page.text, "html.parser")
        for tag in soup.find_all('div', class_ = "accordion-inner"):
            if (tag['id'] == 'Area-Requirements'):
                areaOrder = ['DeviceSciences', 'SignalsAndSystems', 'Circuits',
                    'HardwareSystems', 'SoftwareSystems']
                ece['Area-Requirements'] = (
                    Webscrapers.updateEceAreaCourses(tag, areaOrder, 'area'))
            if (tag['id'] == 'Coverage-Requirement'):
                areaOrder = ['DeviceSciences', 'Circuits', 'HardwareSystems', 
                    'SoftwareSystems', 'ProfessionalPolicy', 
                    'SignalsAndSystems', 'UndergraduateProjects']
                ece['Coverage-Requirement'] = (
                    Webscrapers.updateEceAreaCourses(tag, areaOrder, 
                    'coverage'))
        print(ece)
            



                    

