import random
import os


def create_chromosome(n):
    return random.sample(range(n), n)

def initialize_population(pop_size, n):
    return [create_chromosome(n) for _ in range(pop_size)]

def fitness(chromosome):
    n = len(chromosome)
    non_attacking = 0
    for i in range(n):
        for j in range(i + 1, n):
            if chromosome[i] != chromosome[j] and abs(chromosome[i] - chromosome[j]) != abs(i - j):
                non_attacking += 1
    return non_attacking

def fitness2(chromosome):
    n = len(chromosome)
    diagonal_conflicts = 0
    for i in range(n):
        for j in range(n):
            diagonal_conflicts += int(abs(chromosome[i] - chromosome[j]) == abs(i - j)) * (i!=j)
    return diagonal_conflicts

def tournament_selection(population, tournament_size, verbose=False):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=fitness2)  # Higher fitness is better
    if verbose:
        print( "\n".join( 
            [ f"Chromosome: {chromosome}, Fitness: {fitness2(chromosome)}" for chromosome in tournament ]
         ) ) 
    return tournament[-1]


opts = '''
1. create population
2. population fitness
3. tournament_selection
4. print population
'''

while (inp:=input(opts)) != '':
    if inp == '1':
        pop_size, n = input("pop size, N = ").split(',')
        population = initialize_population(pop_size=int(pop_size), n=int(n))
        print("Population created.")
    elif inp == '2':
        fitness_values = [fitness(chromosome) for chromosome in population]
        print(f"Fitness values: {fitness_values}")
    elif inp == '3':
        tourn_size = int(input("Tournament size= "))
        selected = tournament_selection(population, tournament_size=tourn_size, verbose=True)
        print(f"Selected chromosome: {selected}")
    elif inp == '4':
        print(f"Population: {population}")
    else:
        print("Invalid option. Please try again.")
    input()
    os.system('clear')
    

population = initialize_population(pop_size=10, n=5)




