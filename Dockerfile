FROM ufoym/deepo:pytorch
WORKDIR /QuizBankBackend
COPY . /QuizBankBackend
ENV HOME=/root
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1  -y
RUN pip install --upgrade pip
RUN pip install -e . -U
EXPOSE 5000
# CMD ["gunicorn", "-c", "gunicorn.py", "wsgi:app"]
CMD ["flask", "--app", "QuizBankBackend", "run", "--host=0.0.0.0", "--debug"]
