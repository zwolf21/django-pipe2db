
# django-pipe2db

- [django-pipe2db](#django-pipe2db)
    - [소개](#소개)
    - [사용 목적](#사용-목적)
    - [설치](#설치)
    - [임포트](#임포트)
  - [1. 기본 개념](#1-기본-개념)
    - [1. 데코레이터 - pipe](#1-데코레이터---pipe)
    - [2. 생성자 함수](#2-생성자-함수)
    - [3. 컨텍스트](#3-컨텍스트)
  - [2. 튜토리얼](#2-튜토리얼)
    - [1. 기본 예시](#1-기본-예시)
    - [2. 관계형 테이블](#2-관계형-테이블)
      - [1. 왜래키 관계에 있는 데이터의 pipe](#1-왜래키-관계에-있는-데이터의-pipe)
      - [2. 다대다 관계에 있는 데이터의 pipe](#2-다대다-관계에-있는-데이터의-pipe)
      - [3. 중첩된 관계](#3-중첩된-관계)
  - [3. 컨텐트파일](#3-컨텐트파일)


### 소개

- 파이썬 함수에서 리턴한 데이터를 장고 모델로 저장해주는 하나의 유용한 데코레이터 입니다
- 파이썬 3.8, django 3.2 환경에서 제작 되었습니다.

### 사용 목적

- 웹스크래핑등에서 얻은 데이터를 관계형 데이터베이스인 장고 모델과 연결하는것은 다소 복잡한 코드를 작성해야 할 것입니다.
- 예를들어 북스토어 싸이트에서 데이터를 가져올 경우 특정 페이지 안에 저자, 책, 서평, 장르구분 등 1:N, M:N 등의 관계가 있는 정보들이 혼재 되어 있습니다.
- 그러한 관계성 있는 데이터를 작은 데코레이터 함수로 장고 모델과 연결시켜 줍니다
- 장고코드와 데이터를 가져오는 코드가 섞이지 않고 서로 독립성을 유지 할 수 있게 해줍니다.

### 설치

```code
pip install django-pipe2db
```
### 임포트
```python
from pipe2db import pipe
```



## 1. 기본 개념
- 다음 3가지 사항을 고려해야 합니다

### 1. 데코레이터 - pipe

- 데이터를 생산한 함수를 장식하여 데이터를 장고 모델에 저장해줍니다
- 생산한 데이터와 장고 모델과의 관계를 담은 컨텍스트 정보를 인수로 받습니다.
  ```python
    @pipe{
        'model': 'bookstore.Book',
        'unique_key': 'isbn',
        'foreignkey_fields': {
            'author': {
                'model': 'bookstore.Author',
                'unique_key': 'email',
            }
        }
    }
    def process_item(self, item):
        return item
  ```

### 2. 생성자 함수
- 단일개체: 딕셔너리 형태로 return 하거나 yield 합니다
- 복수개체: 딕셔너리를 리스트에 담아서 return 합니다. 리스트 전체를 yield해서는 안됩니다.
- 딕셔너리의 키 이름과 모델의 필드 이름이 서로 매칭되어야합니다
- 스크래피의 파이프라인을 각 아이템별로 라우팅하여 분리된 process_item에 사용할 수 있습니다.
  - foreignkey, manytomany fields와 같은 관계형 필드는 내포된 딕셔너리, 리스트 형태로 값을 지정합니다.
  - 리턴되는 딕셔너리의 키이름과 모델의 필드 이름이 다를 경우 context의 rename_fields 속성을 통해 해결 할수 있습니다.
  - 딕셔너리에 모델의 필드내역에 없는 키가 있을 경우 context의 exclude_fields 속성을 통해 해결 할수 있습니다.
  
    ```python
        def process_item(self, item):
            book_list = [
                {
                    'author': {'name': 'moon'}, 'title': 'pipe2db', 'description': 'awesome'
                }
            ]
            return book_list        
    ```
    또는 다음과 같이 상위 외래키에 해당하는 데이터는 변수에 담아 리턴하는것이 훨씬 간결해 보입니다.
    ```python
        def process_item(self, item):
            author1 = {
                'name': 'moon'
            }
            book_list = [
                {
                    'author': author1, 'title': 'pipe2db', 'description': 'awesome'
                }
            ]
            return book_list        
    ```
      - author와 book은 1:N 관계에 있습니다.
      - 위와같이 book의 딕셔너리에 author 딕셔너리를 내포하여 리턴하여 줍니다.


### 3. 컨텍스트
- 자바스크립트 스타일의 json형태를 띄고 있습니다.
- 함수가 생산한 데이터와 장고 모델과의 관계를 담고 있는 중첩 된 사전입니다.
- 모델간의 관계에 따라 재귀적으로 여러겹으로 중첩될 수 있습니다
- 컨텍스트 사전에는 다음과 같은 키(기능) 들을 적용 할수 있습니다
- 앞서 리턴한 관계를 foreignkey_fields속성을 사용하여 재귀적으로 구성 합니다.
    ```python
    {
        'model': 'bookstore.Book',
        'unique_key': 'isbn',
    #or 'unique_key': ['isbn','title'], passing list, if it is unique_together!
        'foreignkey_fields': {
            'author': {
                'model': 'bookstore.Author',
                'unique_key': 'email',
            }
        }
    }
    ```
    - model: 현재 생성하는 데이터가 연결 될 장고 모델, 모델을 직접 임포트 하지 않아도 되며 모델의 문자열 경로를 지정합니다.
    - unique_key: 탐색에 필요한 모델이 갖고 있는 유일키, 지정하지 않으면 데이터의 중복등 문제 발생할수 있으므로 가급적 지정하는게 좋습니다.
      - 유일성을 지정하기 위해서 복수의 값을 리스트 형태로 지정할 수도 있습니다. 예(['isbn', 'title'])
    - foreignkey_fields: 모델이 갖고 있는 외래키, 내포된 컨텍스트를 재귀적으로 지정합니다.
    - manytomany_fields: foreignkey_fields키와 마찬가지로 연결된 모델의 컨텍스트를 내포하여 지정합니다.
    - contentfile_fields: 이미지, 파일등의 binary data 가 포함된 필드를 표현합니다
      - source_url_fields: 장고의 meida 폴더에 저장하기 위해선 파일의 출처가 있는 경로도 리턴한 딕셔너리키에 포함되어 있어야합니다.
       ```python
       '''
        image = {
            'image': b'x390j092d'....,
            'src': 'http://pstatic-net/abc/' # 파일의 출처가 있는 경로도 데이터에 포함시켜야합니다.
        }
        '''
        yield image       
       ```
    - rename_fields: 어떠한 이유에 의해서 리턴한 데이터의 키이름 모델의 필드이름이 다를경우 데이터키: 모델필드 형식으로 매칭시켜 줍니다
    - exclude_fields: 리턴한 데이터가 모델의 필드명에 존재하지 않는 키를 갖는 경우 지정해 주어서 배제 할수 있습니다




## 2. 튜토리얼
* 아래의 예제코드의 모델들은 [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) 을 참조 하였습니다.
### 1. 기본 예시
- 다음과 같은 책의 저자 정보에 대한 모델이 있습니다
    ```python
    class Author(models.Model):
        email = models.EmailField('Email', unique=True)
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        date_of_birth = models.DateField(null=True, blank=True)
        date_of_death = models.DateField('Died', null=True, blank=True)
    ```
- 다음과 같은 데이터를 생성하는 함수가 있습니다.
- 간단한 키와 값으로 이루어진 여러개의 사전을 리스트에 담아서 리턴하는 구조입니다.
- 모델의 각 필드 이름이 반환값의 딕셔너리의 키에 매칭이 되어있습니다.
    ```python
    def process_author_item(item):
        author_items = [    
            {
                'email': 'xman1@google.com',
                'first_name': 'charse',
                'last_name': 'javie',
                'date_of_birth': '1975-07-25',
                'date_of_death': '1995-07-11'
            },{
                'email': 'yman1@google.com',
                'first_name': 'jin',
                'last_name': 'gray',
                'date_of_birth': '1925-07-25',
                'date_of_death': '1999-01-21'
            },{
                'email': 'batman1@google.com',
                'first_name': 'wolverin',
                'last_name': 'jack',
                'date_of_birth': '1988-07-25',
                'date_of_death': None
            }
        ]
        return author_items
    ```

- 이제 모델과 함수를 연결하겠습니다.
    ```python
    @pipe({
        'model': 'bookstore.Author', # model: 
        'unique_key': 'email' # unique_key: 
    })
    def process_author_item(item):
        author_items = [...]
        return author_items
    ```
    - pipe 데코레이터로 process_author_item 함수를 장식하여 줍니다.
    - context의 정보로는 연결될 모델에 대한 정보를 지정 합니다
    - 함수가 실행되고 결과를 리턴하는 시점에 장고 모델로 데이터들을 create 합니다


### 2. 관계형 테이블
#### 1. 왜래키 관계에 있는 데이터의 pipe

- 다음과 같이 Author와 1:N의 관계를 맺고 있는 Book 모델이 있습니다.
  
  ```python
  class Book(models.Model):
        """Model representing a book (but not a specific copy of a book)."""
        title = models.CharField(max_length=200)
        author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True) ## FK!!
        summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book') 
        isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character ISBN number</a>')
  ```
- 다음과 같이 Book 데이터 사전의 author 키에 Author 데이터 사전을 내포하여 같이 리턴하는 함수에 데코레이터를 적용하겠습니다.
- *foreignkey_fields*를 이용하여 author데이터가 book 데이터 안에 내포되어 있는 형태를 계층적으로 표현합니다.
- *foreignkey_fields*의 값은 재귀적으로 author의 컨텍스트가 됩니다
- 즉 book cotext가 author 컨텍스트를 품고 있는 모양이 됩니다.

    ```python
    @pipe({
        'model': 'bookstore.Book',
        'unique_key': 'isbn',
        'foreignkey_fields': {
            'author': { # author에 대한 정보를 재귀적으로 다시 표현 합니다.
                'model': 'bookstore.Author', 
                'unique_key': 'email'
            }
        },
        'rename_fields': {
            'descriptions': 'summary' 
        },
        'exclude_fields': ['_referer']
    })
    def process_book_item(item):
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

        book_list = [
            {
                'title': 'oh happy day', 'author': author1, 'descriptions': 'very happy', 'isbn': '1234640841',
                '_referer': 'http://abc1.com' # 모델에 없는 메타정보,
            },
            {
                'title': 'pathology', 'author': author3, 'descriptions': 'very sick', 'isbn': '7417130841',
                '_referer': 'http://abc2.com'
            },
            {
                'title': 'java', 'author': author2, 'descriptions': 'web develop with java', 'isbn': '9875230846',
                '_referer': 'http://abc3.com'
            },
            {
                'title': 'python', 'author': author2, 'descriptions': 'python data analysis', 'isbn': '2828233644',
                '_referer': 'http://abc3.com'
            },
            {
                'title': 'quent', 'author': author3, 'descriptions': 'earn money be rich', 'isbn': '3571879874',
                '_referer': 'http://abc4.com'
            }
        ]
        return book_list
    ```
  - *rename_fields*를 이용하여 데이터의 descriptions 키를 Book모델의 summary로 매칭하여 줍니다.
    - 모델과 데이터의 필드명과 키값이 안 맞는 경우
    - 장고 모델쪽에서 필드명을 바꾸거나 데이터쪽에서 사전의 키값을 바꾸어야 하지만
    - 필드와 키값을 어느 한쪽으로 맞추는 것은 상당히 진행된 프로젝트라면 변경하는 쪽에서 로직이 꼬일 우려가 있습니다
    - 이러한 위험이 존재 한다면 rename_fields 사용합니다.
  - *exclude_fields를* 이용하여 Book모델에 없는 키를 제외하여 줍니다.
    - 데이터 수집을 하다보면 데이터 수집 로직에 필요한 메타 정보를 사전에 정보를 주입해 놓는 것이 필요한 경우가 많습니다
    - 이러한 메타 정보는 데이터를 받는 장고 모델 입장에서는 필요 하지 않고 exclude_fields에 명시적으로 지정하여 주지 않으면 insert할때 오류가 발생합니다.
  - **rename_fields와 exclude_fields를 잘 이용하면 데이터를 수집하는 로직과 장고 로직이 서로 영향 받지 않을 수 있고 독립성 유지에 효과적입니다**
 
- 만약 Author와 Book 데이터를 위와같이 동시에 얻은 상황이 아니라 Author 데이터가 기존에 있고
- Book 데이터는 기존에 존재하는 Author데이터와 외래키 관계만 맺어 주는 상황이라면 
- author키의 값으로 Author 데이터 전체를 딕셔너리로 지정할 필요 없이 Author의 유일키 값만 지정해줘도 됩니다. (문자열이나 숫자여야 함)
- 또한 데코레이터의 method에 get이라고 지정해 줄 수있습니다.
- method는 지정해 주지 않으면 기본값 create로 작동하며, 리턴한 사전의 foreignkey 에 해당하는 키의 값으로 내포된 딕셔너리가 아닌 문자열이나 숫자를 지정하면 get으로 작동하긴 합니다.
  
    ```python
    @pipe({
        'model': 'bookstore.Book',
        'unique_key': 'isbn',
        'foreignkey_fields': {
            'author': { 
                'method': 'get', # Book의 외래키인 Author가 DB에 존재한다면 만들필요 없이 찾기만 하면되죠!
                'model': 'bookstore.Author', 
                'unique_key': 'email'
            }
        },
        'rename_fields': {
            'descriptions': 'summary' 
        },
        'exclude_fields': ['_referer']
    })
    def process_book_item(item):
            book_list = [
            {                                   # Author 데이터 전체가 아닌 Author의 유일키값만 전달해 주었습니다.
                                                # 해당 키값을 가진 Author데이터는 반드시 존해 해야 하며
                                                # 이렇게 단일 문자열을 전달할 경우 method는 get으로 자동으로 작동하게 됩니다.
                'title': 'oh happy day', 'author': 'xman1@google.com', 'descriptions': 'very happy', 'isbn': '1234640841',
                '_referer': 'http://abc1.com' 
            },
            {
                'title': 'pathology', 'author': 'batman1@google.com', 'descriptions': 'very sick', 'isbn': '7417130841',
                '_referer': 'http://abc2.com'
            },
            {
                'title': 'java', 'author': 'yman1@google.com', 'descriptions': 'web develop with java', 'isbn': '9875230846',
                '_referer': 'http://abc3.com'
            },
            {
                'title': 'python', 'author': 'yman1@google.com', 'descriptions': 'python data analysis', 'isbn': '2828233644',
                '_referer': 'http://abc3.com'
            },
            {
                'title': 'quent', 'author': 'batman1@google.com', 'descriptions': 'earn money be rich', 'isbn': '3571879874',
                '_referer': 'http://abc4.com'
            }
        ]
        return book_list
    ```
----
#### 2. 다대다 관계에 있는 데이터의 pipe
  - 아래와 같이 Book 모델과 다대다 관계를 갖고 있는 Genre 모델이 있습니다
    ```python
    # Create your models here.
    class Genre(models.Model):
        name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

        def __str__(self):
            return self.name

    class Book(models.Model):
        """Model representing a book (but not a specific copy of a book)."""
        title = models.CharField(max_length=200)
        author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
        summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
        isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character')

        genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    ```
  - 이럴 경우엔 함수의 리턴 데이터 사전의 genre 키값으로 Genre의 데이터를 리스트 형태로 지정해 줍니다.
    ```python
    genre1 = {'name': 'action'}
    genre2 = {'name': 'fantasy'}
    genre3 = {'name': 'science'}
    genre4 = {'name': 'journel'}

    book_list = [
        {
            'title': 'oh happy day', 'author': 'xman1@google.com', 'descriptions': 'very happy', 'isbn': '1234640841',
            'genre': [genre1, genre3] # 다대다 형식의 필드는 리스트 형태로 지정
        },
        {
            'title': 'pathology', 'author': 'batman1@google.com', 'descriptions': 'very sick', 'isbn': '7417130841',
            'genre': [genre4]
        },
        {
            'title': 'java', 'author': 'yman1@google.com', 'descriptions': 'web develop with java', 'isbn': '9875230846',
            'genre': [genre1]
        },
        {
            'title': 'python', 'author': 'yman1@google.com', 'descriptions': 'python data analysis', 'isbn': '2828233644',
            'genre': [genre1, genre4, genre2]
        },
        {
            'title': 'quent', 'author': 'batman1@google.com', 'descriptions': 'earn money be rich', 'isbn': '3571879874',
            'genre': [genre3]
        },
    ]
    
    def process_book_item(item=book_list):
        return book_list

    ```
- 데코레이터 컨텍스트에 manytomany_fields를 추가 합니다
    ```python
    @pipe({
        'model': 'bookstore.Book',
        'unique_key': 'isbn',
        'foreignkey_fields': {
            'author': { 
                'method': 'get',
                'model': 'bookstore.Author', 
                'unique_key': 'email'
            }
        },
        'rename_fields': {
            'descriptions': 'summary' 
        },
        'exclude_fields': ['_referer'],

        'manytomany_fields':{ # 다대다 관계
            'model': 'bookstore.Genre',
            'unique_key': 'name'
        }

    })
    def process_book_item(item=book_list):
          return book_list
    ```
- foreignkey_fields 와 마찬가지로 다대다 키가 DB에 이미 존재하는 상황이라면 다대다 모델의 유일키 값만 지정해줘도 됩니다
    ```python
        ...
       book_list = [
            {
                'title': 'oh happy day', 'author': 'xman1@google.com', 'descriptions': 'very happy', 'isbn': '1234640841',
                'genre': ['action', 'sceince'] # 해당 Genre 객체가 DB에 이미존재 하는게 확실 할 경우  유일키 값으로 지정
            },
        ...
    ```
----
#### 3. 중첩된 관계
  - 다중으로 외래키가 중첩된 형태의 데이터의 경우 컨텍스트도 그에 맞게 지정하면 됩니다
  - 아래와 같이 Book의 대여 기록을 갱신하는 모델인 BookInstance 모델이 있습니다. 
    ```python
    class BookInstance(models.Model):
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
      book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
      imprint = models.CharField(max_length=200)
      due_back = models.DateField(null=True, blank=True)

      LOAN_STATUS = (
          ('m', 'Maintenance'),
          ('o', 'On loan'),
          ('a', 'Available'),
          ('r', 'Reserved'),
      )
      status = models.CharField(
          max_length=1,
          choices=LOAN_STATUS,
          blank=True,
          default='m',
          help_text='Book availability',
      )
      class Meta:
          ordering = ['due_back']

    ```
    - BookInstance 모델은 Book을 외래키로 하므로 외래키 관계는 BookInstance-> Book-> Author 이렇듯 2중으로 중첩되게 됩니다.
  
  - 아래와 같이 BookInstance, Book, Author, Genre등 여러 계층의 중첩된 데이터를 리턴하는경우
  - 가장 하위에 계층에 있는 데이터를 시작으로 컨텍스트를 작성합니다
  - 데이터가 내포되어 있는 구조 그대로 작성합니다.
    ```python
    @pipe({
        'model': 'bookstore.BookInstance', # unique_key가 지정되지 않는 모델이므로 중복된 create가 발생 합니다.
        'foreignkey_fields':{ #1
            'book':{
                'model': 'bookstore.Book',
                'unique_key': ['isbn', 'title'],
                'rename_fields': {
                    'descriptions': 'summary',
                },
                'foreignkey_fields': { #2
                    'author': {
                        'model': 'bookstore.Author',
                        'unique_key': 'email',
                    }
                },
                'manytomany_fields': {
                    'genre': {
                        'method': 'get',
                        'model': 'bookstore.Genre',
                        'unique_key': 'name',
                        'method': 'get'
                    }
                }
            }
        }
    })
    def process_book_instance(self, item):
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

        genre1 = {'name': 'action'}
        genre2 = {'name': 'fantasy'}
        genre3 = {'name': 'science'}
        genre4 = {'name': 'journel'}

        book1 = {
            'title': 'oh happy day', 'author': author1, 'descriptions': 'very happy', 'isbn': '1234640841', 'genre': ['action', 'science']
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
                'book': book2, 'imprint': 'iwqejadfaodfadf', 'due_back': '2021-08-17'
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
    ```
    - 실제로는 위와 같이 여러관계에 있는 데이터를 한번에 리턴하는 경우는 드물 것입니다.
    - 보통 Author, Book, Genre를 순차적으로 pipe하여 DB에 저장한 후 마지막에 BoonInstance 를 구해서 Book과 연결 시키는것이 일반적일 것입니다.
    - 위 예제는 pipe가 왜래키 관계에 대해서 재귀적으로 작동 할수 있음을 보여 줍니다.
----

## 3. 컨텐트파일
- 현재 이 라이브러리는 이미지나 파일같은 바이너리 데이터의 처리는 다양하게 지원하지는 않습니다
- 아래와 같이 간단한 이미지 저장용 모델과 그 데이터를 생성하는 함수가 있습니다.
    ```python
    class Image(models.Model):
        img = models.ImageField()
        my_src = modles.UrlField('image url')
    ```
    ```python

    @pipe({
        'model': 'bookstore.Image',
        'unique_key': 'src',
        'contentfile_fields': {
            'img': {
                'source_url_fields': 'src' # 파일로 저정하려면 파일의 원본 출처를 꼭 지정하여 주어야 합니다.
            }
        }
    })
    def parse_image(self, response):

        yield {
            'img': response.content, # 바이너리를 사전에 담아서 리턴
            'src': response.url # 파일명을 추출하기위해 파일의 출처를 꼭 포함 시켜 주어야 한다.
        }
    ```
    - 위와 같이 contentfile_fields 속성을 img 키에에 지정해 주었습니다.
    - source_url_fields 속성을 내포하여 지정해 주었는데요, 이 필드를 토대로 이미지의 파일명을 정하기 때문에 반드시 데이터에 포함시켜야 하는 일종의 메타 데이터입니다.
    - 아래와 같이 source_url_fields이 모델에서는 필요가 없다면 exclude_fields에 지정하여 주면 됩니다.
        ```python
        class Image(models.Model):
            img = models.ImageField()
        
        .....
        .....

        @pipe({
            'model': 'bookstore.Image',
            'unique_key': 'src',
            'contentfile_fields': {
                'img': {
                    'source_url_fields': 'my_src' # 파일로 저정하려면 파일의 원본 출처를 꼭 지정하여 주어야 합니다.
                }
            },
            'rename_fields': {
                'src': 'my_src'
            }
           # 'exclude_fields': ['my_src'] # src 키가 실제 모델에 없는 필드일 때는 exclude 시켜 주어야 합니다.
        })
        def parse_image(self, response):

            yield {
                'img': response.content, 
                'my_src': response.url # 파일명을 추출하기위해 파일의 출처를 리턴 데이터에 꼭 포함 시켜 주어야 한다.
            }
        ```

 







