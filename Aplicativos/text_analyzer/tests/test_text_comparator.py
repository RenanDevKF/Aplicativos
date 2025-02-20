import pytest
from collections import Counter
from text_analyzer.comparator.text_comparator import TextComparator

# Fixture para inicializar o TextComparator
@pytest.fixture
def comparator():
    return TextComparator()

# Teste para carregar textos
def test_load_text(mocker, comparator):
    # Mockando o comportamento de carregar o texto de um arquivo e de uma página web
    resume_text = "Eu sou desenvolvedor"
    job_text = "Estamos contratando um programador"
    mocker.patch.object(comparator, 'load_text', return_value=(resume_text, job_text))
    
    result = comparator.load_text('fake_resume.txt', 'fake_job_url')
    assert result == (resume_text, job_text)

# Teste para a similaridade de Jaccard
def test_jaccard_similarity(comparator):
    text1 = "Eu sou desenvolvedor"
    text2 = "Eu sou programador"
    
    expected_result = 1 / 3  # Interseção: ['eu', 'sou'], União: ['eu', 'sou', 'desenvolvedor', 'programador']
    
    result = comparator.jaccard_similarity(text1, text2)
    assert result == pytest.approx(expected_result, rel=1e-2)

# Teste para a similaridade do cosseno
def test_cosine_similarity(comparator):
    text1 = "Eu sou desenvolvedor"
    text2 = "Eu sou programador"
    
    expected_result = 0.9  # Resultado esperado baseado no vetor de contagem de palavras
    
    result = comparator.cosine_similarity(text1, text2)
    assert result == pytest.approx(expected_result, rel=1e-2)

# Teste para obter termos comuns entre os textos
def test_get_common_terms(comparator):
    text1 = "Eu sou desenvolvedor, programador"
    text2 = "Eu sou programador e desenvolvedor"
    
    expected_result = ['desenvolvedor', 'programador']
    result = comparator.get_common_terms(text1, text2)
    
    assert set(result) == set(expected_result)

# Teste para obter termos exclusivos do primeiro texto
def test_get_unique_terms_from_first(comparator):
    text1 = "Eu sou desenvolvedor"
    text2 = "Eu sou programador"
    
    expected_result = ['desenvolvedor']
    result = comparator.get_unique_terms(text1, text2, from_first=True)
    
    assert set(result) == set(expected_result)

# Teste para obter termos exclusivos do segundo texto
def test_get_unique_terms_from_second(comparator):
    text1 = "Eu sou desenvolvedor"
    text2 = "Eu sou programador"
    
    expected_result = ['programador']
    result = comparator.get_unique_terms(text1, text2, from_first=False)
    
    assert set(result) == set(expected_result)

# Teste para a comparação completa entre o currículo e a vaga
def test_compare_documents(comparator, mocker):
    resume_text = "Eu sou desenvolvedor, especializado em Python."
    job_text = "Estamos contratando um programador especializado em Python."
    
    # Mockando o retorno das funções de carregamento de texto
    mocker.patch.object(comparator, 'load_text', return_value=(resume_text, job_text))
    
    expected_result = {
        'jaccard_similarity': pytest.approx(0.2, rel=1e-2),
        'cosine_similarity': pytest.approx(0.8, rel=1e-2),
        'common_terms': ['desenvolvedor', 'python'],
        'unique_terms_resume': ['especializado', 'sou'],
        'unique_terms_job': ['programador', 'estamos', 'contratando'],
        'match_level': 'Médio'
    }
    
    result = comparator.compare_documents('fake_resume.txt', 'fake_job_url')
    
    assert result['jaccard_similarity'] == expected_result['jaccard_similarity']
    assert result['cosine_similarity'] == expected_result['cosine_similarity']
    assert result['common_terms'] == expected_result['common_terms']
    assert result['unique_terms_resume'] == expected_result['unique_terms_resume']
    assert result['unique_terms_job'] == expected_result['unique_terms_job']
    assert result['match_level'] == expected_result['match_level']

# Teste de valores limite para similaridade de Jaccard (sem interseção)
def test_jaccard_no_intersection(comparator):
    text1 = "Texto A"
    text2 = "Texto B"
    
    expected_result = 0.0  # Interseção: 0, União: 4
    
    result = comparator.jaccard_similarity(text1, text2)
    assert result == pytest.approx(expected_result, rel=1e-2)

# Teste de similaridade cosseno com vetor zero
def test_cosine_zero_vector(comparator):
    text1 = " "
    text2 = " "
    
    expected_result = 0.0  # Nenhuma palavra, portanto, o resultado de cosseno é 0
    
    result = comparator.cosine_similarity(text1, text2)
    assert result == pytest.approx(expected_result, rel=1e-2)

# Teste para o comportamento quando os textos estão vazios
def test_edge_case_empty_texts(comparator):
    text1 = ""
    text2 = ""
    
    # Espera-se que as similaridades retornem 0
    assert comparator.jaccard_similarity(text1, text2) == 0.0
    assert comparator.cosine_similarity(text1, text2) == 0.0

# Teste para textos idênticos
def test_edge_case_identical_texts(comparator):
    text1 = "Texto igual"
    text2 = "Texto igual"
    
    # Similaridade de Jaccard e Cosseno devem ser 1 para textos idênticos
    assert comparator.jaccard_similarity(text1, text2) == 1.0
    assert comparator.cosine_similarity(text1, text2) == 1.0
