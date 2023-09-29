import os
from flask import Flask, request, redirect, render_template, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

mongo_url = os.getenv('MONGO_URL', "mongodb://localhost:27017/")
myclient = MongoClient(mongo_url)
plants_db = myclient["plants"]
plants = plants_db["plants"]
harvests_db = myclient["harvests"]
harvests = harvests_db["harvests"]

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""

    # Makes a database call to retrieve *all* plants from the Mongo database's `plants` collection.
    plants_data = plants.find()

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

# Create Custom Error Page for an invalid URL
@app.errorhandler(404)
def page_not_found(e):
    """Displays a custom 404 error page if the user enters an invalid URL"""
    return render_template('404.html'), 404

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        # Gets the new plant's name, variety, photo, & date planted, and 
        # stores them in the new_plant object.
        plant_name = request.form.get('plant_name')
        new_plant = {
            'name': plant_name,
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo'),
            'date_planted': request.form.get('date_planted'),
        }
        # Makes an `insert_one` database call to insert the object into the
        # database's `plants` collection, and get its inserted id. Passes the 
        # inserted id into the redirect call.

        new_plant_id = plants.insert_one(new_plant).inserted_id

        return redirect(url_for('detail', plant_id= new_plant_id))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""
    # Makes a database call to retrieve *one* plant from the database, 
    # whose id matches the id passed in via the URL.
    searchParams = {'_id': ObjectId(plant_id)}
    selected_plant_document = plants.find_one(searchParams)

    # Uses the `find` database operation to find all harvests for the plant's id.  
    # This query is on the `harvests` collection, not the `plants` collection.
    searchParams = {'plant_id': plant_id}
    harvests_result = harvests.find(searchParams)

    context = {
        'plant' : selected_plant_document,
        'harvests': harvests_result
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """

    # Creates a new harvest object by passing in the form data from the
    # detail page form.
    new_harvest = {
        'quantity': request.form.get('harvested_amount'), # e.g. '3 tomatoes'
        'date': request.form.get('date_harvested'),
        'plant_id': plant_id,
    }

    # Makes an `insert_one` database call to insert the object into the 
    # `harvests` collection of the database.

    harvests.insert_one(new_harvest)
    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # Makes an `update_one` database call to update the plant with the
        # given id. Make sure to put the updated fields in the `$set` object.
        searchParams = {'_id': ObjectId(plant_id)}
        updated_values = { '$set':
            {'name': request.form.get('plant_name'),
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo'),
            'date_planted': request.form.get('date_planted')},
        }
        plants.update_one(searchParams, updated_values)
        
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # Makes a `find_one` database call to get the plant object with the passed-in _id.
        searchParams = {'_id': ObjectId(plant_id)}
        plant_to_show = plants.find_one(searchParams)

        context = {
            'plant': plant_to_show
        }
        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    """Deletes the plant whose id was passed in."""
    # Makes a `delete_one` database call to delete the plant with the given id.
    searchParams = {'_id': ObjectId(plant_id)}
    plants.delete_one(searchParams)

    # Makes a `delete_many` database call to delete all harvests with the given plant id.
    searchParams = {'plant_id': plant_id}
    harvests.delete_many(searchParams)

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True)

