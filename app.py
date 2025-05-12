import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.table import TableModel

@app.route('/')
def page_accueil():
    return render_template("index.html")

@app.route('/create', methods=['GET'])
def page_creer():
    return render_template("creerTable.html")

@app.route('/create', methods=['POST'])
def creer_nouvelle_table():
    """Traite la soumission du formulaire et crée une nouvelle table."""
    if request.method == 'POST':
        nb_joueurs = int(request.form.get('nbJoueurs'))
        montant_joueurs = int(request.form.get('montantJoueurs'))
        nom_createur = request.form.get('nomCreateur')

        # Créez une instance du modèle TableModel
        nouvelle_table_db = TableModel(nombre_joueurs=nb_joueurs, createur=nom_createur, montant_joueurs=montant_joueurs)

        try:
            db.session.add(nouvelle_table_db)
            db.session.commit()
            table_id = nouvelle_table_db.id

            print(f"Table {table_id} créée par {nom_createur}")
            return redirect(url_for('page_salle_attente', table_id=table_id))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création de la table : {e}")
            return "Erreur lors de la création de la table. Veuillez réessayer.", 500
    else:
        # Si quelqu'un essaie d'accéder à /create avec une méthode autre que GET ou POST
        return "Méthode non autorisée pour cette URL.", 405

@app.route('/join')
def page_rejoindre():
    return render_template("rejoindreTable.html")

@app.route('/salle/<int:table_id>')
def page_salle_attente(table_id):
    with app.app_context():
        table = db.session.get(TableModel, table_id)
        print("table", table.__repr__())
    return render_template("salleAttente.html")

@app.cli.command("init-db")
def init_db():
    """Initialise la base de données en créant les tables si elles n'existent pas."""
    print("Initialisation de la base de données ")
    with app.app_context():
        db.create_all()
        print("Base de données initialisée et table 'tables_poker' créée (si nécessaire).")

if __name__ == '__main__':
    app.run()
