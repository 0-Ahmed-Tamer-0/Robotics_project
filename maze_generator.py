import numpy as np

class MazeGenerator:
    def __init__(self, width=10, height=10, obstacle_density=0.2):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))  # 0 = free, 1 = wall

        # Add random obstacles
        num_obstacles = int(width * height * obstacle_density)
        for _ in range(num_obstacles):
            x, y = np.random.randint(0, width), np.random.randint(0, height)
            self.grid[y][x] = 1

        # Ensure start (0,0) and goal (width-1, height-1) are free
        self.grid[0][0] = 0
        self.grid[height-1][width-1] = 0

    def get_neighbors(self, x, y):
        """Get valid neighboring cells"""
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] == 0:
                    neighbors.append((nx, ny))
        return neighbors

    def print_maze(self):
        for row in self.grid:
            print(' '.join(['█' if cell == 1 else '.' for cell in row]))