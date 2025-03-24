# lotofacil_analyzer/analyzers/gap.py
from .base import AnalisadorBase
import pandas as pd
import numpy as np

class AnalisadorAtraso(AnalisadorBase):
    """Analisador de atraso de números (análise 2)"""
    
    def analisar(self):
        """Analisa há quanto tempo cada número não é sorteado"""
        # Verifica se o DataFrame foi carregado corretamente
        if self.df is None or self.df.empty:
            return {"erro": "DataFrame vazio ou não carregado. Verifique os dados fornecidos."}
        
        # Debug: Exibe informações sobre o DataFrame
        print("\n[DEBUG] Informações do DataFrame:")
        print("Colunas disponíveis:", list(self.df.columns))
        print("Total de sorteios:", len(self.df))
        if not self.df.empty:
            print("Primeira linha - Concurso:", self.df.iloc[0]['Concurso'])
            print("Primeira linha - Números:", self.df.iloc[0]['numeros'])
        
        try:
            # Ordena os sorteios do mais recente para o mais antigo
            sorteios_ordenados = self.df.sort_values('Concurso', ascending=False)
            
            # Inicializa o dicionário de atrasos
            atrasos_atuais = {i: 0 for i in range(1, 26)}
            historico_atrasos = {i: [] for i in range(1, 26)}
            ultimo_sorteio = {i: None for i in range(1, 26)}
            
            # Percorre os sorteios e calcula os atrasos
            for idx, row in sorteios_ordenados.iterrows():
                concurso = row['Concurso']
                numeros = row['numeros']
                
                # Verifica se 'numeros' é uma lista válida
                if not isinstance(numeros, list) or len(numeros) != 15:
                    print(f"[ERRO] Linha {idx} tem números inválidos: {numeros}")
                    continue
                
                # Atualiza o atraso para cada número
                for num in range(1, 26):
                    if num in numeros:
                        # Se o número foi sorteado, registra o atraso atual e zera
                        if atrasos_atuais[num] > 0:
                            historico_atrasos[num].append(atrasos_atuais[num])
                        atrasos_atuais[num] = 0
                        ultimo_sorteio[num] = concurso
                    else:
                        # Se não foi sorteado, incrementa o atraso
                        atrasos_atuais[num] += 1
            
            # Calcula estatísticas dos atrasos históricos
            estatisticas_atrasos = {}
            for num in range(1, 26):
                if historico_atrasos[num]:
                    estatisticas_atrasos[num] = {
                        'media': float(np.mean(historico_atrasos[num])),
                        'maximo': int(np.max(historico_atrasos[num])),
                        'minimo': int(np.min(historico_atrasos[num])),
                        'atual': int(atrasos_atuais[num]),
                        'ultimo_sorteio': ultimo_sorteio[num] if ultimo_sorteio[num] is not None else "Nunca"
                    }
                else:
                    estatisticas_atrasos[num] = {
                        'media': 0.0,
                        'maximo': 0,
                        'minimo': 0,
                        'atual': int(atrasos_atuais[num]),
                        'ultimo_sorteio': "Nunca"
                    }
            
            # Ordena os números por atraso atual (do maior para o menor)
            numeros_por_atraso = sorted(
                [(num, atraso) for num, atraso in atrasos_atuais.items()],
                key=lambda x: x[1],
                reverse=True
            )
            
            self.resultados = {
                'atrasos_atuais': atrasos_atuais,
                'estatisticas': estatisticas_atrasos,
                'ranking_atrasos': numeros_por_atraso,
                'maior_atraso_atual': numeros_por_atraso[0] if numeros_por_atraso else None,
                'menor_atraso_atual': numeros_por_atraso[-1] if numeros_por_atraso else None,
                'total_sorteios': len(self.df)
            }
            
            print("[DEBUG] Análise de atraso concluída com sucesso")
            return self.resultados
            
        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha na análise de atraso: {str(e)}")
            return {"erro": f"Falha na análise: {str(e)}"}