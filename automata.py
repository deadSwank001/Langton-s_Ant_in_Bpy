"""Finite, wrapping cellular automata independent of Blender."""


class LangtonsAnt:
    def __init__(self, width, height):
        if width < 1 or height < 1:
            raise ValueError("Board dimensions must be positive")
        self.width, self.height = width, height
        self.cells = set()
        self.position = (width // 2, height // 2)
        self.direction = 0  # North, east, south, west.

    def step(self):
        x, y = self.position
        if (x, y) in self.cells:
            self.direction = (self.direction - 1) % 4
            self.cells.remove((x, y))
        else:
            self.direction = (self.direction + 1) % 4
            self.cells.add((x, y))
        dx, dy = ((0, 1), (1, 0), (0, -1), (-1, 0))[self.direction]
        self.position = ((x + dx) % self.width, (y + dy) % self.height)


class Life:
    def __init__(self, width, height, cells):
        if width < 3 or height < 3:
            raise ValueError("Game of Life needs dimensions of at least 3")
        if any(not (0 <= x < width and 0 <= y < height) for x, y in cells):
            raise ValueError("Cells must be inside the board")
        self.width, self.height = width, height
        self.cells = set(cells)

    def step(self):
        counts = {}
        for x, y in self.cells:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    neighbor = ((x + dx) % self.width, (y + dy) % self.height)
                    counts[neighbor] = counts.get(neighbor, 0) + 1
        self.cells = {cell for cell, count in counts.items()
                      if count == 3 or (count == 2 and cell in self.cells)}
