import json
import os
import uuid
from datetime import datetime
import streamlit as st

NOTES_FILE = "data/notes.json"

st.title("Second Brain")

title = st.text_input("Title")
content = st.text_area("Note")


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_note(title, content):
    notes = load_notes()

    notes.append(
        {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "active",
        }
    )

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def archive_note(note_id):
    notes = load_notes()

    for note in notes:
        if note["id"] == note_id:
            note["status"] = "archived"

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def delete_note_permanently(note_id):
    notes = load_notes()

    notes = [
        note for note in notes
        if note["id"] != note_id
    ]

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

if st.button("Save"):
    save_note(title, content)
    st.success("Note saved")

st.divider()

st.header("My notes")

view_mode = st.radio(
    "View",
    ["Active notes", "Archived notes", "All notes"]
)

search = st.text_input("Search", placeholder="Search by title or content...")

notes = load_notes()

filtered_notes = [
    note for note in notes
    if search.lower() in note["title"].lower() or search.lower() in note["content"].lower()
] if search else notes

if view_mode == "Active notes":
    filtered_notes = [note for note in filtered_notes if note.get("status", "active") == "active"]
elif view_mode == "Archived notes":
    filtered_notes = [note for note in filtered_notes if note.get("status", "active") == "archived"]

for note in reversed(filtered_notes):
    st.subheader(note["title"])
    st.caption(note.get("created_at", "—"))
    st.write(note["content"])
    if note.get("status", "active") == "active":
        if st.button("Archive", key=f"archive_{note['id']}"):
            archive_note(note["id"])
            st.rerun()

    if st.button("Delete permanently", key=f"delete_{note['id']}"):
        delete_note_permanently(note["id"])
        st.rerun()