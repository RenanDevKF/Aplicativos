import matplotlib.pyplot as plt
import pandas as pd

class FrequencyVisualizer:
    """
    Classe para visualizar a frequência das palavras em um gráfico de barras.
    """
    def create_bar_chart(self, word_frequencies: dict, top_n: int = 10):
        """
        Cria um gráfico de barras para as palavras mais frequentes.

        Parâmetros:
        -----------
        word_frequencies : dict
            Um dicionário onde as chaves são palavras e os valores são as frequências.
        top_n : int, opcional (padrão: 10)
            Número máximo de palavras a serem exibidas no gráfico.

        Retorno:
        --------
        matplotlib.pyplot
            Retorna o objeto `plt` contendo o gráfico, que pode ser exibido ou salvo.
        
        Exemplo de uso:
        --------------
        viz = FrequencyVisualizer()
        plt = viz.create_bar_chart({'Python': 10, 'Código': 5, 'Dados': 8})
        plt.show()
        """
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
    