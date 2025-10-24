import json
import random
from hangman_art import stages, logo

# ---------- Default words & hints ----------
from word_list import word_list as default_words
from hints import hint as default_hints

# ---------- Upload / JSON load ----------
def load_uploaded_json():
    import os

    print("📂 Upload your files for the game.")
    word_list_path = input("Enter path to 'word_list.json' (or press Enter to use default): ").strip()
    hints_path = input("Enter path to 'hints.json' (or press Enter to use default): ").strip()

    if not word_list_path or not hints_path:
        print("Using default word list and hints.")
        return default_words, default_hints

    if not os.path.exists(word_list_path) or not os.path.exists(hints_path):
        print("One or both files not found. Using default lists.")
        return default_words, default_hints

    try:
        with open(word_list_path, "r", encoding="utf-8") as f:
            uploaded_words = json.load(f)
        with open(hints_path, "r", encoding="utf-8") as f:
            uploaded_hints = json.load(f)

        if not isinstance(uploaded_words, list) or not isinstance(uploaded_hints, list):
            print("Files are not valid lists. Using default lists.")
            return default_words, default_hints

        if len(uploaded_words) != len(uploaded_hints):
            print("⚠️ Word list and hints length mismatch! Using default lists.")
            return default_words, default_hints

        uploaded_words = [str(w) for w in uploaded_words]
        uploaded_hints = [str(h) for h in uploaded_hints]

        print(f"✅ Loaded {len(uploaded_words)} words and hints from uploaded files.")
        return uploaded_words, uploaded_hints

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error reading uploaded files: {e}. Using default lists.")
        return default_words, default_hints

# ---------- Game function ----------
def hangman_game():
    print(logo)
    word_list, hint_list = load_uploaded_json()
    play_again = True

    while play_again:
        rand_index = random.randint(0, len(word_list) - 1)
        chosen_word = word_list[rand_index].lower()
        chosen_hint = hint_list[rand_index]

        lives = 6
        correct_letters = set()
        guessed_letters = set()
        display = ["_"] * len(chosen_word)
        game_over = False

        while not game_over:
            print("\nWord to guess: " + " ".join(display))
            print(f"Lives left: {lives}")
            print("Hint:", chosen_hint)

            guess = input("Guess a letter: ").lower()
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter.")
                continue

            if guess in guessed_letters:
                print("You already guessed that letter!")
                continue

            guessed_letters.add(guess)

            if guess in chosen_word:
                correct_letters.add(guess)
                # Update display for all occurrences
                for i, letter in enumerate(chosen_word):
                    if letter == guess:
                        display[i] = guess
            else:
                lives -= 1
                print("Wrong guess!")

            # Check game over
            if lives == 0:
                game_over = True
                print("\n***********************YOU LOSE**********************")
                print(f"The word was: {chosen_word}")

            if "_" not in display:
                game_over = True
                print("\n****************************YOU WIN****************************")

            print(stages[lives])

        answer = input("\nDo you want to play again? (y/n): ").lower()
        if answer != "y":
            play_again = False

# ---------- Main ----------
if __name__ == "__main__":
    hangman_game()
