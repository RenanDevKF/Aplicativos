import argparse
import os
import json
from audio_processor.extractor import AudioExtractor
from audio_processor.analyzer import AudioAnalyzer
from audio_processor.converter import AudioToTextConverter
from language_tools.vocabulary import VocabularyAnalyzer
from language_tools.pronunciation import PronunciationAnalyzer
from study_materials.exercises import ExerciseGenerator
from utils.visualizer import AudioVisualizer
from typing import Dict, Any

def main():
    """Função principal que implementa a interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description='Processador de Áudio para Estudos de Linguagem'
    )
    
    # Argumentos obrigatórios
    parser.add_argument(
        'audio_path', 
        help='Caminho para o arquivo de áudio a ser analisado'
    )
    
    # Argumentos opcionais
    parser.add_argument(
        '--language', '-l',
        default='en-US',
        help='Código do idioma (ex: en-US, pt-BR, es-ES)'
    )
    
    parser.add_argument(
        '--reference', '-r',
        help='Caminho para arquivo de áudio de referência (opcional)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Caminho para salvar resultados (opcional)'
    )
    
    parser.add_argument(
        '--visualize', '-v',
        action='store_true',
        help='Gerar visualizações dos resultados'
    )
    
    parser.add_argument(
        '--exercises', '-e',
        action='store_true',
        help='Gerar exercícios baseados na análise'
    )
    
    parser.add_argument(
        '--difficulty', '-d',
        choices=['fácil', 'médio', 'difícil'],
        default='médio',
        help='Nível de dificuldade dos exercícios gerados'
    )
    
    # Analisar argumentos
    args = parser.parse_args()
    
    # Verificar se o arquivo existe
    if not os.path.isfile(args.audio_path):
        print(f"Erro: arquivo de áudio não encontrado: {args.audio_path}")
        return
    
    # Verificar arquivo de referência se fornecido
    if args.reference and not os.path.isfile(args.reference):
        print(f"Erro: arquivo de referência não encontrado: {args.reference}")
        return
    
    # Processar o áudio
    try:
        results = process_audio(
            args.audio_path,
            args.language,
            args.reference,
            args.visualize,
            args.exercises,
            args.difficulty
        )
        
        # Salvar resultados se caminho de saída for fornecido
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Resultados salvos em: {args.output}")
        else:
            # Exibir resultados resumidos
            display_summary(results)
    
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        import traceback
        traceback.print_exc()
        
def process_audio(
    audio_path: str,
    language: str,
    reference_path: str = None,
    visualize: bool = False,
    generate_exercises: bool = False,
    difficulty: str = 'médio'
) -> Dict[str, Any]:
    """
    Processa um arquivo de áudio e realiza várias análises linguísticas.
    
    Args:
        audio_path: Caminho para o arquivo de áudio a ser analisado
        language: Código do idioma do áudio (ex: en-US, pt-BR)
        reference_path: Caminho opcional para um áudio de referência para comparação
        visualize: Se True, gera visualizações dos resultados
        generate_exercises: Se True, gera exercícios baseados na análise
        difficulty: Nível de dificuldade dos exercícios ('fácil', 'médio', 'difícil')
        
    Returns:
        Dicionário contendo os resultados da análise
    """
    print(f"Processando arquivo: {audio_path}")
    print(f"Idioma: {language}")
    
    # Inicializar componentes
    extractor = AudioExtractor()
    analyzer = AudioAnalyzer()
    converter = AudioToTextConverter()
    vocab_analyzer = VocabularyAnalyzer()
    
    # Extrair características do áudio
    print("Extraindo características do áudio...")
    audio_features = extractor.extract_features(audio_path)
    
    # Converter áudio para texto
    print("Convertendo áudio para texto...")
    text = converter.convert(audio_path, language)
    
    # Analisar características do áudio
    print("Analisando características do áudio...")
    audio_analysis = analyzer.analyze(audio_features, language)
    
    # Analisar vocabulário
    print("Analisando vocabulário...")
    vocab_analysis = vocab_analyzer.analyze(text, language)
    
    # Resultado inicial
    results = {
        "metadata": {
            "arquivo": os.path.basename(audio_path),
            "idioma": language,
            "duração": audio_features.get("duration", 0)
        },
        "transcrição": text,
        "análise_áudio": audio_analysis,
        "análise_vocabulário": vocab_analysis
    }
    
    # Comparar com referência se fornecida
    if reference_path:
        print(f"Comparando com referência: {reference_path}")
        pronunciation_analyzer = PronunciationAnalyzer()
        
        # Extrair características do áudio de referência
        ref_features = extractor.extract_features(reference_path)
        
        # Comparar pronúncia
        pronunciation_results = pronunciation_analyzer.compare(
            audio_features, 
            ref_features,
            language
        )
        
        results["comparação_pronúncia"] = pronunciation_results
    
    # Gerar visualizações se solicitado
    if visualize:
        print("Gerando visualizações...")
        visualizer = AudioVisualizer()
        
        # Determinar pasta de saída para visualizações
        output_dir = os.path.dirname(audio_path)
        base_filename = os.path.splitext(os.path.basename(audio_path))[0]
        
        # Gerar visualizações
        visualization_paths = visualizer.generate_visualizations(
            audio_features,
            output_dir,
            base_filename
        )
        
        results["visualizações"] = visualization_paths
    
    # Gerar exercícios se solicitado
    if generate_exercises:
        print(f"Gerando exercícios (dificuldade: {difficulty})...")
        exercise_generator = ExerciseGenerator()
        
        # Mapear dificuldade para valor numérico
        difficulty_map = {
            'fácil': 1,
            'médio': 2,
            'difícil': 3
        }
        
        # Gerar exercícios
        exercises = exercise_generator.generate(
            text,
            vocab_analysis,
            audio_analysis,
            language,
            difficulty_map.get(difficulty, 2)
        )
        
        results["exercícios"] = exercises
    
    print("Processamento concluído com sucesso!")
    return results


def display_summary(results: Dict[str, Any]) -> None:
    """
    Exibe um resumo dos resultados da análise no terminal.
    
    Args:
        results: Dicionário contendo os resultados da análise
    """
    print("\n" + "="*60)
    print(f"RESUMO DA ANÁLISE")
    print("="*60)
    
    # Metadados
    print(f"\nArquivo: {results['metadata']['arquivo']}")
    print(f"Idioma: {results['metadata']['idioma']}")
    print(f"Duração: {results['metadata']['duração']:.2f} segundos")
    
    # Transcrição (primeiras 150 caracteres)
    text = results.get('transcrição', '')
    if text:
        print(f"\nTranscrição (início): {text[:150]}{'...' if len(text) > 150 else ''}")
    
    # Estatísticas de áudio
    audio_analysis = results.get('análise_áudio', {})
    if audio_analysis:
        print("\nEstatísticas de áudio:")
        print(f"- Ritmo médio: {audio_analysis.get('ritmo_médio', 'N/A')} palavras/min")
        print(f"- Pausas: {audio_analysis.get('número_pausas', 'N/A')}")
        print(f"- Clareza: {audio_analysis.get('clareza', 'N/A')}/10")
    
    # Estatísticas de vocabulário
    vocab_analysis = results.get('análise_vocabulário', {})
    if vocab_analysis:
        print("\nEstatísticas de vocabulário:")
        print(f"- Total de palavras: {vocab_analysis.get('total_palavras', 'N/A')}")
        print(f"- Palavras únicas: {vocab_analysis.get('palavras_únicas', 'N/A')}")
        print(f"- Nível de complexidade: {vocab_analysis.get('nível_complexidade', 'N/A')}/10")
        
        # Palavras mais frequentes
        if 'palavras_frequentes' in vocab_analysis and vocab_analysis['palavras_frequentes']:
            print("\nPalavras mais frequentes:")
            for word_info in vocab_analysis['palavras_frequentes'][:5]:
                print(f"- {word_info['palavra']}: {word_info['frequência']} ocorrências")
    
    # Comparação de pronúncia
    pronunciation = results.get('comparação_pronúncia', {})
    if pronunciation:
        print("\nComparação de pronúncia:")
        print(f"- Pontuação geral: {pronunciation.get('pontuação_geral', 'N/A')}/100")
        print(f"- Precisão fonética: {pronunciation.get('precisão_fonética', 'N/A')}/10")
        
        # Áreas para melhoria
        if 'áreas_melhoria' in pronunciation and pronunciation['áreas_melhoria']:
            print("\nÁreas para melhoria:")
            for area in pronunciation['áreas_melhoria'][:3]:
                print(f"- {area['nome']}: {area['descrição']}")
    
    # Exercícios
    exercises = results.get('exercícios', {})
    if exercises:
        print(f"\nExercícios gerados: {len(exercises.get('itens', []))}")
        print(f"Dificuldade: {exercises.get('dificuldade', 'N/A')}")
    
    # Visualizações
    visualizations = results.get('visualizações', [])
    if visualizations:
        print(f"\nVisualizações geradas: {len(visualizations)}")
        for viz_path in visualizations[:3]:
            print(f"- {viz_path}")
    
    print("\n" + "="*60)
    print("Para ver resultados completos, use a opção --output para salvar em arquivo")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()