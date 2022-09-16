from flask import Flask, flash, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
import parseSearch
import os


UPLOAD_FOLDER = './pdf_files'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

searchTerm = ""
book_list=[]
page_list=[]
length_of_list= 0

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ['POST', 'GET'])
def home():
    # variable have global so that function can change values for load_pdf function to render results page again
    global searchTerm
    global book_list
    global page_list
    global length_of_list
    if request.method == 'POST':
        # parseSearch will return a tuple, gets unwrapped into appropiate variables
        searchTerm, book_list, page_list, length_of_list = parseSearch.wordSearch(request.form['searchTerm'])
        # sends variables to searchOutput page and generates results
        # searchTerm is the serach term
        # book_list is a list of books the term was found in
        # page_list is list of key value pairs of the page number and the hyperlink to open specific book to specific page
        # length_0f_list is a variable to hold length of book_list so for loop in searchOutput.html can loop through appropiate amount of times
        if(length_of_list == 0):
            searchTerm += " was not found in data/PDF files"
        return render_template("searchOutput.html", searchTerm=searchTerm, book_list=book_list, page_list=page_list, length_of_list=length_of_list)
    else:
        return render_template("index.html", flasktext = "Enter Search Term")

    if request.method == 'GET':
        #renders upload pdf page
        return render_template("upload.html")

@app.route("/upload", methods = ['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            # if it doesn't, page will reload
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            #if there is no file in upload form, page will reload
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #pdf file will upload into pdf_files folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #and then parser will process
            parseSearch.pdfParser(filename)
            return render_template("uploadSuccess.html", filename=filename)
    #else renders upload page again
    return render_template("upload.html")

@app.route("/searchOutput", methods=['POST', 'GET'])
def load_pdf():
    #load pdf on default browser
    if request.method == 'POST':
        parseSearch.pdfOpen(request.form['pdfName'])
        #render searchOutput page again
        return render_template("searchOutput.html", searchTerm=searchTerm, book_list=book_list, page_list=page_list, length_of_list=length_of_list)
    else:
        return render_template("searchOutput.html", searchTerm=searchTerm, book_list=book_list, page_list=page_list, length_of_list=length_of_list)




if __name__ == "__main__":
    app.run(debug=True)