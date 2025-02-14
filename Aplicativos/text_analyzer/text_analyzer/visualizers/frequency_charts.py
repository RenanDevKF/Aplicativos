import matplotlib.pyplot as plt
import pandas as pd

class FrequencyVisualizer:
    def create_bar_chart(self, word_frequencies: dict, top_n: int = 10):
        """Cria um gráfico de barras das palavras mais frequentes"""
        df = pd.DataFrame(
            list(word_frequencies.items()),
            columns=['Palavra', 'Frequência']
        ).nlargest(top_n, 'Frequência')
        
        plt.figure(figsize=(10, 6))
        plt.bar(df['Palavra'], df['Frequência'])
        plt.xticks(rotation=45)
        plt.title(f'Top {top_n} Palavras Mais Frequentes')
        plt.tight_layout()
        return plt