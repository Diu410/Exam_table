from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QSpinBox, QLabel, QMessageBox


class DeleteDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle('Удаление')
        self.layout = QVBoxLayout()

        self.delete_type = QComboBox()
        self.delete_type.addItems(['По среднему баллу', 'По группе', 'По баллу и предмету'])
        self.layout.addWidget(self.delete_type)

        self.params_layout = QVBoxLayout()
        self.layout.addLayout(self.params_layout)

        self.delete_btn = QPushButton('Удалить')
        self.delete_btn.clicked.connect(self.delete)
        self.layout.addWidget(self.delete_btn)

        self.setLayout(self.layout)
        self.delete_type.currentIndexChanged.connect(self.update_params)
        self.update_params()

    def update_params(self):
        for i in reversed(range(self.params_layout.count())):
            self.params_layout.itemAt(i).widget().deleteLater()

        idx = self.delete_type.currentIndex()
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

    def delete(self):
        idx = self.delete_type.currentIndex()
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

        removed_count = self.model.remove_students(condition)
        QMessageBox.information(self, 'Результат', f'Удалено записей: {removed_count}')
        self.accept()