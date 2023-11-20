"""
    TDE - Otimizaçao de Sistemas Lineares
    NOME: Erick Lemmy dos Santos Oliveira
    PROF: Guilherme

    Construção de programa que resolve problemas de programação linear por SIMPLEX
"""
import copy
from fractions import Fraction
from rich.console import Console
from rich.table import Table

class SimplexOutput:
    UNIQUE_OPTIMAL = 0
    MULTIPLE_OPTIMAL = 1
    UNBOUNDED = 2
    DEGENERACY = 3
    INFEASIBLE = 4

class SimplexSolver:
    def __init__(self):
        self.tableau = None  # Instância de SimplexTableau

    def minimize(self, A, b, ineq, C):
        self.tableau = SimplexTableau(ineq, True)
        C = [-1 * value for value in C]
        self.tableau.initialize(A, b, C)

    def maximize(self, A, b, ineq, C):
        self.tableau = SimplexTableau(ineq, False)
        self.tableau.initialize(A, b, C)

    def solve(self):
        input("Press enter to continue...")
        while not self.is_optimal():
            pivot = self.tableau.find_pivot()

            if pivot[1] < 0:
                return None, SimplexOutput.UNBOUNDED  

            print(f"Iteração: {self.tableau.iteration_count}")
            print(f"Pivo: {self.tableau.tableau[pivot[1]][pivot[0]]}")
            print(f"Variavel entrando: {self.tableau.entering[pivot[0]]}")
            print(f"Variavel saindo: {self.tableau.departing[pivot[1]]}")
            self.tableau._print_tableau()
            print("Soluçao atual: \n")
            for chave, valor in self.get_current_solution().items():
                print(f"{chave}: {valor}")

            input("Press enter to continue...")
            self.tableau.step(pivot)

        solution = self.get_current_solution()
        result = self.determine_solution_type(solution)
        return solution, result

    def is_optimal(self):
        return all(x >= 0 for x in self.tableau.tableau[-1][:-1])

    def determine_solution_type(self, solution):
        if self.check_multiple_solutions(solution):
            return SimplexOutput.MULTIPLE_OPTIMAL

        if self.is_infeasible(solution):
            return SimplexOutput.INFEASIBLE

        is_degenerate = self.tableau.has_degeneracy or self.tableau.iteration_count >= 2 * len(self.tableau.A[0])
        if is_degenerate:
            return SimplexOutput.DEGENERACY

        return SimplexOutput.UNIQUE_OPTIMAL

    def is_infeasible(self, solution):
        return any(value != 0 for key, value in solution.items() if key.startswith("a"))  # a representa variáveis artificiais

    def check_multiple_solutions(self, solution):
        var_prefix = "x" if not self.tableau.is_minimize else "y"
        return any(value == 0 for key, value in solution.items() if key.startswith(var_prefix))


    def get_current_solution(self):
        solution = {}
        departing_mapping = {d: i for i, d in enumerate(self.tableau.departing)}

        for x in self.tableau.entering:
            if x != "b":
                departing_index = departing_mapping.get(x, -1)
                solution[x] = self.tableau.tableau[departing_index][-1] if departing_index >= 0 else 0

        solution["z"] = self.tableau.tableau[-1][-1]
        return solution


class SimplexTableau:
    def __init__(self, ineq, is_minimize):
        self.A = []
        self.C = []
        self.b = []
        self.ineq = ineq
        self.tableau = []
        self.entering = []
        self.departing = []
        self.iteration_count = 0
        self.has_degeneracy = False
        self.is_minimize = is_minimize

    def initialize(self, A, b, C):
        # Multiplica linha por -1 se ineq >= para transformar em <=
        for i, ineq in enumerate(self.ineq):
            if ineq == ">=":
                for j in range(len(A[i])):
                    A[i][j] *= -1 if self.is_minimize else 1
                b[i] *= -1 if self.is_minimize else 1

        self.A = [[Fraction(x) for x in a] for a in A]
        self.b = [Fraction(x) for x in b]
        self.C = [-Fraction(x) if self.is_minimize else -Fraction(x) for x in C]

        self.update_enter_depart(self.get_matrixAb())
        self.create_tableau()
        self.ineq = ["="] * len(self.b)
        self.update_enter_depart(self.tableau)

    def create_tableau(self):
        self.tableau = copy.deepcopy(self.A)
        slack_vars = self._generate_identity(len(self.tableau))
        for i in range(len(slack_vars)):
            self.tableau[i] += slack_vars[i]
            if self.ineq[i] == ">=":
                self.tableau[i].append(-1)
            elif ">=" in self.ineq:
                self.tableau[i].append(0)
            self.tableau[i] += [self.b[i]]


        self.tableau.append(self.C + [0] * (len(self.b) + 1))

    def find_pivot(self):
        enter_index = self.get_entering_var()
        depart_index = self.get_departing_var(enter_index)
        return [enter_index, depart_index]

    def step(self, pivot_index):
        j, i = pivot_index

        pivot = self.tableau[i][j]
        self.tableau[i] = [element / pivot for element in self.tableau[i]]
        for index, row in enumerate(self.tableau):
            if index != i:
                row_scale = [y * self.tableau[index][j] for y in self.tableau[i]]
                self.tableau[index] = [
                    x - y for x, y in zip(self.tableau[index], row_scale)
                ]

        self.departing[i] = self.entering[j]
        self.iteration_count += 1

    def update_enter_depart(self, matrix):
        self.entering = []
        self.departing = []

        for i in range(len(matrix[0])):
            if i < len(self.A[0]):
                prefix = "x" if not self.is_minimize else "y"
                self.entering.append(f"{prefix}{i+1}")
            elif i < len(matrix[0]) - 1:
                self.entering.append(f"s{i + 1 - len(self.A[0])}")
                self.departing.append(f"s{i + 1 - len(self.A[0])}")
            else:
                self.entering.append("b")

    def get_matrixAb(self):
        matrix = [row + [bi] for row, bi in zip(self.A, self.b)]
        return matrix

    def get_entering_var(self):
        bottom_row = self.tableau[-1]
        most_neg_ind = bottom_row.index(min(bottom_row))
        return most_neg_ind

    def get_departing_var(self, entering_index):
        # Verificação de unboundedness
        if all(row[entering_index] <= 0 for row in self.tableau[:-1]):
            return -1  # Indica uma solução ilimitada

        skip = 0
        min_ratio_index = -1
        min_ratio = 0
        for index, x in enumerate(self.tableau):
            if x[entering_index] != 0 and x[-1] / x[entering_index] > 0:
                skip = index
                min_ratio_index = index
                min_ratio = x[-1] / x[entering_index]
                break

        if min_ratio > 0:
            for index, x in enumerate(self.tableau):
                if index > skip and x[entering_index] > 0:
                    ratio = x[-1] / x[entering_index]
                    if min_ratio > ratio:
                        min_ratio = ratio
                        min_ratio_index = index
                    elif min_ratio == ratio:
                        self.has_degeneracy = True  # variável básica com a mesma razão

        if self.has_degeneracy:
            print("Possivel degeneração detectada!")
        return min_ratio_index

    def _generate_identity(self, n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def _print_tableau(self):
        console = Console()
        console.print("\nTabela Atual:", style="bold magenta")
        table = Table(show_header=True, header_style="bold green")
        for col in self.entering:
            table.add_column(col)

        for row in self.tableau:
            formatted_row = [f"{cell}" for cell in row]
            table.add_row(*formatted_row)
        console.print(table)


class UserInterface:
    def __init__(self):
        self.console = Console()
        self.instructions = "Bem-vindo ao solucionador Simplex!\nSiga as instruções para inserir os dados do problema."

    def display_instructions(self):
        self.console.print(self.instructions, style="bold blue")

    def input_minimize_maximize(self):
        while True:
            prob = input("\nDeseja minimizar ou maximizar o problema (Min/Max): ").upper()
            if prob in ["MIN", "MAX"]:
                return prob == "MIN"
            print("Entrada inválida. Por favor, insira 'Min' para minimizar ou 'Max' para maximizar.")

    def input_matrix(self):
        try:
            num_equations = int(input("Número de equações (linhas): "))
            num_variables = int(input("Número de variáveis (colunas): "))
            A, C, b, ineq = [], [], [], []

            for i in range(num_equations):
                row = list(map(float, input(f"Coeficientes da equação {i + 1} (separados por espaço): ").split()))
                if len(row) != num_variables:
                    raise ValueError("Número de coeficientes diferente do número de variáveis.")
                A.append(row)

            C = list(map(float, input("Coeficientes da função objetivo (separados por espaço): ").split()))
            if len(C) != num_variables:
                raise ValueError("Número de coeficientes diferente do número de variáveis.")

            b = list(map(float, input("Valores do vetor de constantes (separados por espaço): ").split()))
            if len(b) != num_equations:
                raise ValueError("Número de constantes diferente do número de equações.")

            ineq = input("Inequações (>=, <=, =) para cada linha: ").split()
            if len(ineq) != num_equations:
                raise ValueError("Número de inequações diferente do número de equações.")

            return A, C, b, ineq
        except ValueError as e:
            print(f"Erro de entrada: {e}")
            return None, None, None, None

    def print_solution(self, solution, result):
        result_messages = {
            SimplexOutput.UNIQUE_OPTIMAL: "A solução é única e ótima.",
            SimplexOutput.MULTIPLE_OPTIMAL: "Existem múltiplas soluções ótimas.",
            SimplexOutput.UNBOUNDED: "A solução é ilimitada (UNBOUNDED).",
            SimplexOutput.INFEASIBLE: "O problema é inviável (INFEASIBLE).",
            SimplexOutput.DEGENERACY: "O problema sofre de degeneração.",
        }

        message = result_messages.get(result, "Resultado desconhecido.")
        self.console.print(message, style="bold yellow")

        if solution:
            self.console.print("\nSolução Encontrada:", style="bold green")
            for var, value in solution.items():
                self.console.print(f"{var}: {value}", style="bold blue")
        else:
            self.console.print("Nenhuma solução foi encontrada.", style="bold red")

        self.console.print("\n")

    def print_tableau(self, tableau):
        self.console.print("\nSolução:", style="bold magenta")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Base", justify="right")
        for var in tableau.entering:
            table.add_column(var, justify="right")

        for i, row in enumerate(tableau.tableau):
            row_data = [tableau.departing[i]] if i < len(tableau.departing) else ["z"]
            # row_data.extend([f"{val:.2f}" for val in row])
            row_data.extend([f"{val}" for val in row])
            table.add_row(*row_data)

        self.console.print(table)

    def simplex_show(self, tableau, is_minimize, ineq=None):
        self.console.print(
            "\nFormulação do Problema de Programação Linear:", style="bold magenta"
        )
        objective = "Maximizar" if not is_minimize else "Minimizar"
        self.console.print(f"{objective} -> Z: ", style="bold green", end="")

        for i, value in enumerate(tableau.tableau[-1]):
            if not is_minimize:
                value *= -1
            sign = "+" if value >= 0 and i > 0 else "\b"
            if i < len(tableau.tableau[-1]) - 1:
                self.console.print(f"{sign} {value}x{i+1} ", end="")

        self.console.print("\nSujeito a:", style="bold green")
        for i, row in enumerate(tableau.tableau[:-1]):
            equation = " + ".join(f"{value}x{j+1}" for j, value in enumerate(row[:-1]))
            ineq = tableau.ineq if ineq is None else ineq
            self.console.print(f"{equation} {ineq[i]} {row[-1]}", style="dim")

        for i in range(len(tableau.tableau[0])):
            comma = "," if i < len(tableau.tableau) else ""
            self.console.print(f"  x{i+1}{comma}", style="bold", end="")
        self.console.print(" >= 0\n\n", style="bold")


def main():
    ui = UserInterface()
    ui.display_instructions()

    A, C, b, ineq = ui.input_matrix()
    if A is None or C is None or b is None or ineq is None:
        ui.console.print("Entrada inválida. O programa será encerrado.", style="bold red")
        return

    is_minimize = ui.input_minimize_maximize()
    solver = SimplexSolver()

    if is_minimize:
        solver.minimize(A, b, ineq, C)
        ui.simplex_show(solver.tableau, is_minimize, ineq)
        ui.simplex_show(solver.tableau, not is_minimize)
    else:
        solver.maximize(A, b, ineq, C)
        ui.simplex_show(solver.tableau, is_minimize, ineq)
        ui.simplex_show(solver.tableau, is_minimize)

    solution, result = solver.solve()
    ui.print_tableau(solver.tableau)
    ui.print_solution(solution, result)


if __name__ == "__main__":
    main()
