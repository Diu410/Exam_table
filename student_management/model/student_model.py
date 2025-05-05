import xml.dom.minidom as minidom
import xml.sax
from .student import Student

class StudentModel:
    def __init__(self):
        self.students = []
        self.groups = set()
        self.subjects = set()

    def add_student(self, student):
        self.students.append(student)
        self.groups.add(student.group)
        for exam in student.exams:
            self.subjects.add(exam['name'])

    def remove_students(self, condition):
        initial_count = len(self.students)
        self.students[:] = [s for s in self.students if not condition(s)]
        removed_count = initial_count - len(self.students)
        self.update_metadata()
        return removed_count

    def search_students(self, condition):
        return [s for s in self.students if condition(s)]

    def update_metadata(self):
        self.groups = set(s.group for s in self.students)
        self.subjects = set()
        for s in self.students:
            for exam in s.exams:
                self.subjects.add(exam['name'])

    def save_to_xml(self, filename):
        doc = minidom.Document()
        root = doc.createElement('students')
        doc.appendChild(root)
        for student in self.students:
            student_elem = doc.createElement('student')
            student_elem.setAttribute('fio', student.fio)
            student_elem.setAttribute('group', student.group)
            for exam in student.exams:
                exam_elem = doc.createElement('exam')
                exam_elem.setAttribute('name', exam['name'])
                exam_elem.setAttribute('score', str(exam['score']))
                student_elem.appendChild(exam_elem)
            root.appendChild(student_elem)
        with open(filename, 'w', encoding='utf-8') as f:
            doc.writexml(f, indent='  ', addindent='  ', newl='\n')

    def load_from_xml(self, filename):
        class StudentHandler(xml.sax.ContentHandler):
            def __init__(self, model):
                super().__init__()
                self.model = model
                self.current_student = None
                self.current_exam = None
                self.current_tag = None

            def startElement(self, tag, attrs):
                self.current_tag = tag
                if tag == 'student':
                    self.current_student = {'fio': attrs['fio'], 'group': attrs['group'], 'exams': []}
                elif tag == 'exam':
                    self.current_exam = {'name': attrs['name'], 'score': int(attrs['score'])}

            def endElement(self, tag):
                if tag == 'student':
                    self.model.add_student(Student(
                        self.current_student['fio'],
                        self.current_student['group'],
                        self.current_student['exams']
                    ))
                    self.current_student = None
                elif tag == 'exam':
                    self.current_student['exams'].append(self.current_exam)
                    self.current_exam = None
                self.current_tag = None

        self.students.clear()
        parser = xml.sax.make_parser()
        parser.setContentHandler(StudentHandler(self))
        parser.parse(filename)
        self.update_metadata()