from pathlib import Path
from setuptools import setup, find_packages



setup(
	name='django-pipe2db',
	version='1.0.2',
	license='MIT',
	description='A decorator that connects django model and data generator function',
	long_description=Path('README.md').read_text(encoding='utf-8'),
	long_description_content_type="text/markdown",
	author = 'HS Moon',
	author_email = 'pbr112@naver.com',
	keywords=['pipe2db', 'django-pipe2db', 'django orm', 'standalone django', 'standalone django orm'],
	url='https://github.com/zwolf21/django-pipe2db',
	packages=find_packages(exclude=['test', 'testsite', 'useage', 'docs', 'useage']),
	install_requires=['django'],
	classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Email',
    ],
	python_requires=">=3.8"
)