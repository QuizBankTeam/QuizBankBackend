from setuptools import setup, find_packages

requirements = [
    'Flask',
    'Flask-WTF',
    'pymongo',
    'WTForms',
    'WTForms-JSON',
    'flask-restful',
    'flask-jwt-extended',
    'email_validator',
    'google-cloud-vision',
    'itsdangerous',
    'Flask-Mail',
    'gunicorn',
    'google-cloud-storage',
    'facexlib>=0.2.5',
    'gfpgan>=1.3.5',
    'Pillow',
    'tqdm',
    'numpy',
    'basicsr>=1.4.2',
    'opencv-python-headless',
    'opencv-contrib-python-headless'
]

setup(
    name = 'QuizBankBackend',
    version = '0.1.0',
    description = 'QuizBank bankend system.',
    packages = find_packages(include=['QuizBankBackend', 'QuizBankBackend.*']),
    include_package_data=True,
    install_requires=requirements,
)
