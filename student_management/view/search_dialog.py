from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QSpinBox, QLabel, QTableWidget, \
    QTableWidgetItem


class SearchDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle('Поиск')
        self.layout = QVBoxLayout()

        self.search_type = QComboBox()
        self.search_type.addItems(['По среднему баллу', 'По группе', 'По баллу и предмету'])
        self.layout.addWidget(self.search_type)

        self.params_layout = QVBoxLayout()
        self.layout.addLayout(self.params_layout)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['ФИО', 'Группа', 'Экзамены'])
        self.layout.addWidget(self.result_table)

        self.search_btn = QPushButton('Поиск')
        self.search_btn.clicked.connect(self.search)
        self.layout.addWidget(self.search_btn)

        self.setLayout(self.layout)
        self.search_type.currentIndexChanged.connect(self.update_params)
        self.update_params()

    def update_params(self):
        for i in reversed(range(self.params_layout.count())):
            self.params_layout.itemAt(i).widget().deleteLater()

        idx = self.search_type.currentIndex()
        if idx == 0:  # По среднему баллу
            self.min_avg = QSpinBox()
            self.min_avg.setRange(0, 100)
            self.max_avg = QSpinBox()
            self.max_avg.setRange(0, 100)
            self.params_layout.addWidget(QLabel('Мин. средний балл:'))
            self.params_layout.addWidget(self.min_avg)
            self.params_layout.addWidget(QLabel('Макс. средний балл:'))
            self.params_layout.addWidget(self.max_avg)
        elif idx == 1:  # По группе
            self.group_combo = QComboBox()
            self.group_combo.addItems(sorted(self.model.groups))
            self.params_layout.addWidget(QLabel('Группа:'))
            self.params_layout.addWidget(self.group_combo)
        elif idx == 2:  # По баллу и предмету
            self.subject_combo = QComboBox()
            self.subject_combo.addItems(sorted(self.model.subjects))
            self.min_score = QSpinBox()
            self.min_score.setRange(0, 100)
            self.max_score = QSpinBox()
            self.max_score.setRange(0, 100)
            self.params_layout.addWidget(QLabel('Предмет:'))
            self.params_layout.addWidget(self.subject_combo)
            self.params_layout.addWidget(QLabel('Мин. балл:'))
            self.params_layout.addWidget(self.min_score)
            self.params_layout.addWidget(QLabel('Макс. балл:'))
            self.params_layout.addWidget(self.max_score)

    def search(self):
        idx = self.search_type.currentIndex()
        if idx == 0:  # По среднему баллу
            min_avg = self.min_avg.value()
            max_avg = self.max_avg.value()
            condition = lambda s: min_avg <= s.average_score() <= max_avg
        elif idx == 1:  # По группе
            group = self.group_combo.currentText()
            condition = lambda s: s.group == group
        elif idx == 2:  # По баллу и предмету
            subject = self.subject_combo.currentText()
            min_score = self.min_score.value()
            max_score = self.max_score.value()
            condition = lambda s: any(
                exam['name'] == subject and min_score <= exam['score'] <= max_score for exam in s.exams)

        results = self.model.search_students(condition)
        self.result_table.setRowCount(len(results))
        for i, student in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(student.fio))
            self.result_table.setItem(i, 1, QTableWidgetItem(student.group))
            exams_str = '; '.join(f"{e['name']}: {e['score']}" for e in student.exams)
            self.result_table.setItem(i, 2, QTableWidgetItem(exams_str))