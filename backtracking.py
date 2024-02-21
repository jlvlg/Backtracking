import pandas as pd
from time import time


class Backtracking:
    def __init__(self, filePath):
        with open(filePath, encoding="cp1252") as f:
            self.data = pd.DataFrame(
                {
                    x.split(":")[0]: {
                        y.split("=")[0]: int(y.split("=")[1])
                        for y in x.split(":")[1].split(";")[:-1]
                    }
                    for x in f.read().split("\n")[:-1]
                },
            ).fillna(0)

    def run(self, *args):
        while True:
            try:
                self.timer = time() + 3
                return self.backtracking(
                    pd.DataFrame({x: [] for x in self.data}, dtype="string"),
                    self.data.copy(),
                )
            except TimeoutError:
                pass

    def backtracking(self, solution: pd.DataFrame, data: pd.DataFrame):
        if time() > self.timer:
            raise TimeoutError()
        if self.is_solved(data):
            return solution
        column = self.select_column(solution)
        for name in data.loc[data[column] > 0, column].sample(frac=1).index:
            solution.loc[solution[column].count(), column] = name
            data.loc[name, column] -= 1
            if self.infer(solution):
                result = self.backtracking(solution, data)
                if result is not False:
                    return result
            solution.loc[solution[column].count() - 1, column] = pd.NA
            data.loc[name, column] += 1
        return False

    def is_solved(self, data: pd.DataFrame):
        return (data == 0).all().all()

    def select_column(self, solution: pd.DataFrame):
        return solution.count().idxmin()

    @staticmethod
    def infer(solution: pd.DataFrame):
        return solution.apply(lambda x: x.dropna().is_unique, axis=1).all()
