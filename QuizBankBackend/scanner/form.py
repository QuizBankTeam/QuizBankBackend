from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class OCRForm(FlaskForm):
    image = StringField(
        label='image',
        validators=[DataRequired()]
    )

class GetImgurPhotoForm(FlaskForm):
    class Meta:
        csrf = False

    imageId = StringField(
        label='imageId',
        validators=[DataRequired()]
    )

class PostImgurPhotoForm(FlaskForm):
    image = StringField(
        label='image',
        validators=[DataRequired()]
    )

class DeleteImgurPhotoForm(FlaskForm):
    imageId = StringField(
        label='imageId',
        validators=[DataRequired()]
    )
    deletehash = StringField(
        label='deletehash',
        validators=[DataRequired()]
    )
