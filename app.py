from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def page_accueil():
    return render_template("index.html")

@app.route('/create')
def page_creer():
    return render_template("creerTable.html")

@app.route('/join')
def page_rejoindre():
    return render_template("rejoindreTable.html")

@app.route('/salle-attente')
def page_salle_attente():
    return render_template("salleAttente.html")

if __name__ == '__main__':
    app.run()
