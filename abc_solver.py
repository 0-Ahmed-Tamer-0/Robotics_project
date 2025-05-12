# import numpy as np
# from solver_base import SolverBase

# class ABCSolver(SolverBase):
#     def __init__(self, maze, n_employed=20, n_onlooker=20, limit=100):
#         super().__init__(maze)
#         self.n_employed = n_employed
#         self.n_onlooker = n_onlooker
#         self.limit = limit  # Abandonment limit
        
#         self.food_sources = []
#         for _ in range(n_employed):
#             path = self._generate_random_path()
#             self.food_sources.append({
#                 'path': path,
#                 'fitness': 1 / self._calculate_path_length(path),
#                 'trials': 0
#             })

    # def solve(self, max_iter=100):
    #     for _ in range(max_iter):
    #         # Employed bee phase
    #         for i in range(self.n_employed):
    #             new_path = self._mutate_path(self.food_sources[i]['path'])
    #             new_fitness = 1 / self._calculate_path_length(new_path)
                
    #             if new_fitness > self.food_sources[i]['fitness']:
    #                 self.food_sources[i]['path'] = new_path
    #                 self.food_sources[i]['fitness'] = new_fitness
    #                 self.food_sources[i]['trials'] = 0
    #             else:
    #                 self.food_sources[i]['trials'] += 1

    #         # Onlooker bee phase
    #         fitness_sum = sum(fs['fitness'] for fs in self.food_sources)
    #         for _ in range(self.n_onlooker):
    #             selected = np.random.choice(
    #                 self.food_sources,
    #                 p=[fs['fitness']/fitness_sum for fs in self.food_sources]
    #             )
    #             # ... similar to employed phase ...
            
    #         # Scout bee phase
    #         for i in range(self.n_employed):
    #             if self.food_sources[i]['trials'] >= self.limit:
    #                 self.food_sources[i]['path'] = self._generate_random_path()
    #                 self.food_sources[i]['fitness'] = 1 / self._calculate_path_length(self.food_sources[i]['path'])
    #                 self.food_sources[i]['trials'] = 0
            
    #         # Update best path
    #         for fs in self.food_sources:
    #             length = 1 / fs['fitness']
    #             if length < self.best_length:
    #                 self.best_length = length
    #                 self.best_path = fs['path']
                    
    #     return self.best_path

#     def _generate_random_path(self):
#         # Similar to PSO's path generation
#         pass

#     def _mutate_path(self, path):
#         # Randomly modify some steps in the path
#         new_path = path.copy()
#         if len(new_path) > 0:
#             mutate_idx = np.random.randint(0, len(new_path))
#             neighbors = self.maze.get_neighbors(*new_path[mutate_idx])
#             if neighbors:
#                 new_path[mutate_idx] = neighbors[np.random.choice(len(neighbors))]
#         return new_path
import numpy as np
from solver_base import SolverBase

class ABCSolver(SolverBase):
    def __init__(self, maze, n_employed=20, n_onlooker=20, limit=50):
        super().__init__(maze)
        self.n_employed = n_employed
        self.n_onlooker = n_onlooker
        self.limit = limit
        self.food_sources = [self._init_food_source() for _ in range(n_employed)]
        
    def solve(self, max_iter=100):
        for _ in range(max_iter):
            # Employed bee phase
            for i in range(self.n_employed):
                new_path = self._mutate_path(self.food_sources[i]['path'])
                new_fitness = 1 / self.calculate_path_length(new_path)
                
                if new_fitness > self.food_sources[i]['fitness']:
                    self.food_sources[i]['path'] = new_path
                    self.food_sources[i]['fitness'] = new_fitness
                    self.food_sources[i]['trials'] = 0
                else:
                    self.food_sources[i]['trials'] += 1

            # Onlooker bee phase
            fitness_sum = sum(fs['fitness'] for fs in self.food_sources)
            for _ in range(self.n_onlooker):
                selected = np.random.choice(
                    self.food_sources,
                    p=[fs['fitness']/fitness_sum for fs in self.food_sources]
                )
                # ... similar to employed phase ...
            
            # Scout bee phase
            for i in range(self.n_employed):
                if self.food_sources[i]['trials'] >= self.limit:
                    self.food_sources[i]['path'] = self._generate_random_path()
                    self.food_sources[i]['fitness'] = 1 / self.calculate_path_length(self.food_sources[i]['path'])
                    self.food_sources[i]['trials'] = 0
            
            # Update best path
            for fs in self.food_sources:
                length = 1 / fs['fitness']
                if length < self.best_length:
                    self.best_length = length
                    self.best_path = fs['path']
                    
        return self.best_path

    def _init_food_source(self):
        path = self._generate_random_path()
        return {
            'path': path,
            'fitness': 1 / self.calculate_path_length(path),
            'trials': 0
        }

    def _run_single_iteration(self):
        # Employed phase
        for fs in self.food_sources:
            new_path = self._mutate_path(fs['path'])
            new_fitness = 1 / self.calculate_path_length(new_path)
            if new_fitness > fs['fitness']:
                fs.update({'path': new_path, 'fitness': new_fitness, 'trials': 0})
            else:
                fs['trials'] += 1

        # Onlooker phase
        total_fitness = sum(fs['fitness'] for fs in self.food_sources)
        for _ in range(self.n_onlooker):
            fs = np.random.choice(self.food_sources, 
                                 p=[fs['fitness']/total_fitness for fs in self.food_sources])
            # ... similar mutation logic ...

        # Scout phase
        for i, fs in enumerate(self.food_sources):
            if fs['trials'] >= self.limit:
                self.food_sources[i] = self._init_food_source()

        # Update best path
        for fs in self.food_sources:
            length = 1 / fs['fitness']
            if length < self.best_length:
                self.best_length = length
                self.best_path = fs['path']
        
        self.iteration += 1

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

    def _mutate_path(self, path):
        if not path:
            return self._generate_random_path()
        new_path = path.copy()
        idx = np.random.randint(0, len(new_path))
        neighbors = self.maze.get_neighbors(*new_path[idx])
        if neighbors:
            new_path[idx] = neighbors[np.random.choice(len(neighbors))]
        return new_path