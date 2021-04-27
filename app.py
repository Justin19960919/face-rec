# Flask
from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory, abort
from werkzeug.utils import secure_filename

# support
import os
import json
import requests

# face_recognition 
from detect import label_image
# fetch news
from newsAPI import readNews


#pip3 install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy



# google sheet api and google drive api

# dependencies
from saveToSheets import saveToGoogleSheets






app = Flask(__name__)
app.secret_key = "some secret key you made up"


# upload configurations
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',"gif"}
app.config['UPLOAD_FOLDER'] = "upload/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # This sets the max upload to 16 mb (1024*1024)


# sqlite:////tmp/test.db
# db configurations
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False


# configure db
db = SQLAlchemy(app)

# Represent user object
class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True) # store an integer id as PK
    email = db.Column(db.String(100))
    feedback = db.Column(db.String(200))


    def __init__(self,email,feedback):
        self.email = email
        self.feedback = feedback



####### self defined functions ####### 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_images(route):
    dir_files = os.listdir(route)
    if len(dir_files) == 0:
        return
    # else remove all
    for p_file in dir_files:
        os.remove(os.path.join(route,p_file))
    print(f"Removed all files in {route}")






# Home
@app.route("/")
def home():
    return render_template("home.html")



# Uploads / Outputs

# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
@app.route("/upload",methods = ["GET","POST"])
def upload():
   if request.method == "GET":
        return render_template("upload.html")
    # curently not very secure
    # add progress bar and wait icon
   elif request.method == 'POST':
        print("we got the post request")

        # # remove all images from the specified directory
        # remove_images("./upload")
        # remove_images("./static/results")
        
        f = request.files['uploadFile']
        if f.filename != '':
            flash("Loading and matching..","info")
            saved_filename = secure_filename(f.filename)
            saved_route =  os.path.join(app.config['UPLOAD_FOLDER'],saved_filename)
            f.save(
                saved_route
               )
            label_image(saved_route)
            return redirect(url_for("output"))
        else:
            flash("User didn't select a photo ","error")
            return render_template("upload.html")


@app.route("/output")
def output():
    return render_template("output.html")






# News
@app.route("/news")
def news():
    display_news = readNews()
    return render_template("news.html",news_data = display_news)




# Newsletters (not yet implemented)
@app.route("/newsletter",methods = ["POST","GET"])
def signup():
    # return "we are at the newsletter signup page"
    if request.method == "POST":
        # ok , I got the form data
        email = request.form['emailInput']
        feedback = request.form['feedBack']
        print(email,feedback)

        # check if user already exists
        found_user = users.query.filter_by(email=email).first()
        if found_user:
            flash("You already signed up for the Newsletter! ","error")
        # add one
        else:
            usr = users(email,feedback)
            db.session.add(usr)         # add usr to db
            db.session.commit()                 # commit to db
            flash("Congratulations! Your email was saved..","info")

        return redirect(url_for("signup"))

    else:
        return render_template("newsletter.html")




# route to view all users
@app.route("/viewUsers")
def view():
    allUsers = users.query.all()
    
    userData = list(map(lambda x:[x.email,x.feedback],allUsers))
    # save to the google sheets
    saveToGoogleSheets(userData)
    # success
    return render_template("view.html",values = users.query.all())





# Companies
# introduce users to the 7 companies
@app.route("/companies")
def getCompanies():
    return render_template("companies.html")





# updates changes in the server automatically and shows debug
if __name__ == "__main__":
    db.create_all() # create db if it doesn't already exist
    # app.run(debug=True)
    app.run()

