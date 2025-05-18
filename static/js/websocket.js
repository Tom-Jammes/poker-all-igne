const socket = io();
const tableId = document.getElementById("table-id").textContent;
const nomJoueur = document.getElementById("nom-joueur").textContent;
const nbJoueursConnectes = document.getElementById("joueurs-connectes");
const salleAttente = document.getElementById("salle-attente")
const jeuLance = document.getElementById("jeu-lance")
const btnFold = document.getElementById("btn-fold")
const btnCall = document.getElementById("btn-call")
const btnBet = document.getElementById("btn-bet")

btnFold.addEventListener("click", fold)
btnCall.addEventListener("click", call)
btnBet.addEventListener("click", bet)

function activerTourJoueur(nomJoueurTour) {
    if (nomJoueurTour === nomJoueur) {
        btnFold.disabled = false
        btnCall.disabled = false
        btnBet.disabled = false
    } else {
        btnFold.disabled = true
        btnCall.disabled = true
        btnBet.disabled = true
    }
}

function fold() {
    socket.emit(
        'joueur_se_couche',
        {
            table_id: tableId,
            nom_joueur: nomJoueur
        }
    )
}

function call() {
    socket.emit(
        'joueur_suit',
        {
            table_id: tableId,
            nom_joueur: nomJoueur
        }
    )
}

function bet() {
    socket.emit(
        'joueur_mise',
        {
            table_id: tableId,
            nom_joueur: nomJoueur
        }
    )
}

socket.on('connect', () => {
    console.log("Socket connectée !");
    socket.emit('join_table', {
        table_id: tableId,
        nom_joueur: nomJoueur
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
    console.log(`C'est à ${data.joueur_tour} de jouer`)

    activerTourJoueur(data.joueur_tour)
});

socket.on('joueur_est_couche', (data) => {
    console.log(`${data.nom_joueur} est couché.`);
    console.log(`C'est à ${data.joueur_tour} de jouer`)

    activerTourJoueur(data.joueur_tour)
});

socket.on('joueur_a_suivi', (data) => {
    console.log(`${data.nom_joueur} a suivi.`);
    console.log(`C'est à ${data.joueur_tour} de jouer`)

    activerTourJoueur(data.joueur_tour)
});

socket.on('joueur_a_mise', (data) => {
    console.log(`${data.nom_joueur} sur encheri.`);
    console.log(`C'est à ${data.joueur_tour} de jouer`)

    activerTourJoueur(data.joueur_tour)
});