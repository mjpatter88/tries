from trie import Trie


def run(filename):
    with open(filename) as in_file:
        lines = [line.strip() for line in in_file.readlines()]
    t = Trie(lines)
    print(f"{len(t.get_words())} words ingested.")

    # print(t.get_autocomplete('ard', 10))
    # print(t.get_autocomplete('bin', 10))
    # print(t.get_autocomplete('cat', 10))
    # print(t.get_autocomplete('division', 10))

    while True:
        word = input('Enter a word to be completed: ')
        print(t.get_autocomplete(word, 100))



if __name__ == '__main__':
    run('words.txt')