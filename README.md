# QuizBankBackend
**Environment**<br>
Platform: Ubuntu 22.04 LTS<br>
Python version: 3.10.12<br>

**Configuration**<br>
You need to add those settings in `QuizBankBackend/setting.json`
```json
{
    "MongodbUri": "YOUR_MONGODB_URI",
    "OCRCredentialPath": "YOUR_OCR_CREDENTIAL_PATH",
    "ImgurClientId": "YOUR_CLIENT_ID",
    "GmailAppPassword": "YOUR_GMAIL_APP_PASSWORD",
    "GCPProjectId": "YOUR_GCP_PROJECT_ID",
    "SecretKey": "YOUR_SECRET_KEY"
}
```

**Build**<br>
For conda virtual environment (recommanded)
```
conda create --name quizbank
conda activate quizbank
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -e . -U
```
For python virtual environment
```
python -m venv quizbank
source quizbank/bin/activate
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -e . -U
```
**Run**<br>
```
python3 main.py
```
or run in Docker container
```
docker run -p 5000:5000 --name quizbank -v ~/.config/gcloud:/root/.config/gcloud -d youwaiting/quizbank:no_wsgi
```
## API Description
[API Document](https://hackmd.io/@5ljei2jDT1KwLOo0tzos2w/Sk4YwJqw3)

## Reference
[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)<br>
[Latex OCR](https://github.com/lukas-blecher/LaTeX-OCR)<br>
[Hough Rotate](https://bit.kuas.edu.tw/~jni/2021/vol6/s2/07-v6n2-0115_r02.pdf)
