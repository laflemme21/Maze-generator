import random as random
import sys as sys


def step_one_maze_gen(x, y, directions):
    maze = []
    for i in range(0, y):
        maze.append([])
        for j in range(0, x):
            maze[i].append('#')

    Sx = random.randint(0, x-1)
    Sy = random.randint(0, y-1)

    if Sx <= len(maze[0])//2:
        Ex = random.randint(len(maze[0])-len(maze[0])//4, x-1)
    else:
        Ex = random.randint(0, len(maze[0])//4)

    if Sy <= len(maze)//2:
        Ey = random.randint(len(maze)-len(maze)//4, y-1)
    else:
        Ey = random.randint(0, len(maze)//4)

    Py = Sy
    Px = Sx
    maze[Py][Px] = ' '

    while Py != Ey or Px != Ex:
        direction = random.choice(directions)
        new_Px, new_Py = move(Px, Py, direction)
        if valid_move(maze, new_Px, new_Py, False):
            Px, Py = new_Px, new_Py
        maze[Py][Px] = ' '

    return maze, Sx, Sy, Ex, Ey


def valid_move(maze, x, y, check_for_space):
    if (0 <= y < len(maze)) and (0 <= x < len(maze[0])):
        if check_for_space and maze[y][x] == '#':
            return False
        return True
    return False


def is_solvable(maze, x, y, Ex, Ey, is_solution_outputted, previous_solution):
    path = []
    invalid_path = []
    possible_moves = []
    for i in previous_solution:
        if maze[i[0]][i[1]] == '#':
            break
        else:
            path.append(i)
            possible_moves.append(get_possible_moves(maze, path, i[1], i[0]))
    # assigns the starting position

    next_move = ''
    # loops while maze is not solved
    y, x = path[-1][0], path[-1][1]
    while path[-1][1] != Ex or path[-1][0] != Ey:
        # if all the direction possible of the position of the player were taken, go to the previous position
        if possible_moves[-1] == []:

            maze[path[-1][0]][path[-1][1]] = ' '

            invalid_path.append(path[-1])

            possible_moves.pop(-1)
            path.pop(-1)

            # if all possible paths were taken then unsolvable
            if path == []:
                return [], False
            y, x = path[-1][0], path[-1][1]
        else:
            # move and mark it as taken
            next_move = possible_moves[-1][0]
            possible_moves[-1].pop(0)

        if next_move != '':
            new_Px, new_Py = move(x, y, next_move)
            if [new_Py, new_Px] in path:
                # go back
                while path[-1] != [new_Py, new_Px]:

                    maze[path[-1][0]][path[-1][1]] = ' '

                    path.pop(-1)
                    possible_moves.pop(-1)
                y, x = path[-1][0], path[-1][1]

            elif valid_move(maze, new_Px, new_Py, True) and [new_Py, new_Px] not in invalid_path:
                # assign coordinates to new
                x, y = new_Px, new_Py
                # move the player
                path.append([y, x])
                if [y, x] != [Ey, Ey] and is_solution_outputted:
                    maze[path[-1][0]][path[-1][1]] = '@'
                # add all possibles moves
                possible_moves.append(get_possible_moves(maze, path, x, y))

            next_move = ''

    return path, True


def get_possible_moves(maze, path, x, y):
    possible_moves = []
    for i in ['W', 'A', 'S', 'D']:
        new_Px, new_Py = move(x, y, i)
        if valid_move(maze, new_Px, new_Py, True) and [new_Py, new_Px] not in path:
            possible_moves.append(i)
    return possible_moves


def move(x, y, direction):

    if direction == 'W':
        y = y - 1

    elif direction == 'A':
        x = x - 1

    elif direction == 'S':
        y = y+1

    elif direction == 'D':
        x = x+1

    return x, y


def save_in_file(maze, file, param):
    f = open(file, param)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            f.write(maze[i][j])
        f.write('\n')

    f.close()


def step_two_maze_gen(maze, Sx, Sy, Ex, Ey):
    path_ = [[Sy, Sx]]
    for pattern, pattern_opp, pattern_amount in [' ', '#', 4], ['#', ' ', 2]:
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if check_adj(maze, j, i, pattern) <= pattern_amount:
                    # random position
                    x, y = random_adj(
                        j, i, len(maze[i]), len(maze), Sx, Sy)
                    # assign it to the pattern populating
                    maze[y][x] = pattern
                    # store the solution if true
                    new_path, boolean = is_solvable(
                        maze, Sx, Sy, Ex, Ey, False, path_)
                    if not boolean:
                        maze[y][x] = pattern_opp
                    else:
                        path_ = new_path

    return maze


def check_adj(maze, x, y, pattern):
    sum = 0
    for i in range(-1, 2):
        if 0 <= y+i < len(maze):
            for j in range(-1, 2):
                if 0 <= x+j < len(maze[0]):
                    if maze[y+i][x+j] == pattern:
                        sum += 1

    return sum


def random_adj(x, y, Dx, Dy, Sx, Sy):
    x = random.randint(x-1, x+1)
    y = random.randint(y-1, y+1)

    if 0 >= x:
        x += 1
    elif x >= Dx:
        x -= 1

    if 0 >= y:
        y += 1
    elif y >= Dy:
        y -= 1

    if x == Sx and Sy == y:
        return random_adj(x, y, Dx, Dy, Sx, Sy)

    return x, y


def main():
    Dx = int(sys.argv[3])
    Dy = int(sys.argv[2])
    directions = ['W', 'A', 'S', 'D']
    maze, Sx, Sy, Ex, Ey = step_one_maze_gen(Dx, Dy, directions)
    maze = step_two_maze_gen(maze, Sx, Sy, Ex, Ey)
    maze[Sy][Sx] = 'S'
    maze[Ey][Ex] = 'E'
    save_in_file(maze, sys.argv[1], 'w')
    print("solution?")
    if input() == 'y':
        is_solvable(maze, Sx, Sy, Ex, Ey, True, [[Sy, Sx]])[1]
        save_in_file(maze, sys.argv[1], 'a')


main()
