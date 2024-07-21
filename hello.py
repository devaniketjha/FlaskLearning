from flask import Flask, render_template, abort


# Crete a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route("/")

def index():
    return "Hello World."

@app.route("/user/<name>")

def user(name):
    
    return render_template("index.html", name=name)

@app.route('/error')
def error():
    abort(500)  # This will raise a 500 Internal Server Error

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)