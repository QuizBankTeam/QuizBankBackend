FROM python:3.9.13
WORKDIR /QuizBankBackend
COPY . /QuizBankBackend
RUN pip install e . -U
EXPOSE 5000
CMD ["gunicorn", "-c", "gunicorn.py", "wsgi:app"]
# CMD ["flask", "--app", "QuizBankBackend", "run", "--host=0.0.0.0", "--debug"]
