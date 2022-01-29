from flask import Flask, redirect, request, session, url_for
from flask.templating import render_template
import json
from selenium import webdriver
from tenacity import time
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)
app.config["SECRET_KEY"] = "IMTHEHUNTER89@#0"

def fetch_wiki(subject):
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.google.com/search?q=" + subject + " wikipedia")
        link = driver.find_element_by_xpath('//div[@class="yuRUbf"]').find_element_by_tag_name('a').get_attribute('href')
        driver.get(link)
        parent_div = driver.find_element_by_xpath('//div[@class="mw-parser-output"]')
        paragraphs = parent_div.find_elements_by_tag_name('p')[1:3]
        result = ""
        one_time = False
        for p in paragraphs:
            if one_time == False:
                result = result + p.text + "\n\n"
                one_time = True
            else:
                result = result + p.text
    except NoSuchElementException:
        result = "NEEDS TO BE CHANGED"
    driver.close()
    return result

def fetch_duration(subject):
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.google.com/search?q=" + subject + " duration")
        duration = driver.find_element_by_xpath('//div[@class="DI6Ufb"]').find_element_by_xpath('//div[@class="Z0LcW"]').text
    except NoSuchElementException:
        duration = "50 Minutes Each Episode"
    driver.close()
    return duration

def fetch_release_year(subject):
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.google.com/search?q=" + subject + " release date")
        release_date = driver.find_element_by_xpath('//div[@class="DI6Ufb"]').find_element_by_xpath('//div[@class="Z0LcW"]').text
        seperated = release_date.split(" ")
        release_year = seperated[-1]
    except NoSuchElementException:
        release_year = 2000
    driver.close()
    return release_year

def read_db():
    with open("db.json", 'r', encoding='utf-8') as db_file:
        database = json.load(db_file)
    return database

def write_db(data):
    with open("db.json", 'w', encoding='utf-8') as db_file:
        json.dump(data, db_file)

def read_temp_furls():
    with open("temp_furls.json", 'r', encoding='utf-8') as temp_furls_file:
        temp_furls = json.load(temp_furls_file)
    return temp_furls

def write_temp_furls(data):
    with open("temp_furls.json", 'w', encoding='utf-8') as temp_furls_file:
        json.dump(data, temp_furls_file)

def read_temp_content():
    with open("temp_content.json", 'r', encoding='utf-8') as temp_content_file:
        temp_content = json.load(temp_content_file)
    return temp_content    

def write_temp_content(data):
    with open("temp_content.json", 'w', encoding='utf-8') as temp_content_file:
        json.dump(data, temp_content_file)

def editor_write(data):
    with open("editor.txt", 'w') as editor_file:
        editor_file.write(data)

def editor_read():
    with open("editor.txt", 'r') as editor_file:
        editor_response = editor_file.read()
    return editor_response

def fileadded_write(data):
    with open("fileadded.txt", 'w') as fileadded_file:
        fileadded_file.write(data)

def fileadded_read():
    with open("fileadded.txt", 'r') as fileadded_file:
        fileadded_response = fileadded_file.read()
    return fileadded_response

@app.route("/", methods=["GET", "POST"])
def home():
    session.pop('previousurl', None)
    database = read_db()
    all_content = database['allcontent']
    return render_template("index.html", contents=all_content)

@app.route("/savetempcontent", methods=["GET", "POST"])
def savetempcontent():
    if request.method == "POST":
        data = {}
        data['ctitle'] = request.json['ctitle']
        data['imgurl'] = request.json['imgurl']
        data['lang'] = request.json['lang']
        data['category'] = request.json['category']
        data['subt'] = request.json['subt']
        data['fmat'] = request.json['fmat']
        write_temp_content(data)

@app.route("/saveedittempcontent", methods=["GET", "POST"])
def saveedittempcontent():
    if request.method == "POST":
        editor_write("True")
        data = {}
        data['ctitle'] = request.json['ctitle']
        data['imgurl'] = request.json['imgurl']
        data['desc'] = request.json['desc']
        data['lang'] = request.json['lang']
        data['ryear'] = request.json['ryear']
        data['duration'] = request.json['duration']
        data['category'] = request.json['category']
        data['subt'] = request.json['subt']
        data['fmat'] = request.json['fmat']
        write_temp_content(data)

@app.route("/add-content", methods=["GET", "POST"])
def add_content():
    if fileadded_read() == "True":
        temp_furls = read_temp_furls()
        return render_template("addcontent.html", fileurls=temp_furls['fileUrls'], fileadded=True, temp_content=read_temp_content())
    return render_template("addcontent.html")

@app.route("/addfileurl", methods=["GET", "POST"])
def addfileurl():
    time.sleep(1)
    session['previousurl'] = request.referrer
    temp_content = read_temp_content()
    if temp_content['category'] == "Movie":
        return render_template("addfileurl.html", movie=True, temp_content=temp_content)
    elif temp_content['category'] == "Web Series":
        return render_template("addfileurl.html", webseries=True, temp_content=temp_content)

@app.route("/add_file", methods=["GET", "POST"])
def add_file():
    if request.method == "POST":
        linktext = request.form['linkText']
        downloadtext = request.form['downloadText']
        downloadLink = request.form['downloadLink']
        temp_furls = read_temp_furls()
        try:
            if temp_furls['fileUrls'] != None:
                cur_key = max(temp_furls['fileUrls'].keys())
                required_key = int(cur_key) + 1
                required_key = str(required_key)
                temp_furls['fileUrls'][required_key] = {
                    "linkSpec": linktext,
                    "downloadText": downloadtext,
                    "downloadLink": downloadLink
                }
                write_temp_furls(temp_furls)
            else:
                temp_furls['fileUrls'] = {
                    "1": {
                        "linkSpec": linktext,
                        "downloadText": downloadtext,
                        "downloadLink": downloadLink
                    }
                }
                write_temp_furls(temp_furls)
        except KeyError:
            temp_furls['fileUrls'] = {
                "1": {
                    "linkSpec": linktext,
                    "downloadText": downloadtext,
                    "downloadLink": downloadLink
                }
            }
            write_temp_furls(temp_furls)
        temp_furls = read_temp_furls()
        fileadded_write("True")
        if editor_read() == "True":
            return redirect(session['previousurl'])
        else:
            return redirect(url_for('add_content'))

@app.route("/addcontent", methods=["GET", "POST"])
def addcontent():
    if request.method == "POST":
        contenttitle = request.form['contenttitle']
        imgurl = request.form['imgurl']
        language = request.form['language']
        category = request.form['category']
        subtitles = request.form['subtitles']
        fmat = request.form['format']
        file_urls = read_temp_furls()
        database = read_db()
        all_keys = []
        for key in database['allcontent'].keys():
            all_keys.append(int(key))
        cur_key = max(all_keys)
        required_key = cur_key + 1
        required_key = str(required_key)
        database['allcontent'][required_key] = {
            "movieInfo": {
                "Duration": fetch_duration(contenttitle),
                "Language": language,
                "Category": category,
                "Release Year": fetch_release_year(contenttitle),
                "Subtitles": subtitles,
                "Format": fmat
            },
            "fileUrl": file_urls['fileUrls'],
            "imgUrl": imgurl,
            "movieName": contenttitle,
            "description": fetch_wiki(contenttitle)
        }
        write_db(database)
        new_temp_data = {}
        write_temp_furls(new_temp_data)
        write_temp_content(new_temp_data)
        fileadded_write("False")
        return redirect(url_for('home'))

@app.route("/editcontent/<string:content_id>", methods=["GET", "POST"])
def editcontent(content_id):
    try:
        ex = read_temp_furls()['fileUrls']
        database = read_db()
        allcontents = database['allcontent']
        for key, details in allcontents.items():
            if str(key) == str(content_id):
                required_content = details
                release_year = required_content['movieInfo']['Release Year']
    except KeyError:
        database = read_db()
        allcontents = database['allcontent']
        for key, details in allcontents.items():
            if str(key) == str(content_id):
                required_content = details
                release_year = required_content['movieInfo']['Release Year']
                temp_furls = read_temp_furls()
                temp_furls['fileUrls'] = required_content['fileUrl']
                write_temp_furls(temp_furls)
    temp_furls = read_temp_furls()
    if fileadded_read() == "True":
        return render_template("editcontent.html", fileurls=temp_furls['fileUrls'], fileadded=True, temp_content=read_temp_content(), cid=content_id)
    return render_template("editcontent.html", content=required_content, ryear=release_year, fileurls=temp_furls['fileUrls'], cid=content_id)

@app.route("/savecontent/<string:content_id>", methods=["GET", "POST"])
def savecontent(content_id):
    if request.method == "POST":
        contenttitle = request.form['contenttitle']
        imgurl = request.form['imgurl']
        description = request.form['description']
        releaseyear = request.form['releaseyear']
        duration = request.form['duration']
        language = request.form['language']
        category = request.form['category']
        subtitles = request.form['subtitles']
        format = request.form['format']
        fileurls = read_temp_furls()
        database = read_db()
        database['allcontent'][str(content_id)] = {
            "movieInfo": {
                "Duration": duration,
                "Language": language,
                "Category": category,
                "Release Year": releaseyear,
                "Subtitles": subtitles,
                "Format": format
            },
            "fileUrl": fileurls['fileUrls'],
            "imgUrl": imgurl,
            "movieName": contenttitle,
            "description": description
        }
        write_db(database)
        new_temp_data = {}
        write_temp_content(new_temp_data)
        write_temp_furls(new_temp_data)
        editor_write("False")
        fileadded_write("False")
        return redirect(url_for('home'))

@app.route("/deletefileurl/<string:fileurlid>", methods=["GET", "POST"])
def deletefileurl(fileurlid):
    temp_urls = read_temp_furls()
    temp_urls['fileUrls'].pop(fileurlid)
    write_temp_furls(temp_urls)
    fileadded_write("True")
    return redirect(request.referrer)

@app.route("/editfileurl/<string:fileurlid>", methods=["GET", "POST"])
def editfileurl(fileurlid):
    temp_urls = read_temp_furls()
    session['previousurl'] = request.referrer
    fileadded_write("True")
    for key, details in temp_urls['fileUrls'].items():
        if str(key) == str(fileurlid):
            return render_template("editfileurl.html", file=details, id=key)

@app.route("/edit_file/<string:file_id>", methods=["GET", "POST"])
def edit_file(file_id):
    linkSpec = request.form['linkText']
    downloadText = request.form['downloadText']
    downloadLink = request.form['downloadLink']
    temp_furls = read_temp_furls()
    file = temp_furls['fileUrls'][file_id]
    file['linkSpec'] = linkSpec
    file['downloadText'] = downloadText
    file['downloadLink'] = downloadLink
    write_temp_furls(temp_furls)
    preurl = session['previousurl']
    return redirect(preurl)

@app.route("/deletecontent/<string:cid>", methods=["GET", "POST"])
def deletecontent(cid):
    database = read_db()
    database['allcontent'].pop(str(cid))
    write_db(database)
    return redirect(request.referrer)

@app.route("/discardedit", methods=["GET", "POST"])
def discardedit():
    new_temp_data = {}
    write_temp_content(new_temp_data)
    write_temp_furls(new_temp_data)
    editor_write("False")
    fileadded_write("False")
    return redirect(url_for('home'))

app.run(debug=True)
