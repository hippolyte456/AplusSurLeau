"""
Moteur RAG minimal pour AplusSurLeau.
Cherche dans la base SQLite les données pertinentes à la question,
et retourne un contexte structuré prêt à être injecté dans le prompt système.
"""

import sqlite3
import re
from pathlib import Path
from django.conf import settings


TABLES = [
    "db_disciplines",
    "db_progression",
    "db_materiel",
    "db_spots",
    "db_regles_jointure",
    "questionnaire_m1",
    "questionnaire_m2",
    "questionnaire_m3",
    "regles_association",
]

# Colonnes textuelles principales par table (pour la recherche)
TEXT_COLUMNS = {
    "db_disciplines":     ["critere", "planche", "wing", "parawing", "kite"],
    "db_progression":     ["etape", "planche", "wing", "parawing", "kite"],
    "db_materiel":        ["parametre", "planche", "wing", "parawing", "kite"],
    "db_spots":           ["variable_spot", "impact_pour_le_novice", "niveau_minimal_requis", "disciplines_compatibles"],
    "db_regles_jointure": ["categorie", "condition_si", "action_alors"],
    "questionnaire_m1":   ["question_posee_au_novice", "options__echelle", "note_pour_le_llm"],
    "questionnaire_m2":   ["question_posee_au_novice", "options__echelle", "note_pour_le_llm"],
    "questionnaire_m3":   ["question_posee_au_novice", "options__echelle", "note_pour_le_llm"],
    "regles_association": ["categorie", "variable_novice", "action_pour_le_llm", "moment"],
}


def _get_connection() -> sqlite3.Connection:
    db_path = settings.APLUSURLEAU_DB
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _dump_table(cursor, table: str) -> str:
    """Retourne toute une table formatée en texte."""
    cursor.execute(f'SELECT * FROM "{table}"')
    rows = cursor.fetchall()
    if not rows:
        return ""
    headers = rows[0].keys()
    lines = [" | ".join(headers)]
    lines.append("-" * len(lines[0]))
    for row in rows:
        lines.append(" | ".join(str(v) if v else "" for v in row))
    return "\n".join(lines)


def _extract_keywords(question: str) -> list[str]:
    """Extrait des mots-clés simples depuis la question utilisateur."""
    stopwords = {"le", "la", "les", "un", "une", "des", "du", "de", "je", "tu",
                 "il", "elle", "nous", "vous", "et", "en", "à", "au", "est",
                 "que", "qui", "quoi", "comment", "quand", "où", "pour", "avec",
                 "sur", "par", "pas", "ne", "se", "me", "mon", "ma", "mes",
                 "quel", "quelle", "quels", "quelles", "dois", "peut", "veux"}
    words = re.findall(r"[a-záàâäéèêëîïôùûüç]{3,}", question.lower())
    return [w for w in words if w not in stopwords]


def _search_table(cursor, table: str, keywords: list[str]) -> list[sqlite3.Row]:
    """Cherche les lignes d'une table contenant au moins un des mots-clés."""
    cols = TEXT_COLUMNS.get(table, [])
    if not cols or not keywords:
        return []

    conditions = []
    params = []
    for col in cols:
        for kw in keywords:
            conditions.append(f'"{col}" LIKE ?')
            params.append(f"%{kw}%")

    query = f'SELECT * FROM "{table}" WHERE {" OR ".join(conditions)}'
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.OperationalError:
        return []


def _rows_to_text(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return ""
    headers = rows[0].keys()
    lines = []
    for row in rows:
        lines.append(" | ".join(str(v) if v else "" for v in row))
    return "\n".join(lines)


def build_context(question: str) -> str:
    """
    Point d'entrée principal.
    Retourne un bloc de contexte structuré à injecter dans le prompt système.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    keywords = _extract_keywords(question)

    sections = []

    # --- DB Experte : toujours injectée en entier (petite, statique) ---
    for table in ["db_disciplines", "db_progression", "db_materiel", "db_spots", "db_regles_jointure"]:
        content = _dump_table(cursor, table)
        if content:
            label = table.replace("db_", "").replace("_", " ").upper()
            sections.append(f"[DB EXPERTE — {label}]\n{content}")

    # --- Règles d'association : filtrées par mots-clés si possible, sinon tout ---
    ra_rows = _search_table(cursor, "regles_association", keywords)
    if not ra_rows:
        cursor.execute('SELECT * FROM "regles_association"')
        ra_rows = cursor.fetchall()
    if ra_rows:
        sections.append(f"[RÈGLES D'ASSOCIATION]\n{_rows_to_text(ra_rows)}")

    # --- Questionnaires : questions pertinentes selon les mots-clés ---
    for m, table in [("M1", "questionnaire_m1"), ("M2", "questionnaire_m2"), ("M3", "questionnaire_m3")]:
        rows = _search_table(cursor, table, keywords)
        if rows:
            sections.append(f"[QUESTIONNAIRE {m} — questions pertinentes]\n{_rows_to_text(rows)}")

    conn.close()
    return "\n\n".join(sections)
