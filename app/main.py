from fastapi import FastAPI
from app.database import get_connection

app = FastAPI(title="Team Notes API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes")
def get_notes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, content, author, created_at
        FROM notes
        ORDER BY id
    """)

    notes = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "id": note[0],
            "title": note[1],
            "content": note[2],
            "author": note[3],
            "created_at": note[4]
        }
        for note in notes
    ]


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, content, author, created_at
        FROM notes
        WHERE id = %s
    """, (note_id,))

    note = cursor.fetchone()

    cursor.close()
    connection.close()

    if note is None:
        return {"detail": "Note not found"}

    return {
        "id": note[0],
        "title": note[1],
        "content": note[2],
        "author": note[3],
        "created_at": note[4]
    }