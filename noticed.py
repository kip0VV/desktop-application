import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pathlib import Path
db_path = Path(__file__).resolve().parent / "noticed.db"


connection = sqlite3.connect(db_path)

connection.execute("""
CREATE TABLE IF NOT EXISTS ideas (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL
)
""")


app = QApplication([])
window = QWidget()

ideas = []

def click():
    text = idea_input.toPlainText()
    if text.strip() == "":  # Check if the text is empty
        idea_input.clear()
        return
    cursor = connection.execute(
        "INSERT INTO ideas (text) VALUES (?)",
        (text,)
    )
    new_id = cursor.lastrowid

    connection.commit()
    ideas.append((new_id, text))
    ideas_list.addItem(f"{len(ideas)}. {text}")
    idea_input.clear()
    print(ideas)

def delete_idea():
    if(ideas_list.currentRow() != -1):
        index = ideas_list.currentRow()
        idea_id = ideas[index][0]
        connection.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        connection.commit()
        ideas.pop(index)
        ideas_list.clear()
        for number, text in enumerate(ideas, start=1):
            ideas_list.addItem(f"{number}. {text[1]}")
        print(ideas)


layout = QVBoxLayout(window)

class IdeaInput(QPlainTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            click()
            return
        super().keyPressEvent(event)

idea_input = IdeaInput()
save_button = QPushButton("Save Idea")
delete_button = QPushButton("Delete Idea")
ideas_list = QListWidget()

result = connection.execute("SELECT id, text FROM ideas ORDER BY id")
rows = result.fetchall()
for row in rows:
    ideas.append(row)
    ideas_list.addItem(f"{len(ideas)}. {row[1]}")


window.setWindowTitle("Noticed")
layout.addWidget(idea_input)
layout.addWidget(save_button)
layout.addWidget(delete_button)
layout.addWidget(ideas_list)

save_button.clicked.connect(click)
delete_button.clicked.connect(delete_idea)

window.show()
app.exec()
connection.close()