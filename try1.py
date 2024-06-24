import os

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
    if direction == 'N':
        new_position = (x, y - 1)
    elif direction == 'E':
        new_position = (x + 1, y)
    elif direction == 'S':
        new_position = (x, y + 1)
    elif direction == 'W':
        new_position = (x - 1, y)
    else:
        raise ValueError("Invalid direction")

    if (0 <= new_position[1] < len(map_representation) and
        0 <= new_position[0] < len(map_representation[0]) and
        map_representation[new_position[1]][new_position[0]] != 'X'):
        return new_position
    return position

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

def find_start_position(map_representation):
    for y, row in enumerate(map_representation):
        for x, cell in enumerate(row):
            if cell == 'S':
                return (x, y)
    return None

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
        # Implement the logic to find a cleaning plan here
        # For now, we will create a dummy plan
        dummy_plan = "N"  # Replace this with actual plan finding logic
        with open(solution_file_path, 'w') as file:
            file.write(dummy_plan)
        print(f"Solution for FIND PLAN written to {solution_file_path}")

def automate_solutions(problem_directory, solution_directory):
    for file_name in os.listdir(problem_directory):
        if file_name.startswith('problem_') and file_name.endswith('.txt'):
            task_type, plan, map_representation = load_problem_file(os.path.join(problem_directory, file_name))
            solution_file_name = file_name.replace('problem_', 'solution_')
            solution_file_path = os.path.join(solution_directory, solution_file_name)
            generate_solution_file(task_type, plan, map_representation, solution_file_path)

if __name__ == "__main__":
    problem_directory = 'problems'
    solution_directory = 'example-solutions'
    automate_solutions(problem_directory, solution_directory)

