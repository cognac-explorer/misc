import datetime
from enum import Enum


class WeightExercise(Enum):
    SQUAT = "Squat"
    DEADLIFT = "Deadlift"
    BENCHPRESS = "Benchpress"


class Record:
    """Single record."""

    def __init__(self, exercise: WeightExercise, exercise_data: str, exercise_notes: str):
        self.exercise = exercise
        self.exercise_data = exercise_data
        self.exercise_notes = exercise_notes
        self.formula = self.get_formula()
        data = self.get_record_characteristics()
        self.best_set = data[0]
        self.max_weight = data[1]
        self.total_weight = data[2]

    def get_formula(self):
        return self.exercise_data.replace(":", "*").replace("-", " + ")

    def get_record_characteristics(self):
        # best set is defined by having max weight
        best_reps, max_weight, total_weight = 0, 0, 0
        for set in self.formula.split(" + "):
            sets, reps, weight = map(int, set.split("*"))
            total_weight += reps * weight
            if weight > max_weight:
                best_reps, max_weight = reps, weight

        return f"{best_reps}*{max_weight}", max_weight, total_weight

    def get_raw_data(self):
        return ("; ").join([self.exercise, self.exercise_data, self.exercise_notes])

    def to_gsheet(self, client, sheet_name):
        spreadsheet = client.open("test_tg_bot")
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.append_row(
            [
                # TODO: use user timezone
                datetime.datetime.now().isoformat(),
                self.exercise,
                self.formula,
                self.best_set,
                self.max_weight,
                self.total_weight,
                self.exercise_notes,
            ]
        )

    @classmethod
    def init_from_tg_bot(cls, tg_user_data):
        return cls(
            exercise=tg_user_data.get("exercise"),
            exercise_data=tg_user_data.get("exercise_data"),
            exercise_notes=tg_user_data.get("exercise_notes"),
        )
