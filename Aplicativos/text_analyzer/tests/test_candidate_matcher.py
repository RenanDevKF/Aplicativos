import pytest
from unittest.mock import MagicMock
from text_analyzer.job_matcher.candidate_matcher import CandidateMatcher

# Fixture para inicializar o CandidateMatcher
@pytest.fixture
def candidate_matcher():
    # Supondo que o caminho para o currículo seja "fake_curriculum.txt"
    return CandidateMatcher("fake_curriculum.txt")

# Mockando as dependências externas, como read_file e fetch_web_text
@pytest.fixture
def mock_dependencies(mocker):
    # Mockando o método que lê o currículo
    mocker.patch('src.matcher.candidate_matcher.read_file', return_value="Eu sou um desenvolvedor Python.")
    
    # Mockando o fetch_web_text para obter o conteúdo da vaga
    mocker.patch('src.matcher.candidate_matcher.fetch_web_text', return_value="Estamos buscando um desenvolvedor Python com experiência em Django.")
    
    return mocker

# Teste para verificar a análise de uma vaga
def test_analisar_vaga(mock_dependencies, candidate_matcher):
    # Realiza a análise da vaga
    job_url = "http://fakejob.com"
    resultado = candidate_matcher.analisar_vaga(job_url)
    
    # Verificando se o resultado contém as chaves corretas
    assert 'compatibilidade_geral' in resultado
    assert 'nivel_match' in resultado
    assert 'habilidades_correspondentes' in resultado
    assert 'requisitos_faltantes' in resultado
    assert 'diferenciais_candidato' in resultado
    assert 'recomendacoes' in resultado

    # Verificando se as recomendações são geradas corretamente
    assert isinstance(resultado['recomendacoes'], list)

# Teste para verificar a função de recomendação de melhorias no currículo
def test_recomendar_melhorias_curriculo(mock_dependencies, candidate_matcher):
    # Lista de vagas para análise
    vagas_alvo = ["http://fakejob1.com", "http://fakejob2.com"]
    
    # Chamando o método recomendar_melhorias_curriculo
    resultado = candidate_matcher.recomendar_melhorias_curriculo(vagas_alvo)
    
    # Verificando se as chaves certas estão no resultado
    assert 'habilidades_prioritarias' in resultado
    assert 'sugestao_melhoria' in resultado
    assert isinstance(resultado['habilidades_prioritarias'], list)
    assert isinstance(resultado['sugestao_melhoria'], str)

# Teste para a classificação das vagas
def test_classificar_vagas(mock_dependencies, candidate_matcher):
    # Lista de vagas para classificação
    lista_vagas = [
        {'id': 1, 'titulo': 'Vaga 1', 'url': 'http://fakejob1.com'},
        {'id': 2, 'titulo': 'Vaga 2', 'url': 'http://fakejob2.com'}
    ]
    
    # Chamando o método classificar_vagas
    resultados = candidate_matcher.classificar_vagas(lista_vagas)
    
    # Verificando se a lista de resultados está ordenada corretamente
    assert len(resultados) == 2
    assert resultados[0]['id_vaga'] == 1  # Vaga mais compatível deve estar primeiro
    assert resultados[1]['id_vaga'] == 2

# Teste para verificar o funcionamento do método _gerar_recomendacoes
def test_gerar_recomendacoes(mock_dependencies, candidate_matcher):
    # Resultados simulados de análise
    resultado = {
        'nivel_match': 'Alto',
        'habilidades_correspondentes': ['Python', 'Django'],
        'requisitos_faltantes': [],
        'diferenciais_candidato': ['Flask']
    }
    
    # Chamando o método privado para gerar recomendações
    recomendacoes = candidate_matcher._gerar_recomendacoes(resultado)
    
    # Verificando se a recomendação está correta
    assert isinstance(recomendacoes, list)
    assert "Seu perfil é altamente compatível com esta vaga" in recomendacoes[0]

# Teste para verificar o comportamento quando as habilidades correspondentes estão ausentes
def test_gerar_recomendacoes_sem_habilidades(mock_dependencies, candidate_matcher):
    # Resultados simulados de análise sem habilidades correspondentes
    resultado = {
        'nivel_match': 'Baixo',
        'habilidades_correspondentes': [],
        'requisitos_faltantes': ['Django', 'Flask'],
        'diferenciais_candidato': ['Python']
    }
    
    # Chamando o método privado para gerar recomendações
    recomendacoes = candidate_matcher._gerar_recomendacoes(resultado)
    
    # Verificando se as recomendações estão de acordo com a falta de habilidades
    assert "Destaque suas habilidades compatíveis" in recomendacoes[0]
    assert "Para aumentar sua compatibilidade" in recomendacoes[1]

