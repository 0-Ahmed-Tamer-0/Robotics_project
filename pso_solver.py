# import numpy as np
# from solver_base import SolverBase

# class PSOSolver(SolverBase):
#     def __init__(self, maze, n_particles=20, w=0.5, c1=1, c2=2):
#         super().__init__(maze)
#         self.n_particles = n_particles
#         self.w = w  # Inertia
#         self.c1 = c1  # Cognitive
#         self.c2 = c2  # Social
        
#         # Initialize particles
#         self.particles = []
#         for _ in range(n_particles):
#             particle = {
#                 'position': [],
#                 'velocity': [],
#                 'best_position': None,
#                 'best_length': float('inf')
#             }
#             self.particles.append(particle)
            
#         self.global_best = None

    # def solve(self, max_iter=100):
    #     for _ in range(max_iter):
    #         for particle in self.particles:
    #             path = self._generate_path(particle)
    #             length = self._calculate_path_length(path)
                
    #             if length < particle['best_length']:
    #                 particle['best_length'] = length
    #                 particle['best_position'] = path.copy()
                    
    #                 if length < self.best_length:
    #                     self.best_length = length
    #                     self.best_path = path.copy()
    #                     self.global_best = path.copy()
            
    #         self._update_velocities()
            
    #     return self.best_path

    # def _generate_path(self, particle):
    #     # Simplified path generation for demonstration
    #     path = []
    #     current = (0, 0)
    #     while current != (self.maze.width-1, self.maze.height-1):
    #         neighbors = self.maze.get_neighbors(*current)
    #         if not neighbors:
    #             break
    #         current = neighbors[np.random.choice(len(neighbors))]
    #         path.append(current)
    #     return path

#     def _update_velocities(self):
#         # Simplified velocity update (real implementation needs proper path encoding)
#         for particle in self.particles:
#             if particle['best_position'] and self.global_best:
#                 # This is simplified - real implementation needs proper path encoding
#                 new_velocity = (self.w * np.array(particle['velocity']) +
#                                self.c1 * np.random.rand() * (np.array(particle['best_position']) -
#                                np.array(particle['position'])) +
#                                self.c2 * np.random.rand() * (np.array(self.global_best) -
#                                np.array(particle['position'])))
#                 particle['velocity'] = new_velocity.tolist()
#                 particle['position'] = (np.array(particle['position']) + 
#                                       new_velocity).tolist()
# import numpy as np
# from solver_base import SolverBase

# class PSOSolver(SolverBase):
#     def __init__(self, maze, n_particles=20, w=0.5, c1=1, c2=2):
#         super().__init__(maze)
#         self.n_particles = n_particles
#         self.w = w
#         self.c1 = c1
#         self.c2 = c2
#         self.particles = [self._init_particle() for _ in range(n_particles)]
#         self.global_best = None

#     def _init_particle(self):
#         return {
#             'position': self._generate_random_path(),
#             'velocity': [],
#             'best_position': None,
#             'best_length': float('inf')
#         }

#     def _run_single_iteration(self):
#         for p in self.particles:
#             new_path = self._mutate_path(p['position'])
#             new_length = self.calculate_path_length(new_path)
            
#             if new_length < p['best_length']:
#                 p['best_position'] = new_path
#                 p['best_length'] = new_length
                
#                 if new_length < self.best_length:
#                     self.best_length = new_length
#                     self.best_path = new_path
#                     self.global_best = new_path.copy()
        
#         self._update_velocities()
#         self.iteration += 1

#     def _generate_random_path(self):
#         path = []
#         current = (0, 0)
#         while current != (self.maze.width-1, self.maze.height-1):
#             neighbors = self.maze.get_neighbors(*current)
#             if not neighbors:
#                 break
#             current = neighbors[np.random.choice(len(neighbors))]
#             path.append(current)
#         return path

#     def _mutate_path(self, path):
#         if not path:
#             return self._generate_random_path()
#         new_path = path.copy()
#         idx = np.random.randint(0, len(new_path))
#         neighbors = self.maze.get_neighbors(*new_path[idx])
#         if neighbors:
#             new_path[idx] = neighbors[np.random.choice(len(neighbors))]
#         return new_path

#     def _update_velocities(self):
#         # Simplified velocity update for path representation
#         for p in self.particles:
#             if p['best_position'] and self.global_best:
#                 cognitive = np.random.rand() * (len(p['best_position']) - len(p['position']))
#                 social = np.random.rand() * (len(self.global_best) - len(p['position']))
#                 new_vel = self.w * len(p['position']) + self.c1 * cognitive + self.c2 * social
#                 p['position'] = p['position'][:int(len(p['position']) + new_vel)]
import numpy as np
from solver_base import SolverBase
class PSOSolver(SolverBase):
    def __init__(self, maze, n_particles=20, w=0.5, c1=1, c2=2):
        super().__init__(maze)
        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.particles = [self._init_particle() for _ in range(n_particles)]
        self.global_best = None
        self.best_path = []  # Initialize empty path
        
    def solve(self, max_iter=100):
        for _ in range(max_iter):
            for particle in self.particles:
                path = self._generate_path(particle)
                length = self.calculate_path_length(path)
                
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
    
    
    def _init_particle(self):
         return {
             'position': self._generate_random_path(),
             'velocity': [],
             'best_position': None,
             'best_length': float('inf')
         }
         
    def _generate_random_path(self):
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
        # Simplified velocity update for path representation
        for p in self.particles:
            if p['best_position'] and self.global_best:
                cognitive = np.random.rand() * (len(p['best_position']) - len(p['position']))
                social = np.random.rand() * (len(self.global_best) - len(p['position']))
                new_vel = self.w * len(p['position']) + self.c1 * cognitive + self.c2 * social
                p['position'] = p['position'][:int(len(p['position']) + new_vel)]
    
    def _run_single_iteration(self):
        for p in self.particles:
            # Generate new path based on velocity
            new_path = self._mutate_path(p['position'])
            new_length = self.calculate_path_length(new_path)
            
            # Update personal best
            if new_length < p['best_length']:
                p['best_position'] = new_path.copy()
                p['best_length'] = new_length
                
                # Update global best
                if new_length < self.best_length:
                    self.best_length = new_length
                    self.best_path = new_path.copy()
                    self.global_best = new_path.copy()
        
        self._update_velocities()
        self.iteration += 1

    def _mutate_path(self, path):
        """Create a new path by modifying existing one"""
        if len(path) == 0:
            return self._generate_random_path()
            
        new_path = path.copy()
        
        # Randomly modify parts of the path
        if np.random.rand() < 0.3:  # 30% chance to mutate
            mutate_idx = np.random.randint(0, len(new_path))
            current = new_path[mutate_idx]
            neighbors = self.maze.get_neighbors(*current)
            if neighbors:
                new_path[mutate_idx] = neighbors[np.random.choice(len(neighbors))]
        
        return new_path