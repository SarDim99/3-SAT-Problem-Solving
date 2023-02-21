import random
from typing import List, Tuple


def generate_3SAT(num_vars: int, num_clauses: int) -> List[Tuple[int, int, int]]:
    problem = []
    for _ in range(num_clauses):
        clause = random.sample(range(1, num_vars + 1), 3)
        clause = [random.choice([var, -var]) for var in clause]
        problem.append(clause)
    return problem

def count_satisfied(clauses, assignment):
        
        satisfied = 0
        for clause in clauses:
            for var in clause:
                if (var > 0 and assignment[abs(var)-1]) or (var < 0 and not assignment[abs(var)-1]):
                    satisfied += 1
                    break
        return satisfied

def GSAT(problem, maxTries, maxFlips):

    for i in range(maxTries):
        assignment = [random.choice([True, False]) for _ in range(len(problem))]

    for j in range(maxFlips):
        if count_satisfied(problem, assignment) == len(problem):
            return assignment
        else:
            best_var = None
            best_satisfied = -1
            for var in range(len(problem)):
                flipped_assignment = assignment[:]
                flipped_assignment[var] = not flipped_assignment[var]
                num_satisfied = count_satisfied(problem, flipped_assignment)
                if num_satisfied > best_satisfied:
                    best_var = var
                    best_satisfied = num_satisfied
            
            assignment[best_var] = not assignment[best_var]

    return None

def GSAT_RW(problem, maxTries, maxFlips, p):

    for i in range(maxTries):
       
        assignment = [random.choice([True, False]) for _ in range(len(problem))]

        for j in range(maxFlips):
            if count_satisfied(problem, assignment) == len(problem):
                return assignment
            else:
                best_var = None
                best_satisfied = -1
                false_clauses = []
                for clause in problem:
                    if all([(var > 0 and not assignment[abs(var)-1]) or (var < 0 and assignment[abs(var)-1]) for var in clause]):
                        false_clauses.extend(clause)
                for var in range(len(problem)):
                    flipped_assignment = assignment[:]
                    flipped_assignment[var] = not flipped_assignment[var]
                    num_satisfied = count_satisfied(problem, flipped_assignment)
                    if num_satisfied > best_satisfied:
                        best_var = var
                        best_satisfied = num_satisfied
                if random.random() < p:
                    var = random.choice(false_clauses)
                else:
                    var = best_var
                assignment[var] = not assignment[var]
    return None

def WSAT(problem, maxTries, maxFlips, p):
    
    def heuristic(clause, assignment):
       
        var_counts = [0 for _ in range(len(assignment))]
        for c in problem:
            if all([(var > 0 and not assignment[abs(var)-1]) or (var < 0 and assignment[abs(var)-1]) for var in c]):
                for var in c:
                    var_counts[abs(var)-1] += 1
        return var_counts.index(max(var_counts))

    for i in range(maxTries):
        assignment = [random.choice([True, False]) for _ in range(len(problem))]

        for j in range(maxFlips):
            if count_satisfied(problem, assignment) == len(problem):
                return assignment
            else:
               
                unsatisfied_clauses = [clause for clause in problem if all([(var > 0 and not assignment[abs(var)-1]) or (var < 0 and assignment[abs(var)-1]) for var in clause])]
                c = random.choice(unsatisfied_clauses)
                if random.random() < p:
                    x = random.choice(c)
                else:
                    x = heuristic(c, assignment)
                
                assignment[abs(x)-1] = not assignment[abs(x)-1]
    return None

def semi_greedy(problem, maxTries, maxFlips, k):
    
    def count_satisfied(clauses, assignment):
       
        satisfied = 0
        for clause in clauses:
            for var in clause:
                if (var > 0 and assignment[abs(var)-1]) or (var < 0 and not assignment[abs(var)-1]):
                    satisfied += 1
                    break
        return satisfied

    def heuristic(clause, assignment):
      
        var_counts = [0 for _ in range(len(assignment))]
        for c in problem:
            if all([(var > 0 and not assignment[abs(var)-1]) or (var < 0 and assignment[abs(var)-1]) for var in c]):
                for var in c:
                    var_counts[abs(var)-1] += 1
        return var_counts.index(max(var_counts))

    best_assignment = None
    best_satisfied = -1
    for i in range(maxTries):
        population = [[random.choice([True, False]) for _ in range(len(problem))] for _ in range(k)]
        for j in range(maxFlips):
            for assignment in population:
                if count_satisfied(problem, assignment) == len(problem):
                    return assignment
                else:
                    unsatisfied_clauses = [clause for clause in problem if all([(var > 0 and not assignment[abs(var)-1]) or (var < 0 and assignment[abs(var)-1]) for var in clause])]
                    c = random.choice(unsatisfied_clauses)
                    x = heuristic(c, assignment)
                    assignment[x] = not assignment[x]

            population.sort(key=lambda x: count_satisfied(problem, x), reverse=True)
            population = population[:k]
            if count_satisfied(problem, population[0]) > best_satisfied:
                best_assignment = population[0]
                best_satisfied = count_satisfied(problem, population[0])
    
    return best_assignment

if __name__=='__main__':
    num_problems = 10
    num_vars = 50
    num_clauses = 50
    maxTries = 100
    maxFlips = 100
    p = 0.5
    k = 5

    for i in range(num_problems):
        problem = generate_3SAT(num_vars, num_clauses)
        print("Solving problem ", i+1)
        print("GSAT: ")
        gsat_assignment = GSAT(problem[:], maxTries, maxFlips)
        if gsat_assignment:
            print("Solution found: ", gsat_assignment)
        else:
            print("No solution found!")
        print("\n")
        print("GSAT_RW: ")
        gsat_rw_assignment = GSAT_RW(problem[:], maxTries, maxFlips, p)
        if gsat_rw_assignment:
            print("Solution found: ", gsat_rw_assignment)
        else:
            print("No solution found.")
        print("\n")
        print("WSAT:")
        wsat_assignment = WSAT(problem[:], maxTries, maxFlips, p)
        if wsat_assignment:
            print("Solution found: ", wsat_assignment)
        else:
            print("No solution found.")
        print("\n")
        print("Semi-greedy: ")
        semi_greedy_assignment = semi_greedy(problem[:], maxTries, maxFlips, k)
        if semi_greedy_assignment:
            print("Solution found: ", semi_greedy_assignment)
        else:
            print("No solution found.")
        print("\n")
        input()
