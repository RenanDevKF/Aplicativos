# lotofacil_analyzer/data/processor.py
import pandas as pd
import os

def load_data():
    """
    Carrega o arquivo .xlsx fixo no projeto.
    """
    # Caminho para o arquivo .xlsx
    file_path = os.path.join(os.path.dirname(__file__), 'base_dados.xlsx')
    
    # Lê o arquivo
    df = pd.read_excel(file_path)
    return df