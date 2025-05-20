const socket = io();
const tableId = document.getElementById("table-id").textContent;
const nomJoueur = document.getElementById("nom-joueur").textContent;
const nbJoueursConnectes = document.getElementById("joueurs-connectes");
const salleAttente = document.getElementById("salle-attente");
const jeuLance = document.getElementById("jeu-lance");
const pot = document.getElementById("pot");
const cartesCommunes = document.getElementById("cartes-communes");
const joueurs = document.getElementById("joueurs");
const btnFold = document.getElementById("btn-fold");
const btnCall = document.getElementById("btn-call");
const btnBet = document.getElementById("btn-bet");

btnFold.addEventListener("click", fold);
btnCall.addEventListener("click", call);
btnBet.addEventListener("click", bet);

function activerTourJoueur(nomJoueurTour) {
    if (nomJoueurTour === nomJoueur) {
        btnFold.disabled = false;
        btnCall.disabled = false;
        btnBet.disabled = false;
    } else {
        btnFold.disabled = true;
        btnCall.disabled = true;
        btnBet.disabled = true;
    }
}

function fold() {
    socket.emit(
        'joueur_parle',
        {
            table_id: tableId,
            nom_joueur: nomJoueur,
            action:"se_couche"
        }
    )
}

function call() {
    socket.emit(
        'joueur_parle',
        {
            table_id: tableId,
            nom_joueur: nomJoueur,
            action:"suit"
        }
    )
}

function bet() {
    socket.emit(
        'joueur_parle',
        {
            table_id: tableId,
            nom_joueur: nomJoueur,
            action:"relance"
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
    nbJoueursConnectes.textContent = `${data.nombre_joueurs}`;
});

socket.on('lancement_partie', () => {
    console.log(`La partie est lancée`);
    salleAttente.classList.add("hidden")
    jeuLance.classList.remove("hidden");
});

socket.on("debut_tour", (data) => {
    console.log("Début du tour")
    pot.textContent = data.pot;
    cartesCommunes.innerHTML = ""
    joueurs.innerHTML = ""
    for (let [nomJoueur, jetonsJoueurs] of Object.entries(data.joueurs)) {
        joueurs.innerHTML +=
            `<div id=${nomJoueur}>
                <h2>${nomJoueur}</h2>
                <p id="jetons-${nomJoueur}">Jetons : ${jetonsJoueurs}</p>
                <p id="cartes-${nomJoueur}"></p>
            </div>`;
    }

    console.log(`C'est à ${data.joueur_tour} de jouer`);

    activerTourJoueur(data.joueur_tour);
})

socket.on('reception_cartes', (data) => {
    document.getElementById("cartes-"+nomJoueur).innerHTML =
        `<img src="../static/images/cartes/${data.carte1}.png" alt="${data.carte1}" class="carte-jeu"/>
         <img src="../static/images/cartes/${data.carte2}.png" alt="${data.carte2}" class="carte-jeu"/>`;
});

socket.on("nouvelle_phase_jeu", (data) => {
    console.log("Nouvelle phase de jeu : " + data.phase_jeu);

    const cartesStr = data.cartes_communes || "";

    cartesCommunes.innerHTML = ""
    cartesStr.replace(/;$/, "").split(";").forEach(carte => {
        const img = document.createElement("img");
        img.src = `../static/images/cartes/${carte}.png`;
        img.alt = carte;
        img.classList.add("carte-jeu"); // utile pour appliquer un style CSS
        cartesCommunes.appendChild(img);
    });
});

socket.on("fin_tour", (data)=>{
    console.log("Le ou les gagnants sont : " + data.nom_gagnant)
    activerTourJoueur("") // On active le tour pour aucun joueur (on bloque les actions)
})

socket.on('joueur_est_couche', (data) => {
    console.log(`${data.nom_joueur} est couché.`);
    console.log(`C'est à ${data.joueur_tour} de jouer`);

    activerTourJoueur(data.joueur_tour);
});

socket.on('joueur_a_suivi', (data) => {
    console.log(`${data.nom_joueur} a suivi.`);
    console.log(`C'est à ${data.joueur_tour} de jouer`);

    activerTourJoueur(data.joueur_tour);
});

socket.on('joueur_a_mise', (data) => {
    console.log(`${data.nom_joueur} sur encheri.`);
    console.log(`C'est à ${data.joueur_tour} de jouer`);

    activerTourJoueur(data.joueur_tour);
});