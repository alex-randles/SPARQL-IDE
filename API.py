# imported modules
from flask import Flask, render_template, request, send_file, send_from_directory
from werkzeug import secure_filename
import os
import rdflib

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# to prevent caching of previous result
file_counter = 0
app.config["allowed_file_extensions"] = ["csv", "xls", "json"]
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
file_name = ""




class API:

    def __init__(self):
        app.run(host="127.0.0.1", port="5000", threaded=True, debug=True)

    @staticmethod
    def create_output_file(data,filename):
        output_file = open(filename, "w")
        output_file.write(data)

    @staticmethod
    def compare_files(file_1, query):
        g = rdflib.graph.Graph()
        # ... add some triples to g somehow ...
        g.parse(file_1, format='n3')
        result = []
        query_result = g.query(query)
        for result in query_result:
            print(result)
        return query_result

    @app.route("/", methods=["GET", "POST"])
    def display_results():
        if request.method == "POST":
            # get file uploaded
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_extension = (filename.split(".")[1]).lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            saved_file = file.save(file_path)
            query = request.form.get("query")
            query_result = API.compare_files(file_path, query)
            headings = ["SUBJECT", "PREDICATE", "OBJECT"]
            return render_template("post.html", result=query_result, headers=headings)
        else:
            return render_template("get.html")

    @app.route("/download-file/", methods=["GET"])
    def return_file():
        print("Downloading file.......")
        download_path = "test_output.ttl"
        return send_file(download_path, as_attachment=True, cache_timeout=0)


if __name__ == "__main__":
    # start api
    API()