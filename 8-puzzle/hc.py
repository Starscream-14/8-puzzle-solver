from var import GOAL_STATE
from collections import deque
from heapq import heappush, heappop
import time

# --- Heuristic Function ---
def heuristic(state):
    distance = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_row, goal_col = divmod(val - 1, 3)
        cur_row, cur_col = divmod(i, 3)
        distance += abs(goal_row - cur_row) + abs(goal_col - cur_col)
    return distance

# --- Neighbor Generation ---
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

# --- Hill Climbing with Unlimited Restarts ---
def hill_climbing(state, max_stuck=100):
    initial_state = state[:]
    current_state = state[:]
    visited_states = set()
    path = [current_state[:]]
    stuck_count = 0
    total_steps = 0
    all_attempts = 0
    while True:
        if current_state == GOAL_STATE:
            print("Hill climbing solved:", current_state)
            return path
        visited_states.add(tuple(current_state))
        neighbors = get_neighbors(current_state)
        neighbors.sort(key=lambda x: heuristic(x[0]))
        best_neighbor = neighbors[0][0]
        if heuristic(best_neighbor) >= heuristic(current_state):
            stuck_count += 1
            all_attempts += 1
            if stuck_count >= max_stuck:
                print(f"Hill climbing stuck after {stuck_count} restarts. Switching to BFS+A* hybrid.")
                return bfs_a_star(initial_state)
            print(f"Stuck! Restarting from initial state. Attempt {all_attempts}")
            current_state = initial_state[:]
            path = [current_state[:]]
            visited_states.clear()
            continue
        else:
            current_state = best_neighbor[:]
            path.append(current_state[:])
            stuck_count = 0
            total_steps += 1
            if total_steps % 50 == 0:
                print(f"Step {total_steps}: {current_state}")

# --- BFS + A* Hybrid ---
def bfs_a_star(initial_state):
    print("Starting BFS+A* hybrid search...")
    queue = deque()
    queue.append((initial_state[:], [initial_state[:]]))
    visited_states = set()
    best_path = None
    best_score = float('inf')
    start_time = time.time()
    while queue:
        current_state, path = queue.popleft()
        if tuple(current_state) in visited_states:
            continue
        visited_states.add(tuple(current_state))
        if current_state == GOAL_STATE:
            print("BFS+A* solved:", current_state)
            return path
        neighbors = get_neighbors(current_state)
        for neighbor, _ in neighbors:
            if tuple(neighbor) not in visited_states:
                new_path = path + [neighbor[:]]
                score = heuristic(neighbor) + len(new_path)
                if score < best_score:
                    best_score = score
                    best_path = new_path
                queue.append((neighbor[:], new_path))
        if len(visited_states) % 1000 == 0:
            print(f"Visited {len(visited_states)} states, best score: {best_score}")
        if time.time() - start_time > 30:
            print("Timeout reached, returning best found path.")
            return best_path if best_path else path
    print("BFS+A* failed, returning best found path.")
    return best_path if best_path else [initial_state[:]]

# --- Main Solve Function ---
def solve_puzzle(state, step_limit=100):
    print("Starting solve_puzzle...")
    path = []
    steps = 0
    for s in hill_climbing(state):
        path.append(s)
        steps += 1
        if steps >= step_limit:
            print(f"Step limit of {step_limit} reached. Puzzle may not be solved.")
            return path, False
        if s == GOAL_STATE:
            print("Puzzle solved!")
            return path, True
    print(f"Step limit of {step_limit} reached. Puzzle may not be solved.")
    return path, False