const socket = io();

const tableId = document.getElementById("table-id");
const nomJoueur = document.getElementById("nom-joueur");
const nbJoueursConnectes = document.getElementById("joueurs-connectes");

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