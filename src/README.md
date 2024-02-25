# Campus Routing

## **API**

Path: src/api/.

### **Endpoints**:

- **GET** /api/available_buildings (Pour obtenir la liste des batiments que le graphe contient)
- **POST** /api/ask (Pour demander un chemin entre deux locaux)

### **Comment l'utiliser**:

- Commande pour lancer le serveur: `uvicorn  --app-dir ./src/ main:app --reload` à partir du répertoire racine
- Dans les fichiers webapp/ask_path.\* , on retrouve comment requêter le serveur pour obtenir un chemin entre deux locaux.
