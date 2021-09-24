from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
#import datetime to change date format


@app.route("/")
def form():
    return render_template("create.html")

@app.route('/register', methods=["POST"])
def create_user():

    if not User.validate_user(request.form):
        # we redirect to the template with the form.
            return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    
    data = {
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    
    # We pass the data dictionary into the save method from the User class.
    id= User.save(data)

    # Don't forget to redirect after saving to the database.
    session['user_id'] = id
    return redirect('/homepage')            

@app.route('/login', methods=["POST"])
def login_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not User.validate_login(request.form):
        # we redirect to the template with the form.
            return redirect('/')

    data = {
        "email" : request.form["email"],
        "password" : request.form["pw"]
    }

    user= User.login(data)
    print(user)
    if not user:
        return redirect('/')
    elif not bcrypt.check_password_hash(user['password'], data['password']):
        flash("The password is incorrect", "login")
        return redirect('/')
    session['user_id'] = user['id']
    # Don't forget to redirect after saving to the database.
    return redirect('/homepage')  


@app.route("/homepage")
def read():
    # call the get all classmethod to get all users
    recipes= Recipe.get_all_recipes()
    user= User.get_user_info(data={'id':session['user_id']})
    return render_template("read.html", recipes=recipes, user=user)


@app.route("/recipes/new")
def addRecipe():
    # call the get all classmethod to get all users
    
    return render_template("form_recipe.html")


@app.route("/addRecipe", methods=["POST"])
def sendRecipe():
    # call the get all classmethod to get all users
    if not Recipe.validate_recipe(request.form):
        # we redirect to the template with the form.
            return redirect('/recipes/new')

    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions": request.form["instructions"],
        "under_30min": request.form["under_30min"],
        "made_on": request.form["made_on"],
        "user_id": session["user_id"]
    }

    Recipe.save(data)


    # Don't forget to redirect after saving to the database.
    return redirect('/homepage')

@app.route("/recipes/<int:id>")
def showRecipe(id):
    user= User.get_user_info(data={'id':session['user_id']})
    recipe = Recipe.get_recipe_info(data={'id':id})
    return render_template("show_recipe.html", recipe=recipe, user=user)



@app.route("/recipes/edit/<int:id>")
def editRecipe(id):
    recipe = Recipe.get_recipe_info(data={'id':id})
    print(recipe)
    return render_template("edit_recipe.html", id = id, recipe=recipe)

@app.route("/updateRecipe/<int:id>", methods=["POST"])
def updateRecipe(id):
    # call the get all classmethod to get all users
    if not Recipe.validate_recipe(request.form):
        # we redirect to the template with the form.
            return redirect('/recipes/edit/{}'.format(id))

    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions": request.form["instructions"],
        "under_30min": request.form["under_30min"],
        "made_on": request.form["made_on"],
        "user_id": session["user_id"],
        'id': id
    }

    Recipe.update(data)


    # Don't forget to redirect after saving to the database.
    return redirect('/homepage')

@app.route("/recipes/delete/<int:id>")
def deleteRecipe(id):
    Recipe.delete_recipe(data={'id':id})
    return redirect("/homepage")


@app.route("/logout")
def clearsession():
    session.clear()
    return redirect('/')