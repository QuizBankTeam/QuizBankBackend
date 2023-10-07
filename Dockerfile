FROM youwaiting/pytorch:cpu
WORKDIR /QuizBankBackend
COPY . /QuizBankBackend
ENV HOME=/root
RUN pip install --upgrade pip
RUN pip install -e . -U
EXPOSE 5000
# CMD ["gunicorn", "-c", "gunicorn.py", "main:app"]
CMD ["python3", "main.py"]
