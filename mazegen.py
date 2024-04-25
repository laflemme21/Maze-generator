import random as random
import sys
sys.setrecursionlimit(1001)


def maze_gen(x, y, directions):
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

    maze[Sy][Sx] = 'S'
    maze[Ey][Ex] = 'E'
    for i in range(0, y):
        print('')
        for j in range(0, x):
            print(maze[i][j], end='')
    print('')
    return maze, Sx, Sy, Ex, Ey


def valid_move(maze, x, y, check_for_space):
    if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
        if check_for_space and maze[y][x] != ' ':
            return False
        return True
    return False


def is_solvable(maze, directions, x, y, last_move, Ex, Ey):

    if x == Ex and y == Ey:
        return True
    else:
        if last_move != '':
            directions.remove(last_move)
        for direction in directions:
            new_Px, new_Py = move(x, y, direction)
            if valid_move(maze, new_Px, new_Py, True):
                x, y = new_Px, new_Py
                return is_solvable(maze, ['W', 'A', 'S', 'D'], x, y, direction, Ex, Ey)


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


def main():
    x = random.randint(5, 100)
    y = random.randint(5, 100)
    directions = ['W', 'A', 'S', 'D']
    maze, Sx, Sy, Ex, Ey = maze_gen(x, y, directions)
    save_in_file(maze, 'maze_created.txt')

    if is_solvable(maze, directions, Sx, Sy, '', Ex, Ey):
        print("Maze is Valid")
    else:
        print("wtf just happened")


main()
