import pandas as pd
import sys
import os
from typing import Dict
from datetime import datetime

def process_excel(file_path: str) -> pd.DataFrame:
    """
    Charge un fichier Excel ou CSV, convertit et nettoie les colonnes, puis ajoute un classement (rang) des notes.

    Args:
        file_path (str): Chemin vers le fichier Excel ou CSV contenant les relevés de notes.

    Returns:
        pd.DataFrame: DataFrame transformé.

    Raises:
        RuntimeError: En cas d'erreur de lecture ou de transformation du fichier.
    """
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif ext == '.csv':
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Format de fichier non supporté: {ext}. Utilisez Excel (.xlsx/.xls) ou CSV.")

        # Uniformisation des noms de colonnes en minuscules
        df.columns = df.columns.str.lower()

        # Conversion des notes en numérique et remplissage des valeurs manquantes
        df['notes'] = pd.to_numeric(df['notes'], errors='coerce').fillna(0)

        # Nettoyage et conversion du numéro de téléphone
        df['numéro'] = df['numéro'].astype(str).str.replace(r"\s+", "", regex=True)
        #df['numéro'] = pd.to_numeric(df['numéro'], errors='coerce')

        # Classement des élèves (1 = meilleure note)
        df['rang'] = df['notes'].rank(method='dense', ascending=False).astype(int)

        return df
    except Exception as e:
        raise RuntimeError(f"Erreur lors du traitement du fichier '{file_path}': {e}") from e


def generate_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques générales des notes d'une classe.

    Args:
        df (pd.DataFrame): DataFrame traité par process_excel.

    Returns:
        pd.DataFrame: DataFrame à une ligne contenant les statistiques.

    Raises:
        RuntimeError: Si le calcul des statistiques échoue.
    """
    try:
        if 'notes' not in df.columns:
            raise KeyError("La colonne 'notes' est manquante dans le DataFrame.")
        stats: Dict[str, float] = {
            'note_max': df['notes'].max(),
            'note_min': df['notes'].min(),
            'note_moyenne': df['notes'].mean()
        }
        return pd.DataFrame([stats])
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la génération des statistiques: {e}") from e

# generate_stats(df: pd.DataFrame)['note_max'].iloc[0]
#generate_stats(df: pd.DataFrame)['note_min'].iloc[0]
#generate_stats(df: pd.DataFrame)['note_moyenne'].iloc[0]


def main(file_path: str) -> pd.DataFrame:
    """
    Fonction principale :
    - Prend en argument le chemin d'accès au fichier Excel ou CSV.
    - Traite le fichier et génère les statistiques.
    - Combine résultats et retourne le DataFrame final.
    - Enregistre le DataFrame combiné dans un fichier Excel dans le dossier 'Archives'.

    Args:
        file_path (str): Chemin vers le fichier Excel ou CSV des notes.

    Returns:
        pd.DataFrame: DataFrame fusionné.

    Exits:
        sys.exit(1) en cas d'erreur.
    """
    try:
        # Exécution des fonctions
        df_processed = process_excel(file_path)
        df_stats = generate_stats(df_processed)

        # Fusion des statistiques dans chaque ligne du relevé
        stats_dict = df_stats.iloc[0].to_dict()
        df_combined = df_processed.assign(**stats_dict)

        # Préparation du dossier d'archive
        archive_dir = os.path.join(os.getcwd(), 'Archives')
        os.makedirs(archive_dir, exist_ok=True)

        # Génération du nom de fichier avec timestamp
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        timestamp = datetime.now().strftime('%d-%m-%Y_%H%M%S')
        archive_filename = f"{base_name}_archived_{timestamp}.xlsx"
        archive_path = os.path.join(archive_dir, archive_filename)

        # Enregistrement du DataFrame combiné
        df_combined.to_excel(archive_path, index=False)
        print(f"Fichier archivé créé : {archive_path}")

        return df_combined
    except Exception as e:
        print(f"Erreur dans la fonction principale: {e}")
        sys.exit(1)