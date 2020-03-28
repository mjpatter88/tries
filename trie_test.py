import pytest

from trie import Trie

def test_a():
    word_list = ['a']
    t = Trie(word_list)

    assert t.root.nodes['a'].terminal == True

def test_duplicates_raise_assertion_error():
    word_list = ['a', 'a']

    with pytest.raises(AssertionError):
        t = Trie(word_list)

def test_a_add_additional():
    word_list = ['a', 'add', 'additional']
    t = Trie(word_list)

    assert t.root.nodes['a'].terminal == True
    assert t.root.nodes['a'].nodes['d'].terminal == False
    assert t.root.nodes['a'].nodes['d'].nodes['d'].terminal == True

    assert set(t.get_words()) == set(word_list)

def test_word_list():
    word_list = []
    with open('words_small.txt') as in_file:
        lines = [line.strip() for line in in_file.readlines()]
    word_list.extend(lines)

    t = Trie(word_list)

    trie_word_list = t.get_words()

    assert len(trie_word_list) == len(word_list)

def test_autocomplete():
    word_list = ['a', 'add', 'additional']
    t = Trie(word_list)

    completes = t.get_autocomplete('a', 10)
    print(completes)
    assert len(completes) == 3
    assert 'a' in completes
    assert 'add' in completes
    assert 'additional' in completes

    completes = t.get_autocomplete('ad', 10)
    print(completes)
    assert len(completes) == 2
    assert 'add' in completes
    assert 'additional' in completes

    completes = t.get_autocomplete('addi', 10)
    assert len(completes) == 1
    assert 'additional' in completes