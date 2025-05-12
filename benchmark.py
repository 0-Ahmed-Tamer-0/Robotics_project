import time
from maze_generator import MazeGenerator
from aco_solver import ACOSolver
from pso_solver import PSOSolver
from abc_solver import ABCSolver

def run_benchmark(maze_size=10, iterations=10):
    results = []
    
    for _ in range(iterations):
        maze = MazeGenerator(maze_size, maze_size)
        
        # Test ACO
        start = time.time()
        aco = ACOSolver(maze)
        aco_path = aco.solve()
        aco_time = time.time() - start
        
        # Test PSO
        start = time.time()
        pso = PSOSolver(maze)
        pso_path = pso.solve()
        pso_time = time.time() - start
        
        # Test ABC
        start = time.time()
        abc = ABCSolver(maze)
        abc_path = abc.solve()
        abc_time = time.time() - start
        
        results.append({
            'aco': {'time': aco_time, 'length': len(aco_path)},
            'pso': {'time': pso_time, 'length': len(pso_path)},
            'abc': {'time': abc_time, 'length': len(abc_path)}
        })
        
    return results