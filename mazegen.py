import random as random


def step_one_maze_gen(x, y, directions):
    maze = []
    for i in range(0, y):
        maze.append([])
        for j in range(0, x):
            maze[i].append('#')

    Sx = random.randint(0, x-1)
    Sy = random.randint(0, y-1)
    Ex = random.randint(0, x-1)
    Ey = random.randint(0, y-1)

    Py = Sy
    Px = Sx

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


def is_solvable(maze, x, y, Ex, Ey, solution):
    # assigns the starting position
    path = [[y, x]]
    possible_moves = [get_possible_moves(maze, path, x, y)]

    invalid_path = []
    next_move = ''
    # loops while maze is not solved
    while x != Ex or y != Ey:
        # if all the direction possible of the position of the player were taken, go to the previous position
        if possible_moves[-1] == []:

            maze[path[-1][0]][path[-1][1]] = ' '

            invalid_path.append(path[-1])

            possible_moves.pop(-1)
            path.pop(-1)

            # if all possible paths were taken then unsolvable
            if path == []:
                return False
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
                if [y, x] != [Ey, Ey] and solution:
                    maze[path[-1][0]][path[-1][1]] = '@'
                # add all possibles moves
                possible_moves.append(get_possible_moves(maze, path, x, y))

            next_move = ''

    return True


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


def save_in_file(maze, file):
    f = open(file, 'a')
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            f.write(maze[i][j])
        f.write('\n')
    f.write('\n')
    f.write('====================================================================================================')
    f.write('\n')
    f.write('\n')
    f.close()


def print_maze(maze):
    for i in range(0, len(maze)):
        print('')
        for j in range(0, len(maze[0])):
            print(maze[i][j], end='')
    print('')


def step_two_maze_gen(maze, Sx, Sy, Ex, Ey):
    for k, l in [' ', '#'], ['#', ' ']:
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if check_adj(maze, j, i, k) < 2:
                    x, y = random_adj(j, i, len(maze[i]), len(maze))
                    maze[y][x] = k
                    if not is_solvable(maze, Sx, Sy, Ex, Ey, False):
                        maze[y][x] = l

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


def random_adj(x, y, Dx, Dy):
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

    return x, y


def main():
    Dx = random.randint(5, 100)
    Dy = random.randint(5, 100)
    Dx = 10
    Dy = 11
    directions = ['W', 'A', 'S', 'D']
    maze, Sx, Sy, Ex, Ey = step_one_maze_gen(Dx, Dy, directions)
    maze = step_two_maze_gen(maze, Sx, Sy, Ex, Ey)
    maze[Sy][Sx] = 'S'
    maze[Ey][Ex] = 'E'
    save_in_file(maze, 'maze_created.txt')

    if is_solvable(maze, Sx, Sy, Ex, Ey, True) == True:
        print_maze(maze)
        save_in_file(maze, 'maze_created.txt')
        print('\n')
        print("Maze is Valid")
    else:
        print("Maze is Invalid")


main()
