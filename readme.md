# Kpop101

### Overview
This is a python Flask web app aimed to provide Users with the experience of getting into the
KPOP world. People who want to get into kpop often suffer from not being able to discriminate KPOP
stars and the overwhelming information beforehand. This app provides four features, mainly: facial
recognition, latest news, a newsletter to subscribe,and a brief introduction of korean entertainment
companies. 

### Technologies
The Flask app is incorporated with Bootstap4, making the website responsive. Facial recognition feature
is built using the dllib library of python (face-rec). Latest News is built incorporating GNews api to 
fetch latest kpop news. Users that subscibe to the newletter are feeded into the Google excel api and 
google drive api to update. 

### Dependencies
As specified in the requirements.txt file, this project uses several packages, including:

* flask==1.1.2
* requests==2.24.0
* gspread==3.6.0
* oauth2client==4.1.3
* Flask-SQLAlchemy==2.4.4
* Werkzeug==1.0.1
* python-dotenv==0.15.0
* boost
* cmake
* dlib
* face-recognition==1.3.0
* face-recognition-models==0.3.0


### Build
To build the website, run:
```
python app.py
```
to build the website.
The run on localhost:5000/


### Features
- Facial Recognition
  - Use the Python library 'face-rec' which is built on cmake and dlib to do facial recognition
  - Compares user upload photos with photos in the known folder (containing known Kpop idol photos)
  - Identifies and puts a square with the predicted name beside the photo's people

- Latest News
  - Incorporating the GNews Api to fetch latest Kpop news
  - To fetch Kpop news, run newsAPI.py to download 20 pieces of new to a file called news.txt (which would ideally be done using a cronjob)

- Newsletter
  - Uses the Google Excel Api / Google Drive API to write user emails to a google excel online spreadsheet
  - The API key is hidden ,hence you might need to apply for your own API key

- Introduction to korean entertainment companies
  - Using Bootstap cards to display the company information


### Website 

*Landing Page*
<img src="/demo/home.png" alt="Home page"/>

*Face recognition*
<img src="/demo/upload.png" alt="face-rec"/>

*Face recognition Results*
<img src="/demo/detection_results.png" alt="face-results"/>

*Latest News*
<img src="/demo/news.png" alt="News"/>

*NewsLetter*
<img src="/demo/newsletter.png" alt="Newsletter"/>

*Companies*
<img src="/demo/companies.png" alt="companies"/>



