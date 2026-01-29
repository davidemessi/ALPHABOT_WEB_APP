from flask import Flask, render_template, request
from AlphaBot import AlphaBot
import sqlite3
import time

ab = AlphaBot()
ab.stop()

VELOCITA_FORTE = 100     # avanti / indietro
VELOCITA_PIANO = 40
VELOCITA_CURVA = 40     # destra / sinistra

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    listaComandiDB = ()
    
    comandoSelezionato = None
    if request.method == "POST":
        comandoSelezionato = list(request.form.keys())[0]

    con = sqlite3.connect('./alphaBot_DB.db')
    cur = con.cursor()
    cur.execute("SELECT nome_comando FROM Comandi")
    righe = cur.fetchall()
    listaComandiDB = [riga[0] for riga in righe]
    con.close()

    print(listaComandiDB)
    print(comandoSelezionato)

    if request.method == "POST":

        if comandoSelezionato == "AvantiForte":
            print(comandoSelezionato)
            ab.setMotor(VELOCITA_FORTE, VELOCITA_FORTE)
            ab.forward()
            return render_template("index.html")
        
        elif comandoSelezionato == "AvantiPiano":
            print(comandoSelezionato)
            ab.setMotor(-VELOCITA_PIANO, -VELOCITA_PIANO)
            ab.forward()
            return render_template("index.html")

        elif comandoSelezionato == "IndietroForte":
            print(comandoSelezionato)
            ab.setMotor(-VELOCITA_FORTE, -VELOCITA_FORTE)
            ab.backward()
            return render_template("index.html")
        
        elif comandoSelezionato == "IndietroPiano":
            print(comandoSelezionato)
            ab.setMotor(-VELOCITA_PIANO, -VELOCITA_PIANO)
            ab.backward()
            return render_template("index.html")

        elif comandoSelezionato == "Destra":
            print(comandoSelezionato)
            ab.setMotor(VELOCITA_CURVA, VELOCITA_CURVA)
            ab.right()
            return render_template("index.html")

        elif comandoSelezionato == "Sinistra":
            print(comandoSelezionato)
            ab.setMotor(VELOCITA_CURVA, VELOCITA_CURVA)
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
            con.close()

            movimenti, tempi = righe[0]
            lista_mov = [m.strip() for m in movimenti.split(',')]
            lista_tempi = [t.strip() for t in tempi.split(',')]

            for mov, t in zip(lista_mov, lista_tempi):

                if mov == 'avanti':
                    ab.setMotor(VELOCITA_FORTE, VELOCITA_FORTE)
                    ab.forward()
                    time.sleep(float(t))

                elif mov == 'indietro':
                    ab.setMotor(-VELOCITA_FORTE, -VELOCITA_FORTE)
                    ab.backward()
                    time.sleep(float(t))

                elif mov == 'destra':
                    ab.setMotor(VELOCITA_CURVA, VELOCITA_CURVA)
                    ab.right()
                    time.sleep(float(t))

                elif mov == 'sinistra':
                    ab.setMotor(VELOCITA_CURVA, VELOCITA_CURVA)
                    ab.left()
                    time.sleep(float(t))

                elif mov == 'stop':
                    ab.stop()

            return render_template("index.html")

    return render_template("index.html")


app.run(debug=False, host="0.0.0.0")
