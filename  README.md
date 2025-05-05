# Система управления студентами

## Описание

Программное обеспечение для учета успеваемости студентов с графическим интерфейсом на PyQt5.

## Установка зависимостей

```
pip install PyQt5
```
Структура проекта
## Python
```
-__init__.py
-main.py   
-example_1.xml
-example_2.xml
-requirements.txt
-student_management/
 ├── model/                  # Модель данных
 │   ├── student.py          # Класс Student
 │   ├── __init__.py 
 │   └── student_model.py    # Логика работы с данными
 ├── view/                   # Пользовательский интерфейс
 │   ├── __init__.py 
 │   ├── main_window.py      # Главное окно
 │   ├── add_dialog.py       # Диалог добавления
 │   ├── delete_dialog.py    # Диалог удаления
 │   └── search_dialog.py    # Диалог поиска
 │
 ├── controller/             # Контроллер
 │   ├── __init__.py 
 │   └── student_controller.py               # Точка входа
```

# Запуск системы
```
./python main.py
```
# Основные функции:

Добавление студента:

```
def add_student(self):
    dialog = AddStudentDialog(self)
    if dialog.exec_():
        student = dialog.get_student()
        self.model.add_student(student)
        self.update_table()
```
Поиск студентов:

```
def search_students(self):
    dialog = SearchDialog(self.model, self)
    dialog.exec_()
```
Удаление студентов:
```
def delete_students(self):
    dialog = DeleteDialog(self.model, self)
    if dialog.exec_():
        self.update_table()
```
Работа с файлами:
```
def save_file(self):
    filename, _ = QFileDialog.getSaveFileName(filter="XML (*.xml)")
    if filename:
        self.model.save_to_xml(filename)

def load_file(self):
    filename, _ = QFileDialog.getOpenFileName(filter="XML (*.xml)")
    if filename:
        self.model.load_from_xml(filename)
        self.update_table()
```

Формат данных XML
```
<!-- Пример файла данных -->
<students>
  <student fio="Иванов И.И." group="ИТ-101">
    <exam name="Математика" score="85"/>
    <exam name="Программирование" score="92"/>
  </student>
</students>
```


