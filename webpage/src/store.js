import { createStore } from 'redux';

// Définir l'état initial
const initialState = {
    path: null,
    images: null,
    arrival_building: true,
    first_images: null
};

// Définir un reducer pour gérer les actions
const reducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_DATA':
            return {
                ...state,
                path: action.payload.path,
                images: action.payload.images,
                arrival_building: action.payload.arrival_building,
                first_images: action.payload.first_images
            };
        default:
            return state;
    }
};

// Créer le store Redux avec le reducer
const store = createStore(reducer);

export default store;
