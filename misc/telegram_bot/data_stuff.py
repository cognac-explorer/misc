import datetime
from enum import Enum

import gspread
from google.oauth2 import service_account


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
        self.best_set = self.get_best_set()

    def get_formula(self):
        return self.exercise_data.replace(":", "*").replace("-", " + ")

    def get_best_set(self):
        """Defined as max weight."""
        best_reps, best_weight = 0, 0
        for set in self.formula.split(" + "):
            sets, reps, weight = map(int, set.split("*"))
            if weight > best_weight:
                best_reps, best_weight = reps, weight
        return f"{best_reps}*{best_weight}"

    def get_raw_data(self):
        return ("; ").join([self.exercise, self.exercise_data, self.exercise_notes])

    def to_gsheet(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = service_account.Credentials.from_service_account_file(
            "cognac-explorer-tg-bot.json"
        )
        scoped_credentials = credentials.with_scopes(scope)
        client = gspread.authorize(scoped_credentials)
        spreadsheet = client.open("test_tg_bot")
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.append_row(
            [
                datetime.datetime.now().isoformat(),
                self.exercise,
                self.formula,
                self.best_set,
                self.exercise_notes,
                self.get_raw_data(),
            ]
        )

    @classmethod
    def init_from_tg_bot(cls, tg_user_data):
        return cls(
            exercise=tg_user_data.get("exercise"),
            exercise_data=tg_user_data.get("exercise_data"),
            exercise_notes=tg_user_data.get("exercise_notes"),
        )
