import os
from text_analyzer.core.analyzer import TextAnalyzer
from text_analyzer.visualizers.word_cloud import WordCloudGenerator
from text_analyzer.visualizers.frequency_charts import FrequencyVisualizer
from text_analyzer.utils.file_handler import read_file

def analisar_arquivo_unico(caminho_arquivo: str, nome_saida: str = None):
    """
    Analisa um único arquivo de texto
    """
    # Criar instâncias das classes necessárias
    analyzer = TextAnalyzer()
    wc_generator = WordCloudGenerator()
    viz = FrequencyVisualizer()

    # Definir nome de saída se não fornecido
    if nome_saida is None:
        nome_saida = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    try:
        # Ler e analisar o arquivo
        print(f"Iniciando análise do arquivo: {caminho_arquivo}")  # Print para iniciar a análise
        texto = read_file(caminho_arquivo)
        analyzer.load_text(texto)

        # Imprimir estatísticas básicas
        print(f"\nAnálise do arquivo: {caminho_arquivo}")
        print(f"Total de palavras únicas: {len(analyzer.word_frequencies)}")
        
        # Mostrar top 10 palavras
        print("\nPalavras mais frequentes:")
        sorted_words = sorted(analyzer.word_frequencies.items(), 
                            key=lambda x: x[1], 
                            reverse=True)
        for palavra, frequencia in sorted_words[:10]:
            print(f"- {palavra}: {frequencia} vezes")

        # Gerar visualizações
        print(f"Gerando visualizações para {nome_saida}...")  # Print indicando que as visualizações estão sendo geradas
        # Nuvem de palavras
        wordcloud = wc_generator.generate(analyzer.word_frequencies)
        wordcloud.to_file(f'{nome_saida}_nuvem.png')
        print(f"Nuvem de palavras salva como {nome_saida}_nuvem.png")

        # Gráfico de barras
        plt = viz.create_bar_chart(analyzer.word_frequencies, top_n=10)
        plt.savefig(f'{nome_saida}_frequencia.png')
        print(f"Gráfico de frequência salvo como {nome_saida}_frequencia.png")
        plt.close()

        return analyzer.word_frequencies

    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
        return None

def analisar_pasta(caminho_pasta: str, extensoes=['.txt']):
    """
    Analisa todos os arquivos de texto em uma pasta
    """
    frequencias_totais = {}
    arquivos_processados = 0

    # Percorrer todos os arquivos na pasta
    print(f"Iniciando a análise da pasta: {caminho_pasta}")  # Print para indicar que a pasta está sendo analisada
    for arquivo in os.listdir(caminho_pasta):
        if any(arquivo.endswith(ext) for ext in extensoes):
            caminho_completo = os.path.join(caminho_pasta, arquivo)
            print(f"Processando o arquivo: {caminho_completo}")  # Print para mostrar o arquivo sendo processado
            frequencias = analisar_arquivo_unico(caminho_completo)
            
            if frequencias:
                # Combinar frequências
                for palavra, freq in frequencias.items():
                    frequencias_totais[palavra] = frequencias_totais.get(palavra, 0) + freq
                arquivos_processados += 1

    # Gerar análise consolidada se houver arquivos processados
    if arquivos_processados > 0:
        print(f"\nAnálise consolidada de {arquivos_processados} arquivos:")
        
        # Criar visualizações consolidadas
        wc_generator = WordCloudGenerator()
        viz = FrequencyVisualizer()

        # Nuvem de palavras consolidada
        wordcloud = wc_generator.generate(frequencias_totais)
        wordcloud.to_file('analise_consolidada_nuvem.png')
        print("Nuvem de palavras consolidada salva como analise_consolidada_nuvem.png")

        # Gráfico de frequência consolidado
        plt = viz.create_bar_chart(frequencias_totais, top_n=15)
        plt.savefig('analise_consolidada_frequencia.png')
        print("Gráfico de frequência consolidado salvo como analise_consolidada_frequencia.png")
        plt.close()

def main():
    # Caminho do arquivo único que você deseja analisar
    arquivo_unico = "test_files/curriculo_test_ramiro.pdf"  # Caminho relativo ou absoluto para o arquivo
    if os.path.exists(arquivo_unico):
        print(f"Analisando arquivo único: {arquivo_unico}")
        analisar_arquivo_unico(arquivo_unico)
    else:
        print(f"Arquivo não encontrado: {arquivo_unico}")
    
    # Caminho da pasta onde você tem arquivos para analisar
    pasta_textos = "test_files"  # Caminho relativo ou absoluto para a pasta
    if os.path.exists(pasta_textos):
        print(f"Analisando pasta: {pasta_textos}")
        analisar_pasta(pasta_textos, extensoes=['.txt', '.pdf'])  # Incluindo .pdf nas extensões a serem analisadas
    else:
        print(f"Pasta não encontrada: {pasta_textos}")


if __name__ == "__main__":
    main()
