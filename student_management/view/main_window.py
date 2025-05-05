from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QDockWidget, QWidget,
                             QHBoxLayout, QPushButton, QSpinBox, QLabel, QAction, QToolBar)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setWindowTitle('Система управления студентами')
        self.setGeometry(100, 100, 800, 600)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ФИО', 'Группа', 'Экзамены'])
        self.setCentralWidget(self.table)

        # Пагинация
        self.pagination_layout = QHBoxLayout()
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.per_page_spin = QSpinBox()
        self.per_page_spin.setRange(1, 50)
        self.per_page_spin.setValue(10)
        self.total_label = QLabel()
        self.first_btn = QPushButton('Первая')
        self.prev_btn = QPushButton('Предыдущая')
        self.next_btn = QPushButton('Следующая')
        self.last_btn = QPushButton('Последняя')

        self.pagination_layout.addWidget(QLabel('Страница:'))
        self.pagination_layout.addWidget(self.page_spin)
        self.pagination_layout.addWidget(QLabel('Записей на странице:'))
        self.pagination_layout.addWidget(self.per_page_spin)
        self.pagination_layout.addWidget(self.first_btn)
        self.pagination_layout.addWidget(self.prev_btn)
        self.pagination_layout.addWidget(self.next_btn)
        self.pagination_layout.addWidget(self.last_btn)
        self.pagination_layout.addWidget(self.total_label)

        self.dock = QDockWidget()
        self.dock.setWidget(QWidget())
        self.dock.widget().setLayout(self.pagination_layout)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)

        # Меню и панель инструментов
        self.create_menu_and_toolbar()

    def set_controller(self, controller):
        self.controller = controller
        # Подключение сигналов пагинации
        self.first_btn.clicked.connect(lambda: self.page_spin.setValue(1))
        self.prev_btn.clicked.connect(lambda: self.page_spin.setValue(self.page_spin.value() - 1))
        self.next_btn.clicked.connect(lambda: self.page_spin.setValue(self.page_spin.value() + 1))
        self.last_btn.clicked.connect(self.controller.go_to_last_page)
        self.page_spin.valueChanged.connect(self.controller.update_table)
        self.per_page_spin.valueChanged.connect(self.controller.update_table)
        # Подключение сигналов меню
        self.save_action.triggered.connect(self.controller.save_file)
        self.load_action.triggered.connect(self.controller.load_file)
        self.add_action.triggered.connect(self.controller.add_student)
        self.search_action.triggered.connect(self.controller.search_students)
        self.delete_action.triggered.connect(self.controller.delete_students)
        # Инициализация таблицы
        self.controller.update_table()

    def create_menu_and_toolbar(self):
        menubar = self.menuBar()
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        file_menu = menubar.addMenu('Файл')
        action_menu = menubar.addMenu('Действия')

        self.save_action = QAction('Сохранить', self)
        file_menu.addAction(self.save_action)
        toolbar.addAction(self.save_action)

        self.load_action = QAction('Загрузить', self)
        file_menu.addAction(self.load_action)
        toolbar.addAction(self.load_action)

        self.add_action = QAction('Добавить', self)
        action_menu.addAction(self.add_action)
        toolbar.addAction(self.add_action)

        self.search_action = QAction('Поиск', self)
        action_menu.addAction(self.search_action)
        toolbar.addAction(self.search_action)

        self.delete_action = QAction('Удалить', self)
        action_menu.addAction(self.delete_action)
        toolbar.addAction(self.delete_action)

    def update_table(self, students, page, per_page, total_pages, total_records):
        # Calculate start and end indices for the current page
        start = (page - 1) * per_page
        end = min(start + per_page, total_records)
        current_students = students[start:end]

        # Set row count to the actual number of students on this page
        self.table.setRowCount(len(current_students))
        for i, student in enumerate(current_students):
            self.table.setItem(i, 0, QTableWidgetItem(student.fio))
            self.table.setItem(i, 1, QTableWidgetItem(student.group))
            exams_str = '; '.join(f"{e['name']}: {e['score']}" for e in student.exams)
            self.table.setItem(i, 2, QTableWidgetItem(exams_str))

        # Update pagination controls
        self.page_spin.setMaximum(total_pages)
        self.total_label.setText(f'Всего записей: {total_records}, страниц: {total_pages}')

        # Update button states
        self.first_btn.setEnabled(page > 1)
        self.prev_btn.setEnabled(page > 1)
        self.next_btn.setEnabled(page < total_pages)
        self.last_btn.setEnabled(page < total_pages)