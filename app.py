from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, Pet
from forms import AddPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = 'nimdA'

blank_url = "https://i2.wp.com/www.awilsonsocialwork.net/wp-content/uploads/2017/01/placeholder.jpg?fit=1200%2C1200&ssl=1"

connect_db(app)
db.create_all()

@app.route('/')
def show_home_page():
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/pets/new', methods=["GET", "POST"])
def add_new_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        age = form.age.data
        photo = form.photo_url.data or blank_url
        notes = form.notes.data
        new_pet = Pet(name = name, species = species, age = age, photo_url = photo, notes = notes)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Added pet {name}")
        return redirect('/')
    else:
        print("could not validate form")
        return render_template('pets/new.html', form = form)

@app.route('/pets/<id>')
def show_pet_details(id):
    cur_pet = Pet.query.filter_by(id = id).first_or_404()
    return render_template('pets/details.html', pet = cur_pet)

@app.route('/pets/<id>/edit', methods=["GET", "POST"])
def edit_pet(id):
    pet = Pet.query.filter_by(id=id).first_or_404()
    form = AddPetForm(obj=pet)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.photo_url = form.photo_url.data or blank_url
        pet.notes = form.notes.data
        db.session.commit()
        flash(f"Updated pet {pet.name}")
        return redirect('/')
    else:
        return render_template('pets/edit.html', form = form)