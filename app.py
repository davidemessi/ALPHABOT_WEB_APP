from flask import Flask, render_template, request
from AlphaBot import AlphaBot
import sqlite3
import time

ab = AlphaBot()
ab.stop()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    listaComandiDB = ()
    
    # prendo il comando selezionato
    comandoSelezionato = None
    if request.method == "POST":
        comandoSelezionato = list(request.form.keys())[0]

    # prendo i comandi presenti nel db
    con = sqlite3.connect('./alphaBot_DB.db')
    cur = con.cursor()
    cur.execute("SELECT nome_comando FROM Comandi")
    righe = cur.fetchall()
    listaComandiDB = [riga[0] for riga in righe]
    con.close()


    print(listaComandiDB)
    print(comandoSelezionato.lower())

    if request.method == "POST":
        if comandoSelezionato == "Avanti":
            print(comandoSelezionato)
            ab.forward()
            return render_template("index.html")

        elif comandoSelezionato == "Indietro":
            print(comandoSelezionato)
            ab.backward()
            return render_template("index.html")

        elif comandoSelezionato == "Destra":
            print(comandoSelezionato)
            ab.right()
            return render_template("index.html")

        elif comandoSelezionato == "Sinistra":
            print(comandoSelezionato)
            ab.left()
            return render_template("index.html")

        elif comandoSelezionato == "Stop":
            print(comandoSelezionato)
            ab.stop()
            return render_template("index.html")

        elif comandoSelezionato.lower() in listaComandiDB:
            print(comandoSelezionato)
            con = sqlite3.connect('./alphaBot_DB.db')
            cur = con.cursor()
            cur.execute(
                "SELECT movimento, tempi FROM Comandi WHERE nome_comando = ?",
                (comandoSelezionato.lower(),)
            )
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

    elif request.method == "GET":
        return render_template("index.html")

app.run(debug=False, host="0.0.0.0")
