from flask import *
from tabulate import tabulate 
from Manthan import twitterfunc, img2
import pandas as pd
import csv 
import os

# encoding: utf-8
app = Flask(__name__)
UPLOAD_FOLDER='static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        keyword=request.form['keyword']
        notw=request.form['notw']
        notw=str(notw)
        print(keyword)
        print(notw)
        twitterfunc(keyword,notw)
        filename = "result.csv"
        currentPath = os.getcwd()
        print(currentPath)
        file = os.path.join(currentPath,"Project UI",filename)
        with open(file, encoding="utf-8", newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        print(data)
        # sort csv file by sentiment score
        df = pd.read_csv(file)
        df.sort_values(by=['Sentiment_Score'], inplace=True, ascending=False)
        df.to_csv(file, index=False)
        file = os.path.join(currentPath,"Project UI",filename)
        with open(file, encoding="utf-8", newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        print("------------------------------------------------------")
        print(data)
        return render_template('view.html', result=data )
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/view')
def view():
    return render_template("view.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/image', methods=['GET','POST'])
def image():
    if request.method == "POST":
        file = request.files['image']
        file.save(file.filename)
        output=img2()
        return render_template("image_data.html", result=output )
    return render_template("image_data.html")

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')    


if __name__ == '__main__':
    app.run(debug=True , port = 3000)