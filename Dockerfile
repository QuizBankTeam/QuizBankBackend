FROM python:3.9.13
WORKDIR /QuizBankBackend
COPY . /QuizBankBackend
RUN pip install e . -U
EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "--workers=4", "--threads=4", "-preload", "wsgi:app"]
