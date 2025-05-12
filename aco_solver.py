# import numpy as np
# from solver_base import SolverBase

# class ACOSolver(SolverBase):
#     def __init__(self, maze, n_ants=20, evaporation=0.3, alpha=1, beta=2):
#         super().__init__(maze)
#         self.n_ants = n_ants
#         self.evaporation = evaporation
#         self.alpha = alpha
#         self.beta = beta
#         self.pheromones = np.ones((maze.height, maze.width))
#         self.iteration = 0
#         self.max_iter = 100

#     def _run_single_iteration(self):
#         """Run one iteration of ACO (called by visualizer)"""
#         if self.iteration >= self.max_iter:
#             return

#         paths = []
#         for _ in range(self.n_ants):
#             path = self._construct_ant_path()
#             paths.append(path)
            
#         self._update_pheromones(paths)
#         self.iteration += 1

#     def _construct_ant_path(self):
#         """Generate path for a single ant"""
#         path = []
#         current = (0, 0)
        
#         while current != (self.maze.width-1, self.maze.height-1):
#             neighbors = self.maze.get_neighbors(*current)
#             if not neighbors:
#                 break
                
#             probabilities = []
#             for nx, ny in neighbors:
#                 pheromone = self.pheromones[ny][nx]
#                 heuristic = 1 / (abs(nx - (self.maze.width-1)) + abs(ny - (self.maze.height-1)) + 1e-6)
#                 probabilities.append((pheromone**self.alpha) * (heuristic**self.beta))
                
#             total = sum(probabilities)
#             if total == 0:
#                 break
                
#             probabilities = [p/total for p in probabilities]
#             chosen_idx = np.random.choice(len(neighbors), p=probabilities)
#             current = neighbors[chosen_idx]
#             path.append(current)
            
#         return path

#     def _update_pheromones(self, paths):
#         """Update pheromone matrix"""
#         self.pheromones *= self.evaporation
        
#         for path in paths:
#             path_length = self._calculate_path_length(path)
#             if path_length < self.best_length:
#                 self.best_length = path_length
#                 self.best_path = path
                
#             if path_length != float('inf'):
#                 pheromone_amount = 1 / path_length
#                 for (x, y) in path:
#                     self.pheromones[y][x] += pheromone_amount

    # def solve(self, max_iter=100):
    #     """Traditional solving without visualization"""
    #     self.max_iter = max_iter
    #     self.iteration = 0
    #     while self.iteration < self.max_iter:
    #         self._run_single_iteration()
    #     return self.best_path
                    
                    
# class EnhancedACOSolver(ACOSolver):
#     def __init__(self, maze, n_ants=20, evaporation=0.5, alpha=1, beta=2):
#         super().__init__(maze)
#         self.n_ants = n_ants
#         self.evaporation = evaporation
#         self.alpha = alpha  # Pheromone weight
#         self.beta = beta    # Heuristic weight
#         self.pheromones = np.ones((maze.height, maze.width))

    # def solve(self, max_iter=100,dynamic_maze=None):
    #     for _ in range(max_iter):
    #         if dynamic_maze:
    #             dynamic_maze.stop()
    #             self._handle_maze_changes(dynamic_maze)
    #         paths = []
    #         for _ in range(self.n_ants):
    #             path = self._construct_ant_path()
    #             paths.append(path)
                
    #         self._update_pheromones(paths)
            
    #     return self.best_path

#     def _construct_ant_path(self):
#         path = []
#         current = (0, 0)
        
#         while current != (self.maze.width-1, self.maze.height-1):
#             neighbors = self.maze.get_neighbors(*current)
#             if not neighbors:
#                 break
                
#             probabilities = []
#             for nx, ny in neighbors:
#                 pheromone = self.pheromones[ny][nx]
#                 heuristic = 1 / (abs(nx - (self.maze.width-1)) + 
#                                 abs(ny - (self.maze.height-1)) + 1e-6)
#                 probabilities.append((pheromone**self.alpha) * (heuristic**self.beta))
                
#             total = sum(probabilities)
#             if total == 0:
#                 break
                
#             probabilities = [p/total for p in probabilities]
#             chosen_idx = np.random.choice(len(neighbors), p=probabilities)
#             current = neighbors[chosen_idx]
#             path.append(current)
            
#         return path

#     def _update_pheromones(self, paths):
#         # Evaporation
#         self.pheromones *= self.evaporation
        
#         # Add new pheromones
#         for path in paths:
#             path_length = self._calculate_path_length(path)
#             if path_length < self.best_length:
#                 self.best_length = path_length
#                 self.best_path = path
                
#             if path_length != float('inf'):
#                 pheromone_amount = 1 / path_length
#                 for (x, y) in path:
#                     self.pheromones[y][x] += pheromone_amount
#     def _handle_maze_changes(self, dynamic_maze):
#         """Reset invalid pheromones when obstacles move"""
#         for y in range(self.maze.height):
#             for x in range(self.maze.width):
#                 if dynamic_maze.grid[y][x] == 1 and self.pheromones[y][x] > 0:
#                     self.pheromones[y][x] = 0
import numpy as np
from solver_base import SolverBase

class ACOSolver(SolverBase):
    def __init__(self, maze, n_ants=20, evaporation=0.3, alpha=1, beta=2):
        super().__init__(maze)
        self.n_ants = n_ants
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta
        self.pheromones = np.ones((maze.height, maze.width))

    def _run_single_iteration(self):
        paths = [self._construct_ant_path() for _ in range(self.n_ants)]
        self._update_pheromones(paths)
        self.iteration += 1

    def _construct_ant_path(self):
        path = []
        current = (0, 0)
        while current != (self.maze.width-1, self.maze.height-1):
            neighbors = self.maze.get_neighbors(*current)
            if not neighbors:
                break
            probs = [self._calculate_probability(n, current) for n in neighbors]
            chosen = neighbors[np.random.choice(len(neighbors), p=probs/np.sum(probs))]
            path.append(chosen)
            current = chosen
        return path

    def _calculate_probability(self, neighbor, current):
        pheromone = self.pheromones[neighbor[1], neighbor[0]]
        heuristic = 1 / (abs(neighbor[0] - (self.maze.width-1)) + 
                   abs(neighbor[1] - (self.maze.height-1)) + 1e-6)
        return (pheromone ** self.alpha) * (heuristic ** self.beta)

    def _update_pheromones(self, paths):
        self.pheromones *= self.evaporation
        for path in paths:
            length = self.calculate_path_length(path)
            if length < self.best_length:
                self.best_length = length
                self.best_path = path
            if length != float('inf'):
                for x, y in path:
                    self.pheromones[y, x] += 1 / length
    
    def solve(self, max_iter=10):
        """Traditional solving without visualization"""
        self.max_iter = max_iter
        self.iteration = 0
        while self.iteration < self.max_iter:
            self._run_single_iteration()
        return self.best_path