# import numpy as np

# class MazeGenerator:
#     def __init__(self, width=10, height=10, obstacle_density=0.2):
#         self.width = width
#         self.height = height
#         self.grid = np.zeros((height, width))  # 0 = free, 1 = wall

#         # Add random obstacles
#         num_obstacles = int(width * height * obstacle_density)
#         for _ in range(num_obstacles):
#             x, y = np.random.randint(0, width), np.random.randint(0, height)
#             self.grid[y][x] = 1

#         # Ensure start (0,0) and goal (width-1, height-1) are free
#         self.grid[0][0] = 0
#         self.grid[height-1][width-1] = 0

#     def get_neighbors(self, x, y):
#         """Get valid neighboring cells"""
#         neighbors = []
#         for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.width and 0 <= ny < self.height:
#                 if self.grid[ny][nx] == 0:
#                     neighbors.append((nx, ny))
#         return neighbors

#     def print_maze(self):
#         for row in self.grid:
#             print(' '.join(['█' if cell == 1 else '.' for cell in row]))
            
            
# class DynamicMazeGenerator(MazeGenerator):
#     def __init__(self, width=10, height=10, obstacle_density=0.2, move_prob=0.1):
#         super().__init__(width, height, obstacle_density)
#         self.move_prob = move_prob  # Probability of obstacle moving each step
#         self.original_grid = self.grid.copy()
        
#     def step(self):
#         """Move obstacles randomly while preserving connectivity"""
#         new_grid = self.original_grid.copy()
        
#         # Identify movable obstacles
#         movable = [(x,y) for y in range(self.height) 
#                   for x in range(self.width) 
#                   if self.grid[y][x] == 1 and (x,y) != (0,0) 
#                   and (x,y) != (self.width-1, self.height-1)]
        
#         for x,y in movable:
#             if np.random.rand() < self.move_prob:
#                 neighbors = self._get_free_neighbors(x, y)
#                 if neighbors:
#                     new_grid[y][x] = 0  # Remove from current position
#                     nx, ny = neighbors[np.random.choice(len(neighbors))]
#                     new_grid[ny][nx] = 1  # Add to new position
                    
#         self.grid = new_grid
        
#     def _get_free_neighbors(self, x, y):
#         """Find empty cells around a position"""
#         candidates = []
#         for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.width and 0 <= ny < self.height:
#                 if self.grid[ny][nx] == 0:
#                     candidates.append((nx, ny))
#         return candidates
import numpy as np

class MazeGenerator:
    def __init__(self, width=10, height=10, obstacle_density=0.2):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))  # 0 = free, 1 = wall

        # Add random obstacles while ensuring path exists
        while True:
            self.grid = np.random.choice([0, 1], size=(height, width), 
                        p=[1-obstacle_density, obstacle_density])
            self.grid[0, 0] = 0  # Start
            self.grid[-1, -1] = 0  # Goal
            if self._path_exists():
                break

    def _path_exists(self):
        # Simple BFS check
        visited = np.zeros_like(self.grid)
        queue = [(0, 0)]
        while queue:
            x, y = queue.pop(0)
            if (x, y) == (self.width-1, self.height-1):
                return True
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny, nx] == 0 and not visited[ny, nx]:
                        visited[ny, nx] = 1
                        queue.append((nx, ny))
        return False

    def get_neighbors(self, x, y):
        return [(nx, ny) for nx, ny in 
                [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                if 0 <= nx < self.width and 0 <= ny < self.height
                and self.grid[ny, nx] == 0]