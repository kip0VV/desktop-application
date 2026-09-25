from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

app = QApplication([])
window = QWidget()

ideas = []

def click():
    text = idea_input.toPlainText()
    if text.strip() == "":  # Check if the text is empty
        idea_input.clear()
        return
    ideas_list.addItem(text)
    ideas.append(text)
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

window.setWindowTitle("Noticed")
layout.addWidget(idea_input)
layout.addWidget(save_button)
layout.addWidget(ideas_list)

save_button.clicked.connect(click)

window.show()
app.exec()