#!/usr/bin/env python3

# Write a series of Python classes to model students, professors, course, classes, and majors.
# Implement as many of the magic methods as make sense for your model. Submit a git repo with a readme describing how to use your classes.
# I will leave the specifics up to you but you should implement things like add/drop class, get_advisor/advisee, 
# course requirements, major requirements.
# Note that a class is a specific term offering of a course which is a more general description.
# Because it is so open ended, I am offering up to 20% extra credit (this is your golden parachute for those of you who 
# have been less than studious). The standard for 10% extra credit would be a barebones model with a readme ~100-150 lines of code.
#  20% would include a full demo and documentation ~500+ lines of code.

class Human:
  """The basic necessary attributes of a human being"""
  percentHealth = 100
  percentEnthusiasm = 50
  percentAnger = 0
  percentHappiness = 50
  percentStress = 0
  percentHunger = 0
  knowledge = {}

  def __init__(self, name):
    self.name = name

  # Helper to simplify the logic of messages to three possible states
  def triState(self, value, lowMsg, medMsg, highMsg, lowThold = 33, highThold = 67):
      if value < lowThold:
        return lowMsg
      elif value > highThold:
        return highMsg
      else:
        return medMsg
  
  def getHealth(self):
    return self.triState(self.percentHealth, "nearly dead", "unhealthy", "healthy")
  def getEnthusiasm(self):
    return self.triState(self.percentEnthusiasm, "bored", "intrigued", "enthusiastic")
  def getAnger(self):
    return self.triState(self.percentAnger, "mellow", "angry", "raging")
  def getHappiness(self):
    return self.triState(self.percentHappiness, "depressed", "neutral", "happy")
  def getStress(self):
    return self.triState(self.percentStress, "relaxed", "anxious", "stressed")
  def getHunger(self):
    return self.triState(self.percentHunger, "well-fed", "hungry", "starving")
  
  def __str__(self):
    knows = "absolutely nothing"
    if self.knowledge != {}:
      knows = str(self.knowledge)
    return f"<A {self.getHealth()}, {self.getEnthusiasm()}, {self.getAnger()}, {self.getHappiness()}, {self.getStress()}, {self.getHunger()} {self.__class__.__name__} named {self.name}, who knows {knows}>"

  def __repr__(self):
    return f"<{self.__class__.__name__} avec les attributs: Health: {self.percentHealth}%, Enthusiasm: {self.percentEnthusiasm}%, Anger: {self.percentAnger}%, Happiness: {self.percentHappiness}%, Stress: {self.percentStress}%, Hunger: {self.percentHunder}%, Knowledge: {str(self.knowledge)}"

#class Worker(Human):
#  hrsFreetime = 0
#  def __init__(self, name, affiliation):
#    super(Worker, self).__init__(name)





# A professor
class Professor(Human):
  def __init__(self, name):
    super(Professor, self).__init__(name)


class ClassOffering:
  prerequisites = [] # A list of other course prerequisites to this course
  def __init__(self, code, name, professor: Professor):
    self.professor = professor
    self.code = code
    self.name = name

  def getPrerequisites(self):
    return self.prerequisites

  def getCode(self):
    return self.code

  def getName(self):
    return self.name

  # Override eq to make courses equivalent to class offerings
  def __eq__(self, other):
    if isinstance(other, Course) or isinstance(other, ClassOffering):
      return self.name == other.name and self.code == other.code and self.professor == other.professor

  def __str__(self):
    return "<Class: " + self.getCode() + ": " + self.getName() + ", taught by " + str(self.professor) + ">"
  
  def __repr__(self):
    return self.__str__()



# A course is a physical course that can be taken by students
class Course(ClassOffering):
  enrolledStudents = [] # A list of all students currently enrolled
  def __init__(self, code, name, professor: Professor):
    super(Course, self).__init__(code, name, professor)

  # Adds a prerequisite to this course
  def addPrerequisite(self, offering: ClassOffering):
    self.prerequisites.append(offering)

  # Returns a list of all students currently enrolled in the course
  def getEnrolledStudents(self):
    return self.enrolledStudents

  # Converts this course into a ClassOffering
  def toClassOffering(self):
    return ClassOffering(self.code, self.name, self.professor)

  # Returns a summary of the course
  def __str__(self):
    return "<Course: " + self.getCode() + ": " + self.getName() + ", " + str(len(self.enrolledStudents)) + " enrolled students, " + str(len(self.prequisites)) + " prerequisites>"
  
  # Returns a summary of the course, listing all enrolled students and prerequisites
  def __repr__(self):
    return "<Course: " + self.getCode() + ": " + self.getName() + ", enrolled students: [" + str(self.enrolledStudents) + "], prerequisites: [" + str(self.prequisites) + "]>"



class Major:
  """A major that students can declare"""
  courseRequirements = []
  def __init__(self, name):
    self.name = name
  
  def addCourseRequirement(self, course: ClassOffering):
    self.courseRequirements.append(course)

  def getCourseRequirements(self):
    return self.courseRequirements

  def __str__(self):
    return "<Major: " + self.name + ", requirements: " + str(self.courseRequirements) + ">"

  def __repr__(self):
    return self.__str__()



class Student(Human):
  completedCourses = [] # A history of courses that this student has completed (as ClassOfferings)
  enrolledCourses = [] # Courses currently entrolled
  major = None
  def __init__(self, name, advisor):
    super(Student, self).__init__(name)
    self.advisor = advisor
    self.advisor.addAdvisee(self)

  def __del__(self):
    if self.advisor is not None:
      if self in self.advisor.advisees:
        self.advisor.advisees.remove(self)

  # Returns completed courses, as ClassOfferings
  def getCompletedCourses(self):
    return self.completedCourses

  # Returns enrolled courses, as Courses
  def getEnrolledCourses(self):
    return self.enrolledCourses

  def declareMajor(self, major: Major):
    self.major = major

  def getAdvisor(self):
    return self.advisor

  # Returns true if the student has met all requirements for graduation
  def canGraduate(self):
    if self.major == None:
      return False
    for requirement in self.major.getCourseRequirements():
      if not requirement in self.completedCourses:
        return False
    return True

  # Tells the student to do math. Increases stress by 5 times the number of problems, and decreases health by the number of problems.
  def doMath(self, numProblems):
    self.percentStress = min(100, self.percentStress + numProblems * 5)
    self.health = max(0, self.health - numProblems)

  # Tells the student to do CS. Decrerases stress and increases happiness, optionally by linesOfCode (okay, maybe not totally realistic if trying to keep integer compatibility)
  def doComputerScience(self, linesOfCode = 10):
    self.percentStress = max(0, self.percentStress - linesOfCode)
    self.percentHappiness = min(100, self.percentHappiness + linesOfCode)

  def __str__(self):
    print(super().__str__()[0:-2] + ", major: " + self.major)

  def __repr__(self):
    print(super().__repr__()[0:-2] + ", major: " + self.major)



class Advisor(Human):
  """An advisor can manage a student's course schedule"""
  advisees = []
  def __init__(self, name):
    super(Advisor, self).__init__(name)

  def getAdvisees(self):
    return self.advisees

  def addAdvisee(self, student: Student):
    self.advisees.append(student)

  def enrollStudent(self, student: Student, course: Course):
    # Check prerequisites
    for prereq in course.getPrerequisites():
      if not prereq in student.completedCourses:
        raise LookupError("Student " + str(student) + "cannot take course " + str(course) + ": Unsatisfied prerequisite " + str(prereq))
    course.enrolledStudents.append(student)
    student.enrolledCourses.append(course)

  def disenrollStudent(student: Student, course: Course):
    try:
      course.enrolledStudents.remove(student)
      student.enrolledCourses.remove(course)
    except ValueError as e:
      raise ValueError("Student not currently enrolled in course " + str(course))




class Term:
  """A physical school term as a period of time global to Knox College. Runs a simulation of the term for all courses, students and professors. Prints all output."""
  courses = {}
  def __init__(self):
    pass

  # Adds a course to be offered and run in this term
  def addCourse(self, course: Course):
    self.courses[course.getCode()] = course
  #def addCourse(self, code, name, professor: Professor):
  #  self.courses[code] = Course(code, name, professor)
    
  # Retrieves a course by its code
  def getCourse(self, code):
    return self.courses[code]

  def run(self):
    pass # TODO

  # Concludes this term as complete, and clears / saves all course data
  def conclude(self):
    for course in self.courses:
      for student in course.getEnrolledStudents():
        for course in student.getEnrolledCourses(): # Save all students' courses in the student's history
          student.completedCourses.append(course.toClassOffering())
        student.getAdvisor().disenrollStudent(student, course) # Ask the student's advisor to disenroll them from all courses


def main():
  advisor = Advisor("Bunde")
  stu = Student("John", advisor)
  course = Course("CS208", "Programming Languages", Professor("Bose"))
  course.addPrerequisite(ClassOffering("CS142", "Intro to Algorithms", "Spacco"))
  advisor.enrollStudent(stu, course)

  term = Term()
  term.addCourse(course)
  term.run()
  term.conclude()


if __name__ == "__main__":
  main()