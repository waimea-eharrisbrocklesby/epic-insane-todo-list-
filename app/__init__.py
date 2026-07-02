#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Todo list page - Show all the todos
#-----------------------------------------------------------
@app.get("/index")
def show_all_creatures():
    with connect_db() as db:
        sql = """
            SELECT id, priority, name, status
            FROM creatures
        """
        params = ()
        creatures = db.execute(sql, params).fetchall()

        return render_template("pages/index.jinja", creatures=creatures)


#-----------------------------------------------------------
# Tik page - Update the status of a todo
#-----------------------------------------------------------

@app.get("/creatures/<int:id>/Tik")
def update_creature_status(id):
    with connect_db() as db:
        sql = """
            UPDATE creatures
            SET status = 1
            WHERE id = ?
        """
        params = (id,)
        db.execute(sql, params)

        #done so back to list
        flash("task completed successfully!", "success")
        return redirect("/index")

#-----------------------------------------------------------
# New Task post handler
#-----------------------------------------------------------
@app.post("/creatures/new")
def process_new_creature_form():

    #get data from form
    priority = request.form.get("Priority", "3").strip()
    name = request.form.get("name", "").strip()

    #connect to db
    with connect_db() as db:
        sql = """
            INSERT INTO creatures (priority, name)
            VALUES (?, ?)
        """

        params = (
            priority,
            name
        )

        #run the query
        db.execute(sql, params)

        flash(f"Task ({name}) added successfully!", "success")

        #done so back to listy
        return redirect("/index")



#-----------------------------------------------------------
# Creature delete handler - Delete a creature
#-----------------------------------------------------------
@app.get("/creatures/<int:id>/delete")
def delete_a_creature(id):
    with connect_db() as db:
        #delete the creature using id
        sql = """
            DELETE FROM creatures
            WHERE id = ?
        """
        params = (id,)
        db.execute(sql, params)

        #done so back to list
        flash("Creature deleted successfully!", "success")
        return redirect("/index")

#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

