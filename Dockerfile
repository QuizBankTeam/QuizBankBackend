# FROM ufoym/deepo:pytorch
FROM ufoym/deepo:pytorch-cpu
WORKDIR /QuizBankBackend
COPY . /QuizBankBackend
ENV HOME=/root
RUN pip install --upgrade pip
RUN pip install -e . -U
# RUN pip3 install 'pymongo[srv]'
EXPOSE 5000
CMD ["gunicorn", "-c", "gunicorn.py", "wsgi:app"]
# CMD ["flask", "--app", "QuizBankBackend", "run", "--host=0.0.0.0", "--debug"]
