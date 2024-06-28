import os
from collections import deque

def load_problem_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    task_type = lines[0].strip()
    plan = ""
    map_start_idx = 1

    if task_type == "CHECK PLAN":
        plan = lines[1].strip()
        map_start_idx = 2
    
    map_representation = [line.strip() for line in lines[map_start_idx:]]
    
    return task_type, plan, map_representation

def move(position, direction, map_representation):
    x, y = position
    dx, dy = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}[direction]
    new_position = (x + dx, y + dy)

    if (0 <= new_position[1] < len(map_representation) and
        0 <= new_position[0] < len(map_representation[0]) and
        map_representation[new_position[1]][new_position[0]] != 'X'):
        return new_position
    return position

def find_start_position(map_representation):
    for y, row in enumerate(map_representation):
        for x, cell in enumerate(row):
            if cell == 'S':
                return (x, y)
    return None

def check_plan(plan, initial_position, map_representation):
    cleaned_squares = set()
    current_position = initial_position

    for direction in plan:
        current_position = move(current_position, direction, map_representation)
        cleaned_squares.add(current_position)
    
    all_cleaned = True
    missed_squares = []
    for y, row in enumerate(map_representation):
        for x, cell in enumerate(row):
            if cell == ' ' and (x, y) not in cleaned_squares:
                all_cleaned = False
                missed_squares.append((x, y))

    return all_cleaned, missed_squares

def bfs_find_cleaning_plan(map_representation, start_position):
    directions = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
    direction_keys = list(directions.keys())
    queue = deque([start_position])
    visited = set([start_position])
    parent = {start_position: None}
    path = []

    while queue:
        current = queue.popleft()
        for direction in direction_keys:
            next_position = move(current, direction, map_representation)
            if next_position not in visited and next_position != current:
                queue.append(next_position)
                visited.add(next_position)
                parent[next_position] = (current, direction)

    # Backtrack to find the path
    step = start_position
    while parent[step] is not None:
        path.append(parent[step][1])
        step = parent[step][0]
    path.reverse()

    return ''.join(path)

def find_cleaning_plan(map_representation):
    start_position = find_start_position(map_representation)
    if not start_position:
        return "No start found"

    return bfs_find_cleaning_plan(map_representation, start_position)

def generate_solution_file(task_type, plan, map_representation, solution_file_path):
    if task_type == "CHECK PLAN":
        initial_position = find_start_position(map_representation)
        if initial_position is None:
            print(f"No starting position found in the map for {solution_file_path}")
            return

        is_cleaned, missed_squares = check_plan(plan, initial_position, map_representation)

        if is_cleaned:
            result = "GOOD PLAN"
        else:
            result = "BAD PLAN\n" + "\n".join(f"{y}, {x}" for x, y in missed_squares)
        
        with open(solution_file_path, 'w') as file:
            file.write(result)
    elif task_type == "FIND PLAN":
        cleaning_plan = find_cleaning_plan(map_representation)
        with open(solution_file_path, 'w') as file:
            file.write(cleaning_plan)
        print(f"Solution for FIND PLAN written to {solution_file_path}")

def automate_solutions(problem_directory, solution_directory):
    for file_name in os.listdir(problem_directory):
        if file_name.startswith('problem_') and file_name.endswith('.txt'):
            task_type, plan, map_representation = load_problem_file(os.path.join(problem_directory, file_name))
            solution_file_name = file_name.replace('problem_', 'solution_')
            solution_file_path = os.path.join(solution_directory, solution_file_name)
            generate_solution_file(task_type, plan, map_representation, solution_file_path)
            
            
def find_start_position(map_representation):
    for y, row in enumerate(map_representation):
        print(f"Row {y}: {row}")  # Debug print to show map rows
        for x, cell in enumerate(row):
            if cell == 'S':
                print(f"Found start at ({x}, {y})")  # Confirm start position found
                return (x, y)
    print("No start found in the current map.")  # Indicate no start found
    return None


if __name__ == "__main__":
    problem_directory = 'problems'
    solution_directory = 'example-solutions'
    automate_solutions(problem_directory, solution_directory)

