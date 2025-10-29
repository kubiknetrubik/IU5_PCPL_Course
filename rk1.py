#24 B
from operator import itemgetter
class Book:
    def __init__(self, id, title):
        self.id = id
        self.title = title

class Chapter:
    def __init__(self, id, name, pages, book_id):
        self.id = id
        self.name = name
        self.pages = pages
        self.book_id = book_id

class BookChapter:
    def __init__(self, book_id, chapter_id):
        self.book_id = book_id
        self.chapter_id = chapter_id

books = [
    Book(1, 'Роман Гарри Поттер'),
    Book(2, 'Роман Мастер и Маргарита'),
    Book(3, 'Учебник по Python'),
    Book(11, 'Учебник по С++'),
    Book(22, 'Роман Гордость и предубеждение'),
]

chapters = [
    Chapter(1, 'Мальчик, который выжил', 50, 1),
    Chapter(2, 'Исчезнувшее стекло', 45, 1),
    Chapter(3, 'Никогда не разговаривайте с неизвестными', 60, 2),
    Chapter(4, 'Введение в язык', 20, 3),
    Chapter(5, 'Введение в данные', 35, 3),
]

books_chapters = [
    BookChapter(1, 1),
    BookChapter(1, 2),
    BookChapter(2, 3),
    BookChapter(3, 4),
    BookChapter(3, 5),
    BookChapter(11, 4) 
]

def main():
    one_to_many = [(c.name, c.pages, b.title)
                   for b in books
                   for c in chapters
                   if c.book_id == b.id]

    many_to_many_temp = [(b.title, bc.book_id, bc.chapter_id)
                         for b in books
                         for bc in books_chapters
                         if b.id == bc.book_id]
    
    many_to_many = [(c.name, c.pages, book_title)
                    for book_title, book_id, chapter_id in many_to_many_temp
                    for c in chapters if c.id == chapter_id]

    #Список глав на 'В' и названия их книг
    print('Задание B1')
    res_b1 = [(c_name, b_title) 
              for c_name, _, b_title in one_to_many 
              if c_name.startswith('В')]
    print(res_b1)

    #Список книг с минимальным количеством страниц.
    print('\nЗадание B2')
    res_b2_unsorted = []
    for b in books:
        b_chapters = list(filter(lambda i: i[2] == b.title, one_to_many))
        if len(b_chapters) > 0:
            b_pages_list = [pages for _, pages, _ in b_chapters]
            b_pages_min = min(b_pages_list)
            res_b2_unsorted.append((b.title, b_pages_min))
    
    res_b2 = sorted(res_b2_unsorted, key=itemgetter(1))
    print(res_b2)

    # Список глав и книг (многие-ко-многим), отсортированный по названию главы.
    print('\nЗадание B3')
    res_b3 = sorted(many_to_many, key=itemgetter(0))
    print(res_b3)

if __name__ == '__main__':
    main()