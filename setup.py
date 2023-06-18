from setuptools import setup, find_packages

requirements = [
    'Flask',
    'Flask-WTF',
    'pymongo',
    'WTForms',
    'WTForms-JSON',
    'flask-restful'
]

setup(
    name = 'QuizBankBackend',
    version = '0.1.0',
    description = 'QuizBank bankend system.',
    packages = find_packages(include=['QuizBankBackend', 'QuizBankBackend.*']),
    include_package_data=True,
    install_requires=requirements,
)