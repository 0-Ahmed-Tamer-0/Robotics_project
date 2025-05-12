import itertools
import time
import numpy as np
from maze_generator import MazeGenerator
from aco_solver import ACOSolver
from pso_solver import PSOSolver
from abc_solver import ABCSolver

import random
import time
import numpy as np
from joblib import Parallel, delayed  # For parallel processing

def tune_algorithm_fast(algorithm_class, param_ranges, 
                       maze_size=10, trials=5, iterations=50,
                       n_samples=20, n_jobs=-1):
    """
    Faster tuning using:
    - Random sampling instead of grid search
    - Smaller maze size
    - Parallel execution
    - Early stopping
    """
    def evaluate_params(params):
        total_length = 0
        success_count = 0
        
        for _ in range(trials):
            # Use same maze for all trials of this param set
            maze = MazeGenerator(maze_size, maze_size, obstacle_density=0.2)
            solver = algorithm_class(maze, **params)
            
            # Early stopping check
            best_seen = float('inf')
            no_improvement = 0
            for _ in range(iterations):
                solver._run_single_iteration()
                if solver.best_length < best_seen:
                    best_seen = solver.best_length
                    no_improvement = 0
                else:
                    no_improvement += 1
                
                if no_improvement > 10:  # Stop if no improvement for 10 iterations
                    break
            
            if solver.best_length < float('inf'):
                total_length += solver.best_length
                success_count += 1
                
        if success_count == 0:
            return (params, float('inf'))
            
        avg_length = total_length / success_count
        success_rate = success_count / trials
        return (params, avg_length * (1 + (1 - success_rate)))

    # Generate random parameter combinations
    param_samples = [
        {k: random.choice(v) for k, v in param_ranges.items()}
        for _ in range(n_samples)
    ]

    # Parallel execution
    results = Parallel(n_jobs=n_jobs)(
        delayed(evaluate_params)(params) for params in param_samples
    )

    # Find best parameters
    best_score = float('inf')
    best_params = None
    for params, score in results:
        if score < best_score:
            best_score = score
            best_params = params
            
    return best_params, best_score

# Simplified parameter ranges
ACO_RANGES = {
    'n_ants': [20, 30],
    'evaporation': [0.3, 0.5],
    'alpha': [1, 2],
    'beta': [1, 2]
}

PSO_RANGES = {
    'n_particles': [20, 30],
    'w': [0.4, 0.6],
    'c1': [1.0, 1.5],
    'c2': [1.5, 2.0]
}

ABC_RANGES = {
    'n_employed': [15, 20],
    'limit': [30, 50]
}

if __name__ == "__main__":
    # Tune with faster method (takes ~5-10 minutes instead of hours)
    aco_params, aco_score = tune_algorithm_fast(ACOSolver, ACO_RANGES, n_samples=15)
    pso_params, pso_score = tune_algorithm_fast(PSOSolver, PSO_RANGES, n_samples=15)
    abc_params, abc_score = tune_algorithm_fast(ABCSolver, ABC_RANGES, n_samples=15)
    
    print("\n=== Optimal Parameters ===")
    print(f"ACO: {aco_params} | Score: {aco_score:.2f}")
    print(f"PSO: {pso_params} | Score: {pso_score:.2f}")
    print(f"ABC: {abc_params} | Score: {abc_score:.2f}")