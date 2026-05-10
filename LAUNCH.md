# Comment lancer l'application en local

## 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 2. Définir ta clé API Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 3. Générer la base SQLite (une seule fois, ou après modif des XLSX)

```bash
python convert_to_sqlite.py
```

## 4. Lancer le serveur Django

```bash
cd chatbot
python manage.py runserver
```

Ouvre ensuite http://localhost:8000 dans ton navigateur.


pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
python convert_to_sqlite.py   # déjà fait
cd chatbot && python manage.py runserver
