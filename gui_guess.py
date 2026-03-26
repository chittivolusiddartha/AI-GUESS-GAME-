import tkinter as tk
from tkinter import messagebox

# Game variables
low = 1
high = 100
guess = 0
attempts = 0
player = ""
max_range = 100

# Leaderboard file
FILE = "leaderboard.txt"

# ------------------ GAME FUNCTIONS ------------------

def set_difficulty(value):
    global max_range
    max_range = value
    messagebox.showinfo("Difficulty", f"Range set to 1 - {value}")

def start_game():
    global player
    player = name_entry.get()

    if player == "":
        messagebox.showerror("Error", "Enter your name!")
        return

    start_frame.pack_forget()
    game_frame.pack()

    welcome_label.config(text=f"Welcome {player}! Think of number (1-{max_range})")

    reset_game()
    make_guess()
    load_leaderboard()

def reset_game():
    global low, high, attempts
    low = 1
    high = max_range
    attempts = 0

def make_guess():
    global guess, attempts

    if low > high:
        messagebox.showerror("Error", "Invalid input! Restarting...")
        restart_game()
        return

    guess = (low + high) // 2
    attempts += 1

    guess_label.config(text=f"My guess is: {guess}")
    attempt_label.config(text=f"Attempts: {attempts}")

def too_high():
    global high
    high = guess - 1
    make_guess()

def too_low():
    global low
    low = guess + 1
    make_guess()

def correct():
    messagebox.showinfo("Result", f"Guessed in {attempts} attempts!")
    save_score(player, attempts)
    load_leaderboard()

def restart_game():
    reset_game()
    make_guess()

# ------------------ LEADERBOARD ------------------

def save_score(name, score):
    data = []

    try:
        with open(FILE, "r") as f:
            for line in f:
                n, s = line.strip().split(",")
                data.append((n, int(s)))
    except:
        pass

    data.append((name, score))
    data.sort(key=lambda x: x[1])
    data = data[:5]

    with open(FILE, "w") as f:
        for n, s in data:
            f.write(f"{n},{s}\n")

def load_leaderboard():
    leaderboard_box.delete(0, tk.END)

    try:
        with open(FILE, "r") as f:
            for line in f:
                n, s = line.strip().split(",")
                leaderboard_box.insert(tk.END, f"{n} - {s} attempts")
    except:
        pass

# ------------------ UI ------------------

root = tk.Tk()
root.title("AI Number Guessing Game")
root.geometry("400x500")

# Start Frame
start_frame = tk.Frame(root)
start_frame.pack()

tk.Label(start_frame, text="🎮 AI Number Guessing Game", font=("Arial", 16)).pack(pady=10)

tk.Label(start_frame, text="Enter your name:").pack()
name_entry = tk.Entry(start_frame)
name_entry.pack(pady=5)

tk.Label(start_frame, text="Select Difficulty").pack()

tk.Button(start_frame, text="Easy (1-50)", command=lambda: set_difficulty(50)).pack(pady=2)
tk.Button(start_frame, text="Medium (1-100)", command=lambda: set_difficulty(100)).pack(pady=2)
tk.Button(start_frame, text="Hard (1-200)", command=lambda: set_difficulty(200)).pack(pady=2)

tk.Button(start_frame, text="Start Game", command=start_game).pack(pady=10)

# Game Frame
game_frame = tk.Frame(root)

welcome_label = tk.Label(game_frame, text="")
welcome_label.pack(pady=10)

guess_label = tk.Label(game_frame, text="", font=("Arial", 14))
guess_label.pack(pady=10)

attempt_label = tk.Label(game_frame, text="Attempts: 0")
attempt_label.pack()

tk.Button(game_frame, text="Too High", command=too_high, bg="red", fg="white").pack(pady=5)
tk.Button(game_frame, text="Too Low", command=too_low, bg="blue", fg="white").pack(pady=5)
tk.Button(game_frame, text="Correct", command=correct, bg="green", fg="white").pack(pady=5)

tk.Button(game_frame, text="Restart", command=restart_game).pack(pady=10)

# Leaderboard
tk.Label(game_frame, text="🏆 Leaderboard").pack()
leaderboard_box = tk.Listbox(game_frame)
leaderboard_box.pack(pady=5)

# Run app
root.mainloop()