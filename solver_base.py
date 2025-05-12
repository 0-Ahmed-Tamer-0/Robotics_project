from abc import ABC, abstractmethod

class SolverBase(ABC):
    def __init__(self, maze):
        self.maze = maze
        self.best_path = None
        self.best_length = float('inf')

    @abstractmethod
    def solve(self, max_iter=100):
        pass

    def _calculate_path_length(self, path):
        """Penalize invalid paths with infinity"""
        current = (0, 0)
        length = 0
        
        for step in path:
            if step not in self.maze.get_neighbors(*current):
                return float('inf')
            length += 1
            current = step
            
        if current != (self.maze.width-1, self.maze.height-1):
            return float('inf')
        return length