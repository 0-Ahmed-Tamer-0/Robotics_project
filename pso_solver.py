import numpy as np
from solver_base import SolverBase

class PSOSolver(SolverBase):
    def __init__(self, maze, n_particles=20, w=0.5, c1=1, c2=2):
        super().__init__(maze)
        self.n_particles = n_particles
        self.w = w  # Inertia
        self.c1 = c1  # Cognitive
        self.c2 = c2  # Social
        
        # Initialize particles
        self.particles = []
        for _ in range(n_particles):
            particle = {
                'position': [],
                'velocity': [],
                'best_position': None,
                'best_length': float('inf')
            }
            self.particles.append(particle)
            
        self.global_best = None

    def solve(self, max_iter=100):
        for _ in range(max_iter):
            for particle in self.particles:
                path = self._generate_path(particle)
                length = self._calculate_path_length(path)
                
                if length < particle['best_length']:
                    particle['best_length'] = length
                    particle['best_position'] = path.copy()
                    
                    if length < self.best_length:
                        self.best_length = length
                        self.best_path = path.copy()
                        self.global_best = path.copy()
            
            self._update_velocities()
            
        return self.best_path

    def _generate_path(self, particle):
        # Simplified path generation for demonstration
        path = []
        current = (0, 0)
        while current != (self.maze.width-1, self.maze.height-1):
            neighbors = self.maze.get_neighbors(*current)
            if not neighbors:
                break
            current = neighbors[np.random.choice(len(neighbors))]
            path.append(current)
        return path

    def _update_velocities(self):
        # Simplified velocity update (real implementation needs proper path encoding)
        for particle in self.particles:
            if particle['best_position'] and self.global_best:
                # This is simplified - real implementation needs proper path encoding
                new_velocity = (self.w * np.array(particle['velocity']) +
                               self.c1 * np.random.rand() * (np.array(particle['best_position']) -
                               np.array(particle['position'])) +
                               self.c2 * np.random.rand() * (np.array(self.global_best) -
                               np.array(particle['position'])))
                particle['velocity'] = new_velocity.tolist()
                particle['position'] = (np.array(particle['position']) + 
                                      new_velocity).tolist()