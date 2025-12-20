import unittest
from rk1 import books, chapters, books_chapters, get_one_to_many, get_many_to_many,task_b1, task_b2, task_b3

class TestBookAnalytics(unittest.TestCase):

    def setUp(self):
        self.one_to_many = get_one_to_many(books, chapters)
        self.many_to_many = get_many_to_many(books, chapters, books_chapters)

    def test_task_b1(self):
        result = task_b1(self.one_to_many)
        expected = [
            ('Введение в язык', 'Учебник по Python'),
            ('Введение в данные', 'Учебник по Python')
        ]
        self.assertEqual(result, expected)

    def test_task_b2(self):
        result = task_b2(books, self.one_to_many)
        expected = [
            ('Учебник по Python', 20),
            ('Роман Гарри Поттер', 45),
            ('Роман Мастер и Маргарита', 60)
        ]
        self.assertEqual(result, expected)

    def test_task_b3(self):
        result = task_b3(self.many_to_many)
        expected = [
            ('Введение в данные', 35, 'Учебник по Python'),
            ('Введение в язык', 20, 'Учебник по Python'),
            ('Введение в язык', 20, 'Учебник по С++'),
            ('Исчезнувшее стекло', 45, 'Роман Гарри Поттер'),
            ('Мальчик, который выжил', 50, 'Роман Гарри Поттер'),
            ('Никогда не разговаривайте с неизвестными', 60, 'Роман Мастер и Маргарита')
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()