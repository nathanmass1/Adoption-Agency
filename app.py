from flask import Flask, request, render_template, redirect, flash, session
from model import db, connect_db, Pet, AddPetForm, EditPetForm
from play import get_pets
import datetime
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()

params = {
  'species': 'Dog',
  'limit' : 5,
  'sort' : 'random'
}

@app.route("/")
def home_page():
    
    # Grab all the pets as a list of dictionary for pets (key word arguments) and load to the database.
    list_pets = get_pets(params)
    for pet_dict in list_pets:
        pet = Pet(**pet_dict) # Unloads the keyword arguments
        db.session.add(pet)
        db.session.commit()

    pets = Pet.query.filter_by(available = True)

    return render_template("home.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Pet add form; handle adding."""

    form = AddPetForm()
    # print("LOOOOOOOKKKKKK!!!!")
    # import pdb
    # pdb.set_trace()

    if form.validate_on_submit():
      
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name,
                species=species, photo_url=photo_url, age =age, notes=notes)

        db.session.add(pet)
        db.session.commit()
        flash("You just added {pet.name}")
        return redirect("/")

    else:
        return render_template(
            "add_pet.html", form=form)

@app.route("/pets/<int:id>")
def pet_profile(id):

        pet = Pet.query.get(id)

        return render_template("profile.html", pet = pet)


@app.route("/pets/<int:id>/edit", methods=["GET", "POST"])
def edit_pet(id):

    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)


    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data

        db.session.commit()
        return redirect(f"/pets/{id}")

    else:
        return render_template("edit_pet.html", form=form, pet=pet)




