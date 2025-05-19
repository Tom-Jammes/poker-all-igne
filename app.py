import os
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room
from models.table import Table
from utils.serialisation import serialiser_obj, deserialiser_obj

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)
migrate = Migrate(app, db)

# Définition des modèles SQLAlchemy
class TableModel(db.Model):
    __tablename__ = 'tables_poker'

    id = db.Column(db.Integer, primary_key=True)
    nombre_joueurs_max = db.Column(db.Integer, nullable=False)
    joueurs_en_table = db.relationship('PlayerInTable', back_populates='table') # nombre de joueur qui ont rejoint la salle
    createur = db.Column(db.String(80), nullable=False)
    etat_serialise = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, nombre_joueurs_max, createur, etat_serialise):
        self.nombre_joueurs_max = nombre_joueurs_max
        self.createur = createur
        self.etat_serialise = etat_serialise

    def __repr__(self):
        return (f"<Table {self.id}, nombre_joueurs_max: {self.nombre_joueurs_max}, createur: {self.createur}, "
                f"joueurs_en_table: {self.joueurs_en_table}, date_creation: {self.date_creation}>")

class PlayerInTable(db.Model):
    __tablename__ = 'joueurs_en_table'

    id = db.Column(db.Integer, primary_key=True)
    nom_joueur = db.Column(db.String(80), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables_poker.id'), nullable=False)
    table = db.relationship('TableModel', back_populates='joueurs_en_table')

    def __init__(self, nom_joueur, table_id):
        self.nom_joueur = nom_joueur
        self.table_id = table_id

    def __repr__(self):
        return f"<PlayerInTable nom_joueur={self.nom_joueur}, table_id={self.table_id}>"


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

        try:
            table = Table(nom_createur, nb_joueurs, montant_joueurs)
            table_serialise = serialiser_obj(table)

            # Créez une instance du modèle TableModel
            nouvelle_table_db = TableModel(nombre_joueurs_max=nb_joueurs, createur=nom_createur, etat_serialise=table_serialise)
            db.session.add(nouvelle_table_db)
            db.session.commit()
            table_id = nouvelle_table_db.id

            print(f"Table {table_id} créée par {nom_createur}")
            return render_template("rejoindreTableCreateur.html", nom_joueur=nom_createur, code_partie=table_id)
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création de la table : {e}")
            return "Erreur lors de la création de la table. Veuillez réessayer.", 500
    else:
        # Si quelqu'un essaie d'accéder à /create avec une méthode autre que GET ou POST
        return "Méthode non autorisée pour cette URL.", 405

@app.route('/join', methods=['GET'])
def page_rejoindre():
    return render_template("rejoindreTable.html")

@app.route('/join', methods=['POST'])
def rejoindre_table():
    nom_joueur = request.form.get('nomJoueur')
    table_id = request.form.get('codePartie')

    table = db.session.get(TableModel, table_id)
    if table and len(table.joueurs_en_table) < table.nombre_joueurs_max:
        # Vérifier si le joueur n'est pas déjà dans la table
        joueur_existe = PlayerInTable.query.filter_by(nom_joueur=nom_joueur, table_id=table_id).first()
        if not joueur_existe:
            nouveau_joueur = PlayerInTable(nom_joueur=nom_joueur, table_id=table_id)
            db.session.add(nouveau_joueur)
            table_deserialise = deserialiser_obj(table.etat_serialise)
            table_deserialise.ajouter_joueur(nom_joueur)
            table.etat_serialise = serialiser_obj(table_deserialise)
            db.session.commit()

            return redirect(url_for('page_salle_attente', table_id=table_id, nomJoueur=nom_joueur))
        else:
            return "Ce nom de joueur est déjà utilisé dans cette table."
    return "Impossible de rejoindre la table."

@app.route('/table/<int:table_id>')
def page_salle_attente(table_id):
    nom_joueur = request.args.get('nomJoueur')
    table = db.session.get(TableModel, table_id)
    if table:
        nombre_joueurs = len(table.joueurs_en_table)
        return render_template("tableJeu.html", table_id=table_id, nombre_joueurs=nombre_joueurs,
                               max_joueurs=table.nombre_joueurs_max, nom_joueur = nom_joueur)
    return "Table non trouvée"

# Gestion du websocket

@socketio.on('join_table')
def handle_join_table(data):
    table_id = data.get('table_id')
    nom_joueur = data.get('nom_joueur')

    table = db.session.get(TableModel, table_id)
    if table:
        join_room(str(table_id)) # Channel public pour les informations communes
        join_room(nom_joueur) # Channel privé pour les informations privées
        nombre_joueurs = len(table.joueurs_en_table)
        emit('joueur_rejoint', {
            'nom_joueur': nom_joueur,
            'nombre_joueurs': nombre_joueurs,
        }, to=str(table_id))

        if nombre_joueurs == table.nombre_joueurs_max:
            table_deserialise = deserialiser_obj(table.etat_serialise)
            table_deserialise.demarrer_tour()
            liste_noms_jetons_joueurs = {}

            for joueur in table_deserialise.joueurs:
                liste_noms_jetons_joueurs[joueur.nom] = joueur.jetons

            emit(
                'lancement_partie', {
                    "joueur_tour": table_deserialise.joueurs[table_deserialise.index_joueur_tour].nom,
                    "pot": table_deserialise.pot,
                    "joueurs": liste_noms_jetons_joueurs
                }, to=str(table_id)
            )

            for joueur in table_deserialise.joueurs:
                emit(
                    "reception_cartes", {
                        "carte1": str(joueur.main[0]),
                        "carte2": str(joueur.main[1])
                    }, to=joueur.nom
                )

            table.etat_serialise = serialiser_obj(table_deserialise)
            db.session.commit()
    # TODO retourner une erreur si il n'y a pas de table trouvé

@socketio.on('joueur_se_couche')
def handle_se_coucher(data):
    table_id = data.get('table_id')
    nom_joueur = data.get('nom_joueur')

    table = db.session.get(TableModel, table_id)
    table_deserialise = deserialiser_obj(table.etat_serialise)

    if table_deserialise.joueur_se_couche(nom_joueur):
        emit(
            'joueur_est_couche', {
                'nom_joueur': nom_joueur,
                "joueur_tour": table_deserialise.joueurs[table_deserialise.index_joueur_tour].nom,
            }, to=str(table_id)
        )
        table.etat_serialise = serialiser_obj(table_deserialise)
        db.session.commit()


@socketio.on('joueur_suit')
def handle_suivre(data):
    table_id = data.get('table_id')
    nom_joueur = data.get('nom_joueur')

    table = db.session.get(TableModel, table_id)
    table_deserialise = deserialiser_obj(table.etat_serialise)

    if table_deserialise.joueur_suit(nom_joueur):
        emit(
            'joueur_a_suivi', {
                'nom_joueur': nom_joueur,
                "joueur_tour": table_deserialise.joueurs[table_deserialise.index_joueur_tour].nom,
            }, to=str(table_id)
        )
        table.etat_serialise = serialiser_obj(table_deserialise)
        db.session.commit()

@socketio.on('joueur_mise')
def handle_mise(data):
    table_id = data.get('table_id')
    nom_joueur = data.get('nom_joueur')

    table = db.session.get(TableModel, table_id)
    table_deserialise = deserialiser_obj(table.etat_serialise)

    if table_deserialise.joueur_mise(nom_joueur):
        emit(
            'joueur_a_mise', {
                'nom_joueur': nom_joueur,
                "joueur_tour": table_deserialise.joueurs[table_deserialise.index_joueur_tour].nom,
            }, to=str(table_id)
        )
        table.etat_serialise = serialiser_obj(table_deserialise)
        db.session.commit()

# Initialisation du l'app et de la bd

@app.cli.command("init-db")
def init_db():
    """Initialise la base de données en créant les tables si elles n'existent pas."""
    print("Initialisation de la base de données ")
    with app.app_context():
        db.create_all()
        print("Base de données initialisée et table 'tables_poker' créée (si nécessaire).")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
