"""
stolen from:
https://github.com/BHSPitMonkey/vmflib/blob/master/examples/maze.py
"""

import goldsrcmap as gsm
import random
import numpy


OUTPUT = 'maze.map'
MAZE_BLOCK_SIZE = 512
ROWS = 20
COLUMNS = 20
MAZE_WIDTH = MAZE_BLOCK_SIZE * ROWS
MAZE_HEIGHT = MAZE_BLOCK_SIZE * COLUMNS
MAZE_COMPLEXITY = 10
MAZE_DENSITY = 10
FLOOR_THICKNESS = 64

def maze_2d(width, height, complexity, density):
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)

    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density = int(density * (shape[0] // 2 * shape[1] // 2))
    maze_matrix = numpy.zeros(shape, dtype=bool)

    # Fill borders
    maze_matrix[0, :] = maze_matrix[-1, :] = 1
    maze_matrix[:, 0] = maze_matrix[:, -1] = 1

    for _ in range(density):
        x = random.randint(0, shape[1] // 2) * 2
        y = random.randint(0, shape[0] // 2) * 2
        maze_matrix[y, x] = 1
        for _ in range(complexity):
            neighbours = [
                (y, x - 2) if x > 1 else None,
                (y, x + 2) if x < shape[1] - 2 else None,
                (y - 2, x) if y > 1 else None,
                (y + 2, x) if y < shape[0] - 2 else None
            ]

            valid_neighbours = [neighbour for neighbour in neighbours if neighbour is not None]
            if valid_neighbours:
                neighbour_y, neighbour_x = random.choice(valid_neighbours)
                if maze_matrix[neighbour_y, neighbour_x] == 0:
                    maze_matrix[neighbour_y, neighbour_x] = 1
                    maze_matrix[neighbour_y + (y - neighbour_y) // 2, neighbour_x + (x - neighbour_x) // 2] = 1
                    x, y = neighbour_x, neighbour_y
    return maze_matrix

maze = maze_2d(ROWS-1, COLUMNS-1, MAZE_COMPLEXITY, MAZE_DENSITY)

m = gsm.Map()

blocks = []
for i in range(ROWS-1):
    for j in range(COLUMNS-1):
        if maze[i][j]:
            x = (i * MAZE_BLOCK_SIZE) - (MAZE_WIDTH / 2) + (MAZE_BLOCK_SIZE / 2)
            y = (j * MAZE_BLOCK_SIZE) - (MAZE_HEIGHT / 2) + (MAZE_BLOCK_SIZE / 2)
            blocks.append(gsm.BrushGenerator.cuboid(MAZE_BLOCK_SIZE, MAZE_BLOCK_SIZE, MAZE_BLOCK_SIZE, position=[x, y, 0]))


floor = gsm.BrushGenerator.cuboid(-MAZE_WIDTH, -MAZE_WIDTH, FLOOR_THICKNESS, position=[0, 0, -FLOOR_THICKNESS], center=True)

m.add_brush(floor, *blocks)

gsm.save_map(m, 'maze.map')
