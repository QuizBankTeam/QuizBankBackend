from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Regexp


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

class HoughRotateForm(FlaskForm):
    image = FileField(
        'image',
        validators=[
            DataRequired(),
        ]
    )

class RealESRGANForm(FlaskForm):
    image = FileField(
        'image',
        validators=[
            DataRequired(),
        ]
    )

class LatexOCRForm(FlaskForm):
    image = FileField(
        'image',
        validators=[
            DataRequired(),
        ]
    )