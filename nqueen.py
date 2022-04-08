from dataclasses import dataclass
import random
from typing import List


@dataclass
class Population:
    population: list
    fitness: int


class App:
    def __init__(self, n, mutation_probability=0.5, num_population_initial=100, verbose=1):
        self.n = n
        self.max_fitness = (n * (n - 1)) / 2
        self.mutation_probability = mutation_probability
        random_chromosome = [self.random_chromosome(n) for _ in range(num_population_initial)]
        self.populations: List[Population] = [Population(r, self.get_fitness(r)) for r in random_chromosome]

        self.verbose = verbose

    def print_v(self, *args, v=1, **kwargs):
        if self.verbose >= v:
            print(*args, **kwargs)

    def mutate(self, x):
        n = len(x)
        c = random.randint(0, n - 1)
        m = random.randint(1, n)
        x[c] = m
        return x

    def reproduce(self, x, y):
        n = len(x)
        c = random.randint(0, n - 1)
        return x[0:c] + y[c:n]

    def random_chromosome(self, size):
        return [random.randint(1, size) for _ in range(size)]

    def random_pick(self):
        fitnesses = [p.fitness for p in self.populations]
        total = sum(fitnesses)
        r = random.uniform(0, total)
        upto = 0
        for p in self.populations:
            c, w = p.population, p.fitness
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"

    def get_fitness(self, chromosome):
        horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
        diagonal_collisions = 0

        n = len(chromosome)
        left_diagonal = [0] * 2 * n
        right_diagonal = [0] * 2 * n
        for i in range(n):
            left_diagonal[i + chromosome[i] - 1] += 1
            right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

        for i in range(2 * n - 1):
            counter = 0
            if left_diagonal[i] > 1:
                counter += left_diagonal[i] - 1
            if right_diagonal[i] > 1:
                counter += right_diagonal[i] - 1
            diagonal_collisions += counter / (n - abs(i - n + 1))

        return int(self.max_fitness - (horizontal_collisions + diagonal_collisions))  # 28-(2+3)=23

    def genetic_queen(self):
        new_populations: List[Population] = list()
        for _ in range(len(self.populations)):
            x = self.random_pick()
            y = self.random_pick()
            child = self.reproduce(x, y)
            if random.random() < self.mutation_probability:
                child = self.mutate(child)

            child_fitness = self.get_fitness(child)
            new_populations.append(Population(child, child_fitness))

            self.print_v(f"Chromosome = {child},  Fitness = {child_fitness}", v=2)

            if child_fitness == self.max_fitness:
                break
        self.populations = new_populations

    def print_board(self, population):
        n = len(population)
        board = [["▢" for _ in range(n)] for _ in range(n)]
        for i in range(n):
            board[n - population[i]][i] = "※"
        for row in board:
            self.print_v(" ".join(row), v=1)

    def __call__(self):
        generation = 1
        while not self.max_fitness in {p.fitness for p in self.populations}:
            self.print_v(f"=== Generation {generation} ===", end=" ")
            self.print_v("", v=2)
            self.genetic_queen()
            self.print_v(f"Maximum Fitness = {max({p.fitness for p in self.populations})}")
            generation += 1

        self.print_v("Solved in Generation {}!".format(generation - 1))
        for p in self.populations:
            if p.fitness == self.max_fitness:
                self.print_board(p.population)
                self.best_p = p
                break


if __name__ == "__main__":
    n = int(input("Enter Number of Queens= "))
    App(n=n, mutation_probability=0.9)()
