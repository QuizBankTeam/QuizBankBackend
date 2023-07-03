from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class OCRForm(FlaskForm):
    image = StringField(
        label='image',
        validators=[DataRequired()]
    )

class PostImgurPhotoForm(FlaskForm):
    image = StringField(
        label='image',
        validators=[DataRequired()]
    )