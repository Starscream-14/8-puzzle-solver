import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter.messagebox

import var

def style_button(btn, normal_bg="#4a90e2", hover_bg="#357ABD", fg="white"):
    btn.config(
        relief="flat",
        bg=normal_bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground=fg,
        font=("Arial", 14, "bold"),
        bd=0,
        padx=14,
        pady=8,
        cursor="hand2",
    )
    def on_enter(e):
        btn.config(bg=hover_bg)
    def on_leave(e):
        btn.config(bg=normal_bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def show_rules():
    rules = (
        "8-Puzzle Game Rules:\n\n"
        "1. The puzzle consists of 8 tiles and one empty space arranged in a 3x3 grid.\n"
        "2. Tiles can be moved into the empty space if they are adjacent (up, down, left, right).\n"
        "3. The goal is to arrange the tiles in order from 1 to 8, with the empty space at the end.\n"
        "4. Click a tile next to the empty space to move it.\n"
        "5. Try to solve the puzzle in as few moves as possible!"
    )
    tk.messagebox.showinfo("Rules", rules)

def heuristic(state):
    distance = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_row, goal_col = divmod(val - 1, 3)
        cur_row, cur_col = divmod(i, 3)
        distance += abs(goal_row - cur_row) + abs(goal_col - cur_col)
    return distance

def get_neighbors(state):
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)
    moves = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        r, c = row+dr, col+dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_idx = r*3+c
            new_state = state.copy()
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            moves.append((new_state, new_state[zero_idx]))
    return moves

def is_adjacent(idx1, idx2):
    row1, col1 = divmod(idx1, 3)
    row2, col2 = divmod(idx2, 3)
    return abs(row1 - row2) + abs(col1 - col2) == 1

class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle Game")
        master.configure(bg="#f0f0f0")

        # Use var.CUSTOM_STATE as starting state
        self.start_tiles = var.CUSTOM_STATE.copy()
        self.tiles = self.start_tiles.copy()
        self.buttons = []
        self.example_index = 0  # for cycling through PUZZLE_EXAMPLES

        img_path = os.path.join(os.path.dirname(__file__), "puzzle.jpg")
        puzzle_size = 540
        tile_size = puzzle_size // 3
        self.images = {}

        if os.path.exists(img_path):
            original = Image.open(img_path)
            original = original.resize((puzzle_size, puzzle_size), Image.LANCZOS)
        else:
            original = Image.new("RGB", (puzzle_size, puzzle_size), color="gray")

        try:
            font = ImageFont.truetype("DejaVuSans.ttf", tile_size // 4)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", tile_size // 4)
            except:
                font = ImageFont.load_default()

        for i in range(3):
            for j in range(3):
                idx = i * 3 + j + 1
                if idx <= 8:
                    left = j * tile_size
                    upper = i * tile_size
                    right = left + tile_size
                    lower = upper + tile_size
                    tile_img = original.crop((left, upper, right, lower)).convert("RGBA")
                    draw = ImageDraw.Draw(tile_img)
                    text = str(idx)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (tile_size - text_width) // 2
                    y = (tile_size - text_height) // 2
                    draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))
                    self.images[idx] = ImageTk.PhotoImage(tile_img)
        empty_img = Image.new("RGB", (tile_size, tile_size), color="white")
        self.images[0] = ImageTk.PhotoImage(empty_img)

        # Puzzle frame
        self.frame = tk.Frame(master, bg="#f0f0f0")
        self.frame.pack(pady=20)

        for i in range(3):
            row = []
            for j in range(3):
                idx = i * 3 + j
                btn = tk.Button(
                    self.frame,
                    image=self.images[self.tiles[idx]],
                    width=tile_size, height=tile_size,
                    command=lambda idx=idx: self.move_tile(idx),
                    relief="flat", bd=0, highlightthickness=0
                )
                btn.grid(row=i, column=j, padx=0, pady=0)
                row.append(btn)
            self.buttons.append(row)

        controls = tk.Frame(master, bg="#f0f0f0")
        controls.pack(pady=10)

        restart_btn = tk.Button(controls, text="Restart", command=self.restart)
        style_button(restart_btn, "#27ae60", "#1e8449")  # Green
        restart_btn.grid(row=0, column=0, padx=10)

        step_btn = tk.Button(controls, text="Solve Step", command=self.solve_step)
        style_button(step_btn, "#f39c12", "#d68910")  # Orange
        step_btn.grid(row=0, column=1, padx=10)

        auto_btn = tk.Button(controls, text="Auto Solve (Hill Climbing)", command=self.auto_solve)
        style_button(auto_btn, "#8e44ad", "#6c3483")  # Purple
        auto_btn.grid(row=0, column=2, padx=10)

        random_btn = tk.Button(controls, text="Random", command=self.next_puzzle)
        style_button(random_btn, "#3498db", "#2980b9")  # Blue
        random_btn.grid(row=0, column=3, padx=10)

        self.log = tk.Text(master, height=10, width=65, state="disabled", wrap="word", bg="#ffffff", fg="black")
        self.log.pack(pady=10)

        self.auto_solving = False

    def log_message(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def check_solved(self):
        if self.tiles == var.GOAL_STATE:
            tk.messagebox.showinfo("Congratulations!", "You managed to solve the puzzle!")

    def move_tile(self, idx):
        zero_idx = self.tiles.index(0)
        if is_adjacent(idx, zero_idx):
            self.tiles[zero_idx], self.tiles[idx] = self.tiles[idx], self.tiles[zero_idx]
            self.update_buttons()
            self.check_solved()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                val = self.tiles[idx]
                self.buttons[i][j].config(image=self.images[val])

    def restart(self):
        self.tiles = self.start_tiles.copy()
        self.update_buttons()
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def solve_step(self):
        current_h = heuristic(self.tiles)
        self.log_message(f"Current heuristic: {current_h}")
        neighbors = get_neighbors(self.tiles)
        evaluated = []
        for state, moved in neighbors:
            h = heuristic(state)
            evaluated.append((h, state, moved))
            self.log_message(f"Move tile {moved} → heuristic {h}")
        best = min(evaluated, key=lambda x: x[0])
        if best[0] < current_h:
            self.tiles = best[1]
            self.update_buttons()
            self.log_message(f"Chose move {best[2]}, heuristic improved to {best[0]}")
            self.check_solved()
        else:
            self.log_message("No better neighbor found (stuck).")


    def auto_solve(self):
        import hc
        if self.auto_solving:
            self.auto_solving = False
            return
        self.auto_solving = True
        self.log_message("Auto-solving using auto solver...")
        solution_path, solved = hc.solve_puzzle(self.tiles, step_limit=100)
        self._show_solution_path(solution_path, solved)

    def _show_solution_path(self, path, solved):
        if not self.auto_solving or not path:
            self.auto_solving = False
            return
        def step(idx):
            if not self.auto_solving or idx >= len(path):
                self.auto_solving = False
                if solved:
                    self.log_message("Puzzle solved!")
                    tk.messagebox.showinfo("Congratulations!", "Puzzle solved!")
                else:
                    self.log_message("Step limit reached. Puzzle may not be solved.")
                    tk.messagebox.showwarning("Limit reached", "Step limit reached. Puzzle may not be solved.")
                return
            self.tiles = path[idx]
            self.update_buttons()
            self.log_message(f"Step {idx}: {self.tiles}")
            self.master.after(500, lambda: step(idx+1))
        step(0)

    def next_puzzle(self):
        # increment index and wrap around
        self.example_index = (self.example_index + 1) % len(var.PUZZLE_EXAMPLES)
        new_state = var.PUZZLE_EXAMPLES[self.example_index]
        # persist the change to var.CUSTOM_STATE for future restarts
        var.CUSTOM_STATE[:] = new_state
        self.start_tiles = new_state.copy()
        self.tiles = new_state.copy()
        self.update_buttons()
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
        self.log_message(f"Puzzle changed to example #{self.example_index + 1}.")

def start_game(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#f0f0f0")
    root.geometry("750x750")
    EightPuzzleGUI(root)