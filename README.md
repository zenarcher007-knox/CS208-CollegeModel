# CS208-CollegeModel

This is a collection of classes that can simulate the structure of Knox College. There are students, professors, majors, terms, advisors, and courses.  
All people derive from subclass Human, as all peole are really humans and have feelings, etc.  

The typical usage is to create an advisor, assign the advisor for students, ask the advisor to enroll students into courses, add the courses to a term, and run the term.

```
  advisor = Advisor("Bunde")
  stu = Student("John", advisor)
  course = Course("CS208", "Programming Languages", Professor("Bose"))
  course.addPrerequisite(ClassOffering("CS142", "Intro to Algorithms", "Spacco"))
  advisor.enrollStudent(stu, course)

  term = Term()
  term.addCourse(course)
  term.run()
  term.conclude()
```  

When ```term.conclude()``` is called, the courses that all students are taking are saved in their course history, and can be used for entry to other courses with prerequisites. If a student has declared a major, calling ```stu.canGraduate()``` returns True if they have met their major's requirements for graduation.

<sub><sup>***Please note that the code may have minor errrors, as I was really short on time***</sup></sub>
