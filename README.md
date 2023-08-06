# QuizBankBackend
**Environment**<br>
Platform: Ubuntu 22.04 LTS<br>
Python version: 3.9.13<br>

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
pip install e . -U
```
For python virtual environment
```
python -m venv YOUR_VENV
source YOUR_VENV/bin/activate
pip install e . -U
```
**Run**
```
flask --app QuizBankBackend run --debug --host=0.0.0.0
```
or run `build.sh` in **linux**
```
./build.sh
```
## API Description
[API Document](https://hackmd.io/@5ljei2jDT1KwLOo0tzos2w/Sk4YwJqw3)
