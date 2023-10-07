from setuptools import setup, find_packages

requirements = [
    'Flask',
    'Flask-WTF',
    'pymongo[srv]',
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
    'Pillow',
    'tqdm',
    'numpy',
    'basicsr>=1.4.2',
    'opencv-python-headless',
    'opencv-contrib-python-headless',
    'Flask-Limiter[mongodb]',
    'shortuuid',
    'flask-socketio',
    'eventlet',
    'pix2tex'
]

setup(
    name = 'QuizBankBackend',
    version = '0.1.0',
    description = 'QuizBank bankend system.',
    packages = find_packages(include=['QuizBankBackend', 'QuizBankBackend.*']),
    include_package_data=True,
    install_requires=requirements,
)
