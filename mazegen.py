import random as random


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
    return maze, Sx, Sy, Ex, Ey


def valid_move(maze, x, y, check_for_space):
    if (0 <= y < len(maze)) and (0 <= x < len(maze[0])):
        if check_for_space and maze[y][x] == '#':
            return False
        return True
    return False


def is_solvable(maze, x, y, Ex, Ey):
    # assigns the starting position
    path = [[y, x]]
    possible_moves = [get_possible_moves(maze, path, x, y)]
    next_move = ''
    c = 0
    # loops while maze is not solved
    while x != Ex or y != Ey:
        c += 1
        # if all the direction possible of the position of the player were taken, go to the previous position
        if possible_moves[-1] == []:

            maze[path[-1][0]][path[-1][1]] = ' '

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
            elif valid_move(maze, new_Px, new_Py, True):
                # assign coordinates to new
                x, y = new_Px, new_Py
                # move the player
                path.append([y, x])
                if [y, x] != [Ey, Ey]:
                    maze[path[-1][0]][path[-1][1]] = '@'
                # add all possibles moves
                possible_moves.append(get_possible_moves(maze, path, x, y))

            next_move = ''

    print_maze(maze)
    print(c)
    save_in_file(maze, 'maze_created.txt')
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


def main():
    x = random.randint(5, 100)
    y = random.randint(5, 100)
    x = 40
    y = 40
    directions = ['W', 'A', 'S', 'D']
    maze, Sx, Sy, Ex, Ey = maze_gen(x, y, directions)
    save_in_file(maze, 'maze_created.txt')
    print_maze(maze)
    print('\n |||||||||||||||||||||||||||||||\n')
    if is_solvable(maze, Sx, Sy, Ex, Ey) == True:
        print("Maze is Valid")
    else:
        print("wtf just happened")


main()
