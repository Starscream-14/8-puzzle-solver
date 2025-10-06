import tkinter as tk
from gui import style_button, show_rules, start_game

def main_menu():
    root = tk.Tk()
    root.title("8-Puzzle Main Menu")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    title = tk.Label(root, text="8-Puzzle Game", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="black")
    title.pack(pady=30)
    
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)
    
    play_btn = tk.Button(button_frame, text="Play", command=lambda: start_game(root))
    style_button(play_btn, "#27ae60", "#1e8449")  # Green
    play_btn.pack(side="left", padx=10)

    rules_btn = tk.Button(button_frame, text="Rules", command=show_rules)
    style_button(rules_btn, "#f39c12", "#d68910")  # Orange
    rules_btn.pack(side="left", padx=10)

    exit_btn = tk.Button(button_frame, text="Exit", command=root.destroy)
    style_button(exit_btn, "#e74c3c", "#c0392b")  # Red
    exit_btn.pack(side="left", padx=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()