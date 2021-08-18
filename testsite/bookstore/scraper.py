from pipe2db import pipe


class MockScraper:



    @pipe({
        'model': 'bookstore.BookInstance',
        'foreignkey_fields':{
            'book':{
                'model': 'bookstore.Book',
                'unique_key': 'isbn',
                'rename_fields': {
                    'descriptions': 'summary',
                },
                'foreignkey_fields': {
                    'author': {
                        'model': 'bookstore.Author',
                        'unique_key': 'email',
                    }
                },
                'manytomany_fields': {
                    'genre': {
                        'model': 'bookstore.Genre',
                        'unique_key': 'name',
                    }
                }
            }
        }
    })
    def parse(self, response=None):
        author1 = {
            'email': 'xman1@google.com',
            'first_name': 'charse',
            'last_name': 'javie',
            'date_of_birth': '1975-07-25',
            'date_of_death': '1995-07-11'
        }
        author2 = {
            'email': 'yman1@google.com',
            'first_name': 'jin',
            'last_name': 'gray',
            'date_of_birth': '1925-07-25',
            'date_of_death': '1999-01-21'
        }
        author3 = {
            'email': 'batman1@google.com',
            'first_name': 'wolverin',
            'last_name': 'jack',
            'date_of_birth': '1988-07-25',
            'date_of_death': None
        }

        genre1 = {
            'name': 'action'
        }
        genre2 = {
            'name': 'fantasy'
        }
        genre3 = {
            'name': 'science'
        }
        genre4 = {
            'name': 'journel'
        }

        book1 = {
            'title': 'oh happy day', 'author': author1, 'descriptions': 'very happy', 'isbn': '1234640841', 'genre': [genre1, genre2]
        }
        book2 = {
            'title': 'pathology', 'author': author3, 'descriptions': 'very sick', 'isbn': '7417130841', 'genre': [genre4]
        }
        book3 = {
            'title': 'java', 'author': author2, 'descriptions': 'web develop with java', 'isbn': '9875230846', 'genre': [genre1]
        }
        book4 = {
            'title': 'python', 'author': author2, 'descriptions': 'python data analysis', 'isbn': '2828233644', 'genre': [genre1, genre4, genre2]
        }
        book5 = {
            'title': 'quent', 'author': author3, 'descriptions': 'earn money be rich', 'isbn': '3571879874', 'genre': [genre3]
        }

        book_instance_list = [
            {
                'book': book3, 'imprint': 'iwqejadfaodfadf', 'due_back': '2021-08-17'
            },
            {
                'book': book3, 'imprint': 'afeadjaofjdalf', 'due_back': '2021-08-21'
            },
            {
                'book': book1, 'imprint': 'aefadfaiofjadfadf', 'due_back': '2022-09-17'
            },
            {
                'book': book5, 'imprint': '1af9eadfafeafda', 'due_back': '2021-06-01'
            },
            {
                'book': book2, 'imprint': 'afadfaefadfqqdfa', 'due_back': '2021-08-18'
            },
            {
                'book': book4, 'imprint': 'aefdfaefadfaadfaf', 'due_back': '2021-10-03'
            },
            {
                'book': book1, 'imprint': 'aefafaeqfqefadfadaf', 'due_back': '2021-07-27'
            },
        ]
        yield from book_instance_list
        