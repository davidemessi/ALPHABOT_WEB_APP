from flask import Flask, render_template,request

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])

def index():
    if request.method=="POST":
        if "Avanti" in request.form:
            return "<p>avanti</p>"
        elif "Indietro" in request.form:
            return "<p>indietro</p>"
        elif "Destra" in request.form:
            return "<p>destra</p>"
        elif "Sinistra" in request.form:
            return "<p>sinistra</p>"
    elif request.method=="GET":
        return render_template("index.html")
    

app.run(debug=True, host="0.0.0.0")