import numpy as np
from solver_base import SolverBase

class ACOSolver(SolverBase):
    def __init__(self, maze, n_ants=20, evaporation=0.5, alpha=1, beta=2):
        super().__init__(maze)
        self.n_ants = n_ants
        self.evaporation = evaporation
        self.alpha = alpha  # Pheromone weight
        self.beta = beta    # Heuristic weight
        self.pheromones = np.ones((maze.height, maze.width))

    def solve(self, max_iter=100):
        for _ in range(max_iter):
            paths = []
            for _ in range(self.n_ants):
                path = self._construct_ant_path()
                paths.append(path)
                
            self._update_pheromones(paths)
            
        return self.best_path

    def _construct_ant_path(self):
        path = []
        current = (0, 0)
        
        while current != (self.maze.width-1, self.maze.height-1):
            neighbors = self.maze.get_neighbors(*current)
            if not neighbors:
                break
                
            probabilities = []
            for nx, ny in neighbors:
                pheromone = self.pheromones[ny][nx]
                heuristic = 1 / (abs(nx - (self.maze.width-1)) + 
                                abs(ny - (self.maze.height-1)) + 1e-6)
                probabilities.append((pheromone**self.alpha) * (heuristic**self.beta))
                
            total = sum(probabilities)
            if total == 0:
                break
                
            probabilities = [p/total for p in probabilities]
            chosen_idx = np.random.choice(len(neighbors), p=probabilities)
            current = neighbors[chosen_idx]
            path.append(current)
            
        return path

    def _update_pheromones(self, paths):
        # Evaporation
        self.pheromones *= self.evaporation
        
        # Add new pheromones
        for path in paths:
            path_length = self._calculate_path_length(path)
            if path_length < self.best_length:
                self.best_length = path_length
                self.best_path = path
                
            if path_length != float('inf'):
                pheromone_amount = 1 / path_length
                for (x, y) in path:
                    self.pheromones[y][x] += pheromone_amount