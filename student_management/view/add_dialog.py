from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QSpinBox, QLabel
from student_management.model.student import Student


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить студента')
        self.layout = QVBoxLayout()

        self.fio_input = QLineEdit()
        self.group_input = QLineEdit()
        self.exams_layout = QVBoxLayout()
        self.exams = []

        self.layout.addWidget(QLabel('ФИО:'))
        self.layout.addWidget(self.fio_input)
        self.layout.addWidget(QLabel('Группа:'))
        self.layout.addWidget(self.group_input)
        self.layout.addWidget(QLabel('Экзамены:'))
        self.layout.addLayout(self.exams_layout)

        self.add_exam_btn = QPushButton('Добавить экзамен')
        self.add_exam_btn.clicked.connect(self.add_exam)
        self.layout.addWidget(self.add_exam_btn)

        self.ok_btn = QPushButton('OK')
        self.ok_btn.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_btn)

        self.setLayout(self.layout)
        self.add_exam()

    def add_exam(self):
        exam_layout = QHBoxLayout()
        name_input = QLineEdit()
        score_input = QSpinBox()
        score_input.setRange(0, 100)
        exam_layout.addWidget(QLabel('Предмет:'))
        exam_layout.addWidget(name_input)
        exam_layout.addWidget(QLabel('Балл:'))
        exam_layout.addWidget(score_input)
        self.exams_layout.addLayout(exam_layout)
        self.exams.append((name_input, score_input))

    def get_student(self):
        exams = [
            {'name': name.text(), 'score': score.value()}
            for name, score in self.exams if name.text() and score.value() >= 0
        ]
        return Student(self.fio_input.text(), self.group_input.text(), exams)