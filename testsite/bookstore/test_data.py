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
genre5 = {
    'name': 'romance'
}


book1_with_nested_author_nested_genre = {
    'title': 'oh happy day', 'author': author1, 'descriptions': 'very happy', 'isbn': '1234640841', 'genre': [genre5]
}
book2_with_nested_author_nested_genre = {
    'title': 'pathology', 'author': author3, 'descriptions': 'very sick', 'isbn': '7417130841', 'genre': [genre4]
}
book3_with_nested_author_nested_genre = {
    'title': 'java', 'author': author2, 'descriptions': 'web develop with java', 'isbn': '9875230846', 'genre': [genre1]
}
book4_with_nested_author_nested_genre = {
    'title': 'python', 'author': author2, 'descriptions': 'python data analysis', 'isbn': '2828233644', 'genre': [genre1, genre4, genre2]
}
book5_with_nested_author_nested_genre = {
    'title': 'quent', 'author': author3, 'descriptions': 'earn money be rich', 'isbn': '3571879874', 'genre': [genre3]
}

book1_with_key_author_nested_genre = {
    'title': 'oh happy day', 'author': 'xman1@google.com', 'descriptions': 'very happy', 'isbn': '1234640841', 'genre': [genre5]
}
book2_with_key_author_nested_genre = {
    'title': 'pathology', 'author': 'batman1@google.com', 'descriptions': 'very sick', 'isbn': '7417130841', 'genre': [genre4]
}
book3_with_key_author_nested_genre = {
    'title': 'java', 'author': 'yman1@google.com', 'descriptions': 'web develop with java', 'isbn': '9875230846', 'genre': [genre1]
}
book4_with_key_author_nested_genre = {
    'title': 'python', 'author': 'yman1@google.com', 'descriptions': 'python data analysis', 'isbn': '2828233644', 'genre': [genre1, genre4, genre2]
}
book5_with_key_author_nested_genre = {
    'title': 'quent', 'author': 'batman1@google.com', 'descriptions': 'earn money be rich', 'isbn': '3571879874', 'genre': [genre3]
}

book1_with_key_author_key_genre = {
    'title': 'oh happy day', 'author': 'xman1@google.com', 'descriptions': 'very happy', 'isbn': '1234640841', 'genre': ['romance']
}
book2_with_key_author_key_genre = {
    'title': 'pathology', 'author': 'batman1@google.com', 'descriptions': 'very sick', 'isbn': '7417130841', 'genre': ['journel']
}
book3_with_key_author_key_genre = {
    'title': 'java', 'author': 'yman1@google.com', 'descriptions': 'web develop with java', 'isbn': '9875230846', 'genre': ['action']
}
book4_with_key_author_key_genre = {
    'title': 'python', 'author': 'yman1@google.com', 'descriptions': 'python data analysis', 'isbn': '2828233644', 'genre': ['action', 'journel', 'fantasy']
}
book5_with_key_author_key_genre = {
    'title': 'quent', 'author': 'batman1@google.com', 'descriptions': 'earn money be rich', 'isbn': '3571879874', 'genre': ['science']
}

book1_with_nested_author_key_genre = {
    'title': 'oh happy day', 'author': author1, 'descriptions': 'very happy', 'isbn': '1234640841', 'genre': ['romance']
}
book2_with_nested_author_key_genre = {
    'title': 'pathology', 'author': author3, 'descriptions': 'very sick', 'isbn': '7417130841', 'genre': ['journel']
}
book3_with_nested_author_key_genre = {
    'title': 'java', 'author': author2, 'descriptions': 'web develop with java', 'isbn': '9875230846', 'genre': ['action']
}
book4_with_nested_author_key_genre = {
    'title': 'python', 'author': author2, 'descriptions': 'python data analysis', 'isbn': '2828233644', 'genre': ['action', 'journel', 'fantasy']
}
book5_with_nested_author_key_genre = {
    'title': 'quent', 'author': author3, 'descriptions': 'earn money be rich', 'isbn': '3571879874', 'genre': ['science']
}



bookinstance1_nested_all = {
    'book': book2_with_nested_author_nested_genre, 'imprint': 'iwqejadfaodfadf', 'due_back': '2021-08-17'
}
bookinstance2_nested_all = {
    'book': book3_with_nested_author_nested_genre, 'imprint': 'afeadjaofjdalf', 'due_back': '2021-08-21'
}
bookinstance3_nested_all = {
    'book': book1_with_nested_author_nested_genre, 'imprint': 'aefadfaiofjadfadf', 'due_back': '2022-09-17'
}
bookinstance4_nested_all = {
    'book': book5_with_nested_author_nested_genre, 'imprint': '1af9eadfafeafda', 'due_back': '2021-06-01'
}
bookinstance5_nested_all = {
    'book': book4_with_nested_author_nested_genre, 'imprint': 'aefdfaefadfaadfaf', 'due_back': '2021-10-03'
}

bookinstance6_book2_with_key_author_nested_genre = {
    'book': book2_with_key_author_nested_genre, 'imprint': 'afadfaefadfqqdfa', 'due_back': '2021-08-18'
}
bookinstance7_book1_with_nested_author_key_genre = {
    'book': book1_with_nested_author_key_genre, 'imprint': 'aefafaeqfqefadfadaf', 'due_back': '2021-07-27'
}


