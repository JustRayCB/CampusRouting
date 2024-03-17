// Définir l'état initial
let state = {
    path: null,
    images: null,
    arrival_building: true,
    first_images: null
};

// Liste des observateurs
const observers = [];

// Fonction pour mettre à jour l'état
const updateState = (newState) => {
    state = { ...state, ...newState };
    notifyObservers();
};

// Fonction pour ajouter un observateur
const addObserver = (observer) => {
    observers.push(observer);
};

// Fonction pour notifier tous les observateurs
const notifyObservers = () => {
    observers.forEach(observer => observer());
};

// Fonction pour récupérer l'état actuel
const getState = () => {
    return state;
};

// Exporter les fonctions pour les rendre disponibles
export { updateState, addObserver, getState };
