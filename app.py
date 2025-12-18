from flask import Flask, render_template, request
from AlphaBot import AlphaBot
import sqlite3
import time

ab = AlphaBot()
ab.stop()

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])

def index():
    if request.method=="POST":
        if "Avanti" in request.form:
            ab.forward()
            return render_template("index.html")
        elif "Indietro" in request.form:
            ab.backward()
            return render_template("index.html")
        elif "Destra" in request.form:
            ab.right()
            return render_template("index.html")
        elif "Sinistra" in request.form:
            ab.left()
            return render_template("index.html")
        elif "Stop" in request.form:
            ab.stop()
            return render_template("index.html")
        elif "Quadrato" in request.form:
            comando = "quadrato"
            con = sqlite3.connect('./alphaBot_DB.db')
            cur = con.cursor()
            cur.execute(f"SELECT movimento, tempi FROM Comandi WHERE nome_comando LIKE '{comando}'")
            righe = cur.fetchall()
            print(f"Righe: {righe}")
            con.close()

            movimenti, tempi = righe[0]
            lista_mov = [m.strip() for m in movimenti.split(',')]
            lista_tempi = [t.strip() for t in tempi.split(',')]

            for mov, tempi in zip(lista_mov, lista_tempi):
                if mov == 'avanti':
                    ab.forward()
                    time.sleep(float(tempi))
                if mov == 'indietro':
                    ab.backward()
                    time.sleep(float(tempi))
                if mov == 'destra':
                    ab.right()
                    time.sleep(float(tempi))
                if mov == 'sinistra':
                    ab.left()
                    time.sleep(float(tempi))
                if mov == 'aspetta':
                    ab.stop()
                    time.sleep(float(tempi))
            return render_template("index.html")
        elif "AvantiIndietro" in request.form:
            ab.stop()
            return render_template("index.html")
    elif request.method=="GET":
        return render_template("index.html")
    

app.run(debug=False, host="0.0.0.0")