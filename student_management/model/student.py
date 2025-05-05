class Student:
    def __init__(self, fio, group, exams):
        self.fio = fio
        self.group = group
        self.exams = exams  # Список словарей {name: str, score: int}

    def average_score(self):
        if not self.exams:
            return 0
        return sum(exam['score'] for exam in self.exams) / len(self.exams)