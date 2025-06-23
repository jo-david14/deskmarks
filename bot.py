import re

from reponses_possibles import (
    AverageNoteHandler,
    BestNoteHandler,
    WorstNoteHandler,
    UnknownQuestionHandler
)


def get_handler(path,message: str):
    message = message.lower()

    if re.search(r"\bmoyenne\b", message):
        return AverageNoteHandler(path)
    elif re.search(r"\bmeilleure note\b|\bnote maximale\b|\bnote la plus élevée\b", message):
        return BestNoteHandler(path)
    elif re.search(r"\bplus faible note\b|\bpire note\b|\bnote minimale\b", message):
        return WorstNoteHandler(path)
    else:
        return UnknownQuestionHandler(path)

