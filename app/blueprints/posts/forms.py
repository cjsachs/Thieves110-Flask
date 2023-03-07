from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, StringField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    img_url = StringField('Image URL', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    caption = StringField('Caption', validators=[DataRequired()])
    submit_btn = SubmitField('Post')