import tkinter as tk
import random

# A basic embedded word list
WORD_LIST = {
    "stone", "tones", "notes", "ten", "net", "set", "one", "note", "tone", "sent", "nest",
    "toe", "son", "not", "ons", "ton", "eon", "neo", "no", "on", "so"
}

class WordPolygonGame:
    def __init__(self, master):
        self.master = master
        master.title("Word Polygon Game")
        master.geometry("460x570")
        self.reset_game_data()

        # Letter display
        self.letter_frame = tk.Frame(master)
        self.letter_frame.pack(pady=10)
        self.letter_labels = []
        for i in range(9):
            lbl = tk.Label(self.letter_frame, text="", width=2, font=("Helvetica", 18), relief="ridge", padx=6, pady=4)
            lbl.grid(row=0, column=i, padx=2)
            self.letter_labels.append(lbl)

        self.required_label = tk.Label(master, text="", font=("Helvetica", 12, "bold"), fg="blue")
        self.required_label.pack()

        # Word input
        self.word_entry = tk.Entry(master, font=("Helvetica", 14))
        self.word_entry.pack(pady=5)
        self.word_entry.bind("<Return>", lambda e: self.submit_word())

        self.submit_btn = tk.Button(master, text="Submit Word", command=self.submit_word)
        self.submit_btn.pack(pady=5)

        # Show answers button
        self.answer_btn = tk.Button(master, text="Show Answers", command=self.show_answers)
        self.answer_btn.pack(pady=5)

        # Output display
        self.output_text = tk.Text(master, height=12, width=45, font=("Helvetica", 11))
        self.output_text.pack(pady=5)

        # Score display
        self.score_label = tk.Label(master, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack()

        self.rank_label = tk.Label(master, text="", font=("Helvetica", 10, "italic"))
        self.rank_label.pack()

        self.reset_btn = tk.Button(master, text="New Game", command=self.reset_game)
        self.reset_btn.pack(pady=10)

        self.new_game_ui()

    def reset_game_data(self):
        self.letters = []
        self.required_letter = ''
        self.valid_words = []
        self.found_words = set()
        self.score = 0

    def new_game_ui(self):
        self.reset_game_data()
        self.letters = random.sample("abcdefghijklmnopqrstuvwxyz", random.randint(7, 9))
        self.required_letter = random.choice(self.letters)

        self.valid_words = [word for word in WORD_LIST
                            if len(word) >= 3 and self.required_letter in word
                            and all(word.count(c) <= self.letters.count(c) for c in word)]

        for i, lbl in enumerate(self.letter_labels):
            if i < len(self.letters):
                char = self.letters[i]
                lbl.config(text=char.upper(), fg="blue" if char == self.required_letter else "black")
            else:
                lbl.config(text="")

        self.required_label.config(text=f"Required Letter: {self.required_letter.upper()}")
        self.output_text.delete("1.0", tk.END)
        self.score_label.config(text="Score: 0")
        self.rank_label.config(text="")
        self.word_entry.delete(0, tk.END)

    def submit_word(self):
        word = self.word_entry.get().lower().strip()
        if not word:
            self.log("⚠️ Please type a word first.")
            return

        self.word_entry.delete(0, tk.END)

        if len(word) < 3:
            self.log(f"❌ '{word}': Too short.")
            return
        if self.required_letter not in word:
            self.log(f"❌ '{word}': Missing required letter.")
            return
        if word in self.found_words:
            self.log(f"⚠️ '{word}': Already found.")
            return
        if not all(word.count(c) <= self.letters.count(c) for c in word):
            self.log(f"❌ '{word}': Invalid letter use.")
            return
        if word not in WORD_LIST:
            self.log(f"❌ '{word}': Not a valid word.")
            return

        # Word accepted
        self.found_words.add(word)
        self.score += len(word)
        self.log(f"✅ '{word}' accepted!")
        self.score_label.config(text=f"Score: {self.score}")
        self.update_rank()

    def log(self, msg):
        self.output_text.insert(tk.END, msg + "\n")
        self.output_text.see(tk.END)

    def update_rank(self):
        word_count = len(self.found_words)
        if word_count < 4:
            rank = "Keep going!"
        elif word_count < 8:
            rank = "👍 Good"
        elif word_count < 12:
            rank = "🌟 Very Good"
        else:
            rank = "🏆 Excellent!"
        self.rank_label.config(text=f"Progress: {rank}")

    def reset_game(self):
        self.new_game_ui()

    def show_answers(self):
        self.output_text.insert(tk.END, "\n--- All Valid Words ---\n")
        for word in sorted(self.valid_words):
            self.output_text.insert(tk.END, word + "\n")
        self.output_text.insert(tk.END, "------------------------\n")
        self.output_text.see(tk.END)


# Run the game
root = tk.Tk()
game = WordPolygonGame(root)
root.mainloop()
