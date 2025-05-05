import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from PyQt5.QtWidgets import QApplication
from student_management.model.student_model import StudentModel
from student_management.controller.student_controller import StudentController
from student_management.view.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = StudentModel()
    view = MainWindow()  # Создаём без аргументов
    controller = StudentController(model, view)
    view.set_controller(controller)  # Устанавливаем контроллер и подключаем сигналы
    view.show()
    sys.exit(app.exec_())