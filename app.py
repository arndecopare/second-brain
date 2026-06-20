import json
import os
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
            "title": title,
            "content": content,
        }
    )

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


if st.button("Save"):
    save_note(title, content)
    st.success("Note saved")

st.divider()

st.header("My notes")

notes = load_notes()

for note in reversed(notes):
    st.subheader(note["title"])
    st.write(note["content"])