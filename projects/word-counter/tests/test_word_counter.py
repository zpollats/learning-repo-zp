import pytest
from word_counter import WordCounter

@pytest.fixture
def basic_temp_file(tmp_path):
    test_file = tmp_path / 'basic_test_file.txt'
    test_file.write_text(
        "python is cool\n"
        "python is awesome\n"
        "python is the best language\n"
        "coding is neat\n"
    )
    return str(test_file)

@pytest.fixture
def upper_temp_file(tmp_path):
    test_file = tmp_path / 'upper_test_file.txt'
    test_file.write_text("PYTHON Python python")
    return str(test_file)

@pytest.fixture
def punct_temp_file(tmp_path):
    test_file = tmp_path / 'punct_test_file.txt'
    test_file.write_text("Hello? Hello! Hello, Hello. ?Hello?!")
    return str(test_file)

@pytest.fixture
def empty_file(tmp_path):
    test_file = tmp_path / 'empty_file.txt'
    test_file.write_text("")
    return str(test_file)

@pytest.fixture
def stopwords_temp_file(tmp_path):
    test_file = tmp_path / 'stopwords_temp_file.txt'
    test_file.write_text("the cat and the dog and the pig and the cat and who are you")
    return str(test_file)

def test_top_words_basic(basic_temp_file):
    counter = WordCounter(basic_temp_file)
    counts = counter.top_words(3)
    assert len(counts) == 3
    assert counts[0] == ('python', 3)
    assert all(isinstance(count, tuple) for count in counts)

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        WordCounter('no_file.txt')

def test_case_insensitive(upper_temp_file):
    counter = WordCounter(upper_temp_file)
    counts = counter.top_words()
    assert counts[0] == ('python', 3)

def test_punctuation_removal(punct_temp_file):
    counter = WordCounter(punct_temp_file)
    counts = counter.top_words()
    assert counts[0] == ('hello', 5)

def test_empty_file(empty_file):
    counter = WordCounter(empty_file)
    assert counter.top_words() == []

def test_stopwords_filtered(stopwords_temp_file):
    counter = WordCounter(stopwords_temp_file)
    counts = counter.top_words()
    words = [word for word, _ in counts]
    assert counts[0] == ('cat', 2)
    assert 'the' not in words
    assert 'and' not in words
    assert 'are' not in words
    