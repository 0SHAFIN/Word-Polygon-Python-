import tkinter as tk
import random

# Small internal dictionary (for offline use)
WORD_LIST = [
    "stone", "tones", "notes", "ten", "net", "set", "one", "note", "tone", "sent", "nest", "toe", "son", "not", "ons"
]

# Helper to check if a word is valid
def is_valid_word(word, letters, required_letter):
    if len(word) < 3:
        return False
    if required_letter not in word:
        return False
    temp_letters = list(letters)
    for ch in word:
        if ch not in temp_letters:
            return False
        temp_letters.remove(ch)
    return word in WORD_LIST

class WordPolygonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Polygon Game")

        self.letters = random.sample("abcdefghijklmnopqrstuvwxyz", random.randint(5, 9))
        self.required_letter = random.choice(self.letters)
        self.found_words = []
        self.score = 0

        # Letter display
        self.letters_label = tk.Label(root, text="Letters: " + " ".join(self.letters), font=("Arial", 14))
        self.letters_label.pack(pady=10)

        self.required_label = tk.Label(root, text=f"Required letter: {self.required_letter}", font=("Arial", 12), fg="blue")
        self.required_label.pack(pady=5)

        # Word entry
        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.submit_btn = tk.Button(root, text="Submit Word", command=self.submit_word)
        self.submit_btn.pack(pady=5)

        # Display valid words
        self.output = tk.Text(root, height=10, width=40, font=("Arial", 10))
        self.output.pack(pady=10)

        self.status = tk.Label(root, text="Score: 0", font=("Arial", 12))
        self.status.pack(pady=5)

        self.new_game_btn = tk.Button(root, text="New Game", command=self.reset_game)
        self.new_game_btn.pack(pady=5)

    def submit_word(self):
        word = self.entry.get().lower()
        if word in self.found_words:
            self.output.insert(tk.END, f"'{word}' already used!\n")
        elif is_valid_word(word, self.letters[:], self.required_letter):
            self.found_words.append(word)
            self.score += len(word)
            self.output.insert(tk.END, f"✅ {word}\n")
        else:
            self.output.insert(tk.END, f"❌ Invalid word: {word}\n")
        self.entry.delete(0, tk.END)
        self.status.config(text=f"Score: {self.score}")

    def reset_game(self):
        self.letters = random.sample("abcdefghijklmnopqrstuvwxyz", random.randint(5, 9))
        self.required_letter = random.choice(self.letters)
        self.found_words.clear()
        self.score = 0
        self.letters_label.config(text="Letters: " + " ".join(self.letters))
        self.required_label.config(text=f"Required letter: {self.required_letter}")
        self.output.delete('1.0', tk.END)
        self.status.config(text="Score: 0")
        self.entry.delete(0, tk.END)

# Run the app
root = tk.Tk()
game = WordPolygonGame(root)
root.mainloop()
