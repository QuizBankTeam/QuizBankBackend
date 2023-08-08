# QuizBankBackend
**Environment**<br>
Platform: Ubuntu 22.04 LTS<br>
Python version: 3.10.6<br>

**Configuration**<br>
You need to add those settings in `QuizBankBackend/setting.json`
```json
{
    "MongodbUri": "YOUR_MONGODB_URI",
    "OCRCredentialPath": "YOUR_OCR_CREDENTIAL_PATH",
    "ImgurClientId": "YOUR_CLIENT_ID",
    "GmailAppPassword": "YOUR_GMAIL_APP_PASSWORD"
}
```

**Build**<br>
For conda virtual environment (recommanded)
```
conda create --name YOUR_VENV 
conda activate YOUR_VENV
pip install -e . -U
```
For python virtual environment
```
python -m venv quizbank
source quizbank/bin/activate
pip install -e . -U
```
**Run**
```
flask --app QuizBankBackend run --debug --host=0.0.0.0
```
or run `build.sh` in **linux**
```
./build.sh
```
or run in Docker container
```
docker run -p 5000:5000 --name quizbank -v ~/.config/gcloud:/root/.config/gcloud -e HOME=/root -d youwaiting/quizbank:NO_WSGI
```
## API Description
[API Document](https://hackmd.io/@5ljei2jDT1KwLOo0tzos2w/Sk4YwJqw3)
