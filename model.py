from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField,  BooleanField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, URL, AnyOf, Length
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class Pet(db.Model):
    """ Pet table """

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50), 
                      nullable=False)

    species = db.Column(db.String(50),
                        nullable=False)

    photo_url = db.Column(db.String(500))

    age = db.Column(db.Integer,
                        nullable=False)

    notes = db.Column(db.String(500)) 

    available = db.Column(db.Boolean, default=True) 
    

class AddPetForm(FlaskForm):
    """Form for adding pets"""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species Name", validators=[InputRequired(), AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField("Photo URL", validators=[URL(), Optional()])
    age = IntegerField("Age", validators=[InputRequired(), NumberRange(min=0, max=30)])
    notes = StringField("Notes")


class EditPetForm(FlaskForm):
    """Form for editing an existing pet."""

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()],
    )

    notes = TextAreaField(
        "Comments",
        validators=[Optional(), Length(min=10)],
    )

    available = BooleanField("Available?")    