from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
import os

# import face_recognition function
from detect import label_image


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


# passing paramters
# @app.route("/<name>")
# def home(name):
#     return render_template("home.html",name = name)


UPLOAD_FOLDER = "./upload/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#This sets the max upload to 16 mb
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


####### self defined functions ####### 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_detected_image():
    target_dir = "./static/results/"
    dir_files = os.listdir(target_dir)
    for p_file in dir_files:
        if p_file == "detected_image.jpg":
            os.remove(os.path.join(target_dir,p_file))

###################################


@app.route("/upload",methods = ["GET","POST"])
def upload():

    # delete all files in upload and results
    remove_detected_image()

    if request.method == "GET":
        return render_template("upload.html")
    
    elif request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['uploadFile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_route = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_route)
            #return redirect(url_for('uploaded_file',filename=filename))
            # return "Uploaded file.."
            
            label_image(upload_route)
            return render_template("output.html")


@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/concerts")
def concert():
    return render_template("concerts.html")

@app.route("/newsletter",methods = ["POST","GET"])
def signup():
    # return "we are at the newsletter signup page"
    if request.method == "POST":
        # ok , I got the form data
        email = request.form['emailInput']
        feedback = request.form['feedBack']
        return f"<p>{email}</p>\
                 <p>{feedback}</p>"
        # save to db , implement later

    else:
        return render_template("newsletter.html")








# updates changes in the server automatically
if __name__ == "__main__":
    app.run(debug=True)

