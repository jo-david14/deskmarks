import random
import pandas as pd
import getdata_diago as gd  # Données pré-calculées

# === CLASSE MÈRE ===
class QuestionHandler:
    def __init__(self):
        self.responses = []

    def get_response(self):
        return random.choice(self.responses)

    def can_handle(self, question: str) -> bool:
        raise NotImplementedError("Méthode non implémentée.")


# generate_stats(df: pd.DataFrame)['note_max'].iloc[0]
#generate_stats(df: pd.DataFrame)['note_min'].iloc[0]
#generate_stats(df: pd.DataFrame)['note_moyenne'].iloc[0]

# === CLASSE FILLE : Meilleure note ===
class BestNoteHandler(QuestionHandler):
    def __init__(self,path):
        super().__init__()
        
        self.responses = [
            f"La meilleure note est {gd.generate_stats(pd.read_excel(path))['note_max'].iloc[0]}.",
            f"La note la plus élevée est {gd.generate_stats(pd.read_excel(path))['note_max'].iloc[0]}.",
            f"Top score : {gd.generate_stats(pd.read_excel(path))['note_max'].iloc[0]} points."
        ]
        self.path = path

    def can_handle(self, question: str) -> bool:
        keywords = ["meilleure note", "note la plus élevée", "note maximale", "meilleur score"]
        return any(keyword in question.lower() for keyword in keywords)
    


# === CLASSE FILLE : Plus faible note ===
class WorstNoteHandler(QuestionHandler):
    def __init__(self,path):
        super().__init__()
        self.responses = [
            f"La plus faible note est {gd.generate_stats(pd.read_excel(path))['note_min'].iloc[0]}.",
            f"La note la plus basse est {gd.generate_stats(pd.read_excel(path))['note_min'].iloc[0]}.",
            f"Le plus petit score est {gd.generate_stats(pd.read_excel(path))['note_min'].iloc[0]} points."
        ]
        self.path = path

    def can_handle(self, question: str) -> bool:
        keywords = ["plus faible note", "note minimale", "note la plus basse", "pire note"]
        return any(keyword in question.lower() for keyword in keywords)


# === CLASSE FILLE : Moyenne des notes ===
class AverageNoteHandler(QuestionHandler):
    def __init__(self,path):
        super().__init__()
        self.responses = [
            f"La moyenne des notes est {gd.generate_stats(pd.read_excel(path))['note_moyenne'].iloc[0]}.",
            f"La moyenne générale est de {gd.generate_stats(pd.read_excel(path))['note_moyenne'].iloc[0]}.",
            f"En moyenne, les élèves ont eu {gd.generate_stats(pd.read_excel(path))['note_moyenne'].iloc[0]}."
        ]
        self.path = path

    def can_handle(self, question: str) -> bool:
        keywords = ["moyenne", "note moyenne", "score moyen"]
        return any(keyword in question.lower() for keyword in keywords)


# === CLASSE FILLE : Question inconnue ===
class UnknownQuestionHandler(QuestionHandler):
    def __init__(self,path):
        super().__init__()
        self.responses = ["Je suis un assistant de base. Pour des questions plus complexes, consultez la documentation ou contactez le support.",
            "Essaie de poser la question autrement, s'il te plaît.",
            "Désolé, je ne comprends pas encore cette question.",
            "Tu peux reformuler ?",
            "Je n'ai pas bien saisi.",
            "Pose une autre question en rapport avec les notes."
        ]
        self.path = path

    def can_handle(self, question: str) -> bool:
        return True  # Toujours prêt si aucun autre ne correspond
