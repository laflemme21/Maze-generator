import random
import sys


def step_one_maze_gen(x, y, directions):
    maze = {}
    for i in range(0, y):
        maze[i] = {}
        for j in range(0, x):
            maze[i][j] = '#'

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
    path = {}
    index_of_path = 0
    invalid_path = []
    possible_moves = []
    for i in previous_solution.values():
        if maze[i[0]][i[1]] == '#':
            break
        else:
            path[index_of_path] = i
            index_of_path += 1
            possible_moves.append(get_possible_moves(maze, path, i[1], i[0]))
    # assigns the starting position
    next_move = ''
    # loops while maze is not solved
    y, x = path[index_of_path-1][0], path[index_of_path-1][1]
    while path[index_of_path-1][1] != Ex or path[index_of_path-1][0] != Ey:
        # if all the direction possible of the position of the player were taken, go to the previous position
        if possible_moves[-1] == []:

            maze[path[index_of_path-1][0]][path[index_of_path-1][1]] = ' '

            invalid_path.append(path[index_of_path-1])

            possible_moves.pop()
            path.pop(index_of_path-1)
            index_of_path -= 1

            # if all possible paths were taken then unsolvable
            if path == {}:
                return {}, False
            y, x = path[index_of_path-1][0], path[index_of_path-1][1]
        else:
            # move and mark it as taken
            next_move = possible_moves[-1][0]
            possible_moves[-1].pop(0)

        if next_move != '':
            new_Px, new_Py = move(x, y, next_move)
            if [new_Py, new_Px] in path.values():
                # go back
                while path[index_of_path-1] != [new_Py, new_Px]:

                    maze[path[index_of_path-1][0]
                         ][path[index_of_path-1][1]] = ' '

                    path.pop(index_of_path-1)
                    index_of_path -= 1
                    possible_moves.pop()
                y, x = path[index_of_path-1][0], path[index_of_path-1][1]

            elif valid_move(maze, new_Px, new_Py, True) and [new_Py, new_Px] not in invalid_path:
                # assign coordinates to new
                x, y = new_Px, new_Py
                # move the player
                path[index_of_path] = [y, x]
                index_of_path += 1
                if [y, x] != [Ey, Ey] and is_solution_outputted:
                    maze[path[index_of_path-1][0]
                         ][path[index_of_path-1][1]] = '@'
                # add all possibles moves
                possible_moves.append(get_possible_moves(maze, path, x, y))

            next_move = ''
    return path, True


def get_possible_moves(maze, path, x, y):
    possible_moves = []
    for i in ['W', 'A', 'S', 'D']:
        new_Px, new_Py = move(x, y, i)
        if valid_move(maze, new_Px, new_Py, True) and [new_Py, new_Px] not in path.values():
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
    if param == 'a':
        f.write('\n')
        f.write('====================================================================================================')
        f.write('\n')
        f.write('\n')
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            f.write(maze[i][j])
        f.write('\n')

    f.close()


def step_two_maze_gen(maze, Sx, Sy, Ex, Ey):
    path_ = {0: [Sy, Sx]}
    for pattern, pattern_opp, pattern_amount in [' ', '#', 4], ['#', ' ', 2]:
        for i in range(0, len(maze)):
            for j in range(0, len(maze[i])):
                if maze[i][j] == pattern_opp and check_adj(maze, j, i, pattern) <= pattern_amount:
                    # random position
                    x1, y1 = random_adj(
                        j, i, len(maze[i]), len(maze), Sx, Sy)
                    x2, y2 = random_adj(
                        j, i, len(maze[i]), len(maze), Sx, Sy)
                    # assign it to the pattern populating
                    maze[y1][x1] = pattern
                    maze[y2][x2] = pattern
                    # store the solution if true
                    new_path, boolean = is_solvable(
                        maze, Sx, Sy, Ex, Ey, False, path_)
                    if not boolean:
                        maze[y1][x1] = pattern_opp
                        maze[y2][x2] = pattern_opp
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
    if 5 <= Dx <= 100 and 5 <= Dy <= 100:
        directions = ['W', 'A', 'S', 'D']
        maze, Sx, Sy, Ex, Ey = step_one_maze_gen(Dx, Dy, directions)
        maze = step_two_maze_gen(maze, Sx, Sy, Ex, Ey)
        maze[Sy][Sx] = 'S'
        maze[Ey][Ex] = 'E'
        save_in_file(maze, sys.argv[1], 'w')
        print("solution?")
        if input() == 'y':
            is_solvable(maze, Sx, Sy, Ex, Ey, True, {0: [Sy, Sx]})
            save_in_file(maze, sys.argv[1], 'a')
    else:
        print("Invalid maze size")


main()
