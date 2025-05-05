from PyQt5.QtWidgets import QFileDialog
from student_management.view.add_dialog import AddStudentDialog
from student_management.view.search_dialog import SearchDialog
from student_management.view.delete_dialog import DeleteDialog

class StudentController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_student(self):
        dialog = AddStudentDialog(self.view)
        if dialog.exec_():
            student = dialog.get_student()
            self.model.add_student(student)
            self.update_table()

    def search_students(self):
        dialog = SearchDialog(self.model, self.view)
        dialog.exec_()

    def delete_students(self):
        dialog = DeleteDialog(self.model, self.view)
        if dialog.exec_():
            self.update_table()

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self.view, 'Сохранить файл', '', 'XML Files (*.xml)')
        if filename:
            self.model.save_to_xml(filename)

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.view, 'Загрузить файл', '', 'XML Files (*.xml)')
        if filename:
            self.model.load_from_xml(filename)
            self.update_table()

    def update_table(self):
        page = self.view.page_spin.value()
        per_page = self.view.per_page_spin.value()
        total_records = len(self.model.students)
        total_pages = max(1, (total_records + per_page - 1) // per_page)
        self.view.update_table(self.model.students, page, per_page, total_pages, total_records)

    def go_to_last_page(self):
        per_page = self.view.per_page_spin.value()
        total_records = len(self.model.students)
        total_pages = max(1, (total_records + per_page - 1) // per_page)
        self.view.page_spin.setValue(total_pages)