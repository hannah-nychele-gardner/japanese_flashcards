from tkinter import *
from tkinter import messagebox
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# --------- Data ---------
try:
    data = pd.read_csv("data/japanese_n2_words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/japanese_n2.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ------- Next Card -------


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    if len(to_learn) > 0:
        current_card = choice(to_learn)
        current_word = current_card["expression"]
        current_reading = current_card["reading"]
        canvas.itemconfig(card, image=card_front)
        canvas.itemconfig(title_text, text="Japanese", fill="black")
        canvas.itemconfig(word_text, text=current_word, fill="black")
        canvas.itemconfig(reading_text, text=current_reading, fill="black")
        flip_timer = window.after(3000, func=flip_card)
    else:
        messagebox.showinfo(title="Out of Cards", message="Congrats, you've learned all the cards!")

# ------- Flip Card -------


def flip_card():
    global current_card
    current_meaning = current_card["meaning"]
    current_word = current_card["expression"]
    current_reading = current_card["reading"]
    definition_list = current_meaning.split(",")  # gets only the first definition if there are multiple
    current_meaning = definition_list[0]
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_meaning, fill="white", font=("Arial", 30, "bold"))
    canvas.itemconfig(reading_text, fill="white", text=f"({current_word}, {current_reading})")

# ------ Remove Word ------


def remove_word():
    to_learn.remove(current_card)
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("data/japanese_n2_words_to_learn.csv", index=False)
    next_card()


# ---------- UI ----------

window = Tk()
window.title("Flashcards")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
flip_timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="Language", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
reading_text = canvas.create_text((400, 330), text="Reading", font=("Arial", 20, "italic"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, bd=0, command=next_card)
wrong_button.grid(row=1, column=0)
right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, bd=0, command=remove_word)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
