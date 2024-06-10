# six-degree-separation

### Autors:
- Mar Vega Garcia
- Alejandro Cantero López
- Eloi Busquets García-González
- Fanny Maria Aranda

### Execució del projecte
Per tal que el projecte funcioni correctament cal tenir les taules de la base de dades a un usuari coengut de PostgreSQL.
A més cal afegir un fitxer `.env` al root del projecte amb el següent continut, substituïnt l'usuari i contrassenya de la base de dades pels teus:
```
PROJECT_NAME=backend
BACKEND_CORS_ORIGINS=["*"]
EXT_ENDPOINT1=127.0.0.1
LOCAL_1=localhost
LOCAL_2=127.0.0.1
SECRET_KEY_DATABASE="PWD"
USER_DATABASE="USER"
```
#### Comandes per a executar el backend
És recomanable crear un virtual envoirment i activar-lo abans d'executar el backend. Per a això podem executar les comandes següents des del root del projecte:
```bash
cd backend
#Creem el virtual envoirment
python3 -m venv venv
#Activem el virtual envoirment
source venv/bin/activate
```
Per executar el backend des del root del projecte fem:
```bash
cd backend
make install
make run-app
```

#### Comandes per a executar el frontend
Per executar el frontend des del root del projecte fem:
```bash
cd frontend
npm i
npm run dev
```