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
    connection.execute(
        "INSERT INTO ideas (text) VALUES (?)",
        (text,)
    )
    connection.commit()
    ideas.append(text)
    ideas_list.addItem(f"{len(ideas)}. {text}")
    idea_input.clear()
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
ideas_list = QListWidget()

result = connection.execute("SELECT id, text FROM ideas ORDER BY id")
rows = result.fetchall()
for row in rows:
    ideas.append(row[1])
    ideas_list.addItem(f"{len(ideas)}. {row[1]}")


window.setWindowTitle("Noticed")
layout.addWidget(idea_input)
layout.addWidget(save_button)
layout.addWidget(ideas_list)

save_button.clicked.connect(click)

window.show()
app.exec()
connection.close()