from enum import Enum


class Exercise(Enum):
    squat = "Squat"
    deadlift = "Deadlift"
    benchpress = "Benchpress"
    dips = "Dips"
    pull_ups = "Pull-Ups"
    run = "Run"


# gsheet list index: list of exercises
config = {
    Exercise.squat: 0, 
    Exercise.deadlift: 0, 
    Exercise.benchpress: 0,
    Exercise.dips: 1,
    Exercise.pull_ups: 1,
    Exercise.run: 2
}

tg_reply_keyboard = [
    [Exercise.squat, Exercise.deadlift ,Exercise.benchpress ],
    [Exercise.dips, Exercise.pull_ups, Exercise.run],
]