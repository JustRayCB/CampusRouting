# Campus Routing

## **API**

Path: src/main.py

### **Endpoints**:

- **GET** /api/available_buildings (Pour obtenir la liste des batiments que le graphe contient)
- **POST** /api/ask_inside (Pour demander un chemin entre deux locaux ou zone intérieure d'un même bâtiment)
- **POST** /api/ask_outside (Pour demander un chemin entre un local et un point extérieur au graphe)

### **Comment l'utiliser**:

- Commande pour lancer le serveur: `uvicorn  --app-dir ./src/ main:app --reload` à partir du répertoire racine
  You can also use the commande `Make run` to run the server
- Dans les fichiers webapp/ask_path.\* , on retrouve comment requêter le serveur pour obtenir un chemin entre deux locaux.
