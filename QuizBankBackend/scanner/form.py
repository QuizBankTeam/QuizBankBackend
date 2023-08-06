from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class OCRForm(FlaskForm):
    image = StringField(
        label='image',
        validators=[DataRequired()]
    )

class DocumentOCRForm(FlaskForm):
    document = StringField(
        label='document',
        validators=[DataRequired()]
    )

class PostImgurPhotoForm(OCRForm):
    pass

class HoughRotateForm(OCRForm):
    pass