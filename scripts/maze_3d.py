import goldsrcmap as gsm
import numpy
import random

OUTPUT = 'maze3d.map'
MAZE_BLOCK_SIZE = 256
ROWS = 10
COLUMNS = 10
LEVELS = 10
MAZE_WIDTH = MAZE_BLOCK_SIZE * ROWS
MAZE_HEIGHT = MAZE_BLOCK_SIZE * COLUMNS
MAZE_DEPTH = MAZE_BLOCK_SIZE * LEVELS
COMPLEXITY = 1
DENSITY = 1

def maze_3d(width, length, height, complexity, density):
    shape = (
        (height // 2) * 2 + 1,
        (width // 2) * 2 + 1,
        (length // 2) * 2 + 1
    )
    complexity = int(complexity * (5 * (shape[0] + shape[1] + shape[2])))
    density = int(density * (shape[0] // 2 * shape[1] // 2 * shape[2] // 2))

    maze_tensor = numpy.zeros(shape, dtype=bool)
    #EXTERIOR WALLS
    #maze_tensor[0, :, :] = maze_tensor[-1, :, :] = 1
    #maze_tensor[:, 0, :] = maze_tensor[:, -1, :] = 1
    #maze_tensor[:, :, 0] = maze_tensor[:, :, -1] = 1

    for _ in range(density):
        x, y, z = (
            random.randint(0, shape[1] // 2) * 2,
            random.randint(0, shape[0] // 2) * 2,
            random.randint(0, shape[2] // 2) * 2
        )
        maze_tensor[y, x, z] = 1
        for _ in range(complexity):
            neighbours = [
                (y, x - 2, z) if x > 1 else None,
                (y, x + 2, z) if x < shape[1] - 2 else None,
                (y - 2, x, z) if y > 1 else None,
                (y + 2, x, z) if y < shape[0] - 2 else None,
                (y, x, z - 2) if z > 1 else None,
                (y, x, z + 2) if z < shape[2] - 2 else None
            ]
            valid_neighbours = [neighbour for neighbour in neighbours if neighbour is not None]
            if valid_neighbours:
                neighbour_y, neighbour_x, neighbour_z = random.choice(valid_neighbours)
                if maze_tensor[neighbour_y, neighbour_x, neighbour_z] == 0:
                    maze_tensor[neighbour_y, neighbour_x, neighbour_z] = 1
                    maze_tensor[neighbour_y + (y - neighbour_y) // 2, neighbour_x + (x - neighbour_x) // 2, neighbour_z + (z - neighbour_z) // 2] = 1
                    x, y, z = neighbour_x, neighbour_y, neighbour_z
    return maze_tensor

maze = maze_3d(ROWS, COLUMNS, LEVELS, COMPLEXITY, DENSITY)

blocks_3d = []
for i in range(ROWS - 1):
    for j in range(COLUMNS - 1):
        for k in range(LEVELS - 1):
            #This only work when ROWS == COLUMNS == LEVELS:
            #if i != 0 and j != 0 and k != 0:

            # This works also when ROWS != COLUMNS != LEVELS:
            if 0 <= i < maze.shape[0] - 1 and 0 <= j < maze.shape[1] - 1 and 0 <= k < maze.shape[2] - 1:
                if maze[i, j, k]: 
                #if maze[i][j][k]:
                    x = (i * MAZE_BLOCK_SIZE) - (MAZE_WIDTH / 2) + (MAZE_BLOCK_SIZE / 2)
                    y = (j * MAZE_BLOCK_SIZE) - (MAZE_HEIGHT / 2) + (MAZE_BLOCK_SIZE / 2)
                    z = (k * MAZE_BLOCK_SIZE) - (MAZE_DEPTH / 2) + (MAZE_BLOCK_SIZE / 2)
                    blocks_3d.append(gsm.BrushGenerator.cuboid(MAZE_BLOCK_SIZE, MAZE_BLOCK_SIZE, MAZE_BLOCK_SIZE, position=[x, y, z]))


m = gsm.Map()
m.add_brush(*blocks_3d)

gsm.save_map(m, OUTPUT)
