const socket = io();
const tableId = document.getElementById("table-id");
const nomJoueur = document.getElementById("nom-joueur");
const nbJoueursConnectes = document.getElementById("joueurs-connectes");
const salleAttente = document.getElementById("salle-attente")
const jeuLance = document.getElementById("jeu-lance")
const btnFold = document.getElementById("btn-fold")
const btnCall = document.getElementById("btn-call")
const btnBet = document.getElementById("btn-bet")

btnFold.addEventListener("click", fold)
btnCall.addEventListener("click", call)
btnBet.addEventListener("click", bet)

function fold() {
    socket.emit(
        'joueur_se_couche',
        {
            table_id: tableId.textContent,
            nom_joueur: nomJoueur.textContent
        }
    )
}

function call() {
    socket.emit(
        'joueur_suit',
        {
            table_id: tableId.textContent,
            nom_joueur: nomJoueur.textContent
        }
    )
}

function bet() {
    socket.emit(
        'joueur_sur_encheri',
        {
            table_id: tableId.textContent,
            nom_joueur: nomJoueur.textContent
        }
    )
}

socket.on('connect', () => {
    console.log("Socket connectée !");
    socket.emit('join_table', {
        table_id: tableId.textContent,
        nom_joueur: nomJoueur.textContent
    });
});

socket.on('joueur_rejoint', (data) => {
    console.log(`${data.nom_joueur} a rejoint la table.`);
    nbJoueursConnectes.textContent = `${data.nombre_joueurs}`
});

socket.on('lancement_partie', (data) => {
    console.log(`La partie est lancée`);
    salleAttente.classList.add("hidden")
    jeuLance.classList.remove("hidden")
});

socket.on('joueur_est_couche', (data) => {
    console.log(`${data.nom_joueur} est couché.`);
});

socket.on('joueur_a_suivi', (data) => {
    console.log(`${data.nom_joueur} a suivi.`);
});

socket.on('joueur_a_sur_encheri', (data) => {
    console.log(`${data.nom_joueur} sur encheri.`);
});