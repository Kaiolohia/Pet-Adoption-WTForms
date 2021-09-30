from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Optional, URL, InputRequired, EqualTo, ValidationError

def validate_species(form, field):
        if field.data.lower() not in ("cat" "dog" "porcupine"):
            raise ValidationError('Species must be either cat, dog, or porcupine')

class AddPetForm(FlaskForm):
    name = StringField("Pet name", [InputRequired(message = "Name cannot be blank")], render_kw={"placeholder":"Junior"})
    species = StringField("Species", [InputRequired(), validate_species], render_kw={"placeholder":"Pug"})
    age = IntegerField("Age of pet", render_kw={"placeholder":"12"})
    photo_url = StringField("Photo of pet (url)", [Optional(), URL(message = "Must be a valid URL | Or no URL at all")])
    notes = StringField("Additional notes", render_kw={"placeholder":"Loves to cuddle"})