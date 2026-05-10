## Feuille de route technique

### 1 - Conversion des données (XLSX → JSON / SQLite)

Script de conversion des bases de données questionnaires et règles d'association vers un format exploitable par le RAG :

- `1_DB_Experte.xlsx` + `1_Questionnaires.xlsx` + `3_Regles_Association.xlsx` → JSON ou base SQLite

> ❓ **A préciser** : JSON (simple, portable) ou SQLite (mieux pour les requêtes complexes et l'intégration Django) ?

### 2 - Moteur RAG intégrable à Django

Outil simple pour le RAG, compatible Django :

| Outil                | Type             | Points forts                                                  |
| -------------------- | ---------------- | ------------------------------------------------------------- |
| **LlamaIndex** | Framework        | Excellent pour bases documentaires, plus simple que LangChain |
| **LangChain**  | Framework        | Le plus connu, très complet                                  |
| **DSPy**       | Framework        | Approche "compiler ton prompt", plus récent                  |
| **Chroma**     | Base vectorielle | Simple, open source, parfait pour débuter                    |
| **Pinecone**   | Base vectorielle | Managé, très utilisé en prod                               |
| **Weaviate**   | Base vectorielle | Données structurées + sémantiques                          |
| **Flowise**    | No-code          | Interface drag & drop pour pipelines RAG                      |
| **Langflow**   | No-code          | Similaire à Flowise                                          |

> ❓ **A préciser** : Quelle stack choisir selon les contraintes (hébergement, budget, compétences) ?

### 3 - Application Django minimale (chatbot)

Interface web minimaliste avec :

- Formulaire de questionnaire (M1 → M2 → M3)
- Chatbot qui répond via le RAG
- Historique de session utilisateur

---

## 4- Diffuser

- → Publier une mini-version sur wing4all
- → Envoyer à cdv35 + Erwan Geoffroy
