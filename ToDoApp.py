from flask import Flask
app = Flask(__name__)

@app.route("/")
def indec():
    return "Hello, World"

app.run(debug=True)