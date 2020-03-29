import time
from collections import deque

class Node:
    def __init__(self, terminal=False):
        self.terminal = terminal
        # map of value -> node
        self.nodes = {}

def add_to_node(node, words):
    while words:
        word = words.popleft()
        add_rec(words, word, 0, node)


def add_rec(words, word, index, node):
    if index == len(word):
        assert node.terminal == False, f"Duplicate words are not allowed. {word}"
        node.terminal = True
        return
    letter = word[index]
    if letter in node.nodes:
        node = node.nodes[letter]
    else:
        node.nodes[letter] = Node(False)
        node = node.nodes[letter]
    add_rec(words, word, index+1, node)

    # Recursive implementation. When a word is added, start at that node for the next word.
    # If the path isn't in the new word, then back up one level and try, etc.
    while words:
        new_word = words.popleft()
        if new_word.startswith(word[:index + 1]):
            add_rec(words, new_word, index + 1, node)
        else:
            words.appendleft(new_word)
            break


class Trie:
    def __init__(self, word_list):
        start = time.time()
        self.root = Node(False)
        words = deque()
        words.extendleft(word_list)
        add_to_node(self.root, words)
        end = time.time()
        print(f"Building trie took {end-start} seconds.")
    
    def get_words(self):
        start = time.time()
        words = []

        # holds (prefix, node) tuples to visit
        nodes = deque()
        for key, node in self.root.nodes.items():
            nodes.append((key, node))

        while nodes:
            prefix, cur_node = nodes.pop()
            if cur_node.terminal:
                words.append(prefix)
            for key, node in cur_node.nodes.items():
                new_prefix = prefix + key
                nodes.append((new_prefix, node))
        end = time.time()
        print(f"Build word list took {1000*(end-start)} ms.")
        return words

    def get_autocomplete(self, search, limit):
        start = time.time()
        words = []

        # holds (prefix, search_remainder, node) tuples to visit
        nodes = deque()
        nodes.append(('', search, self.root))

        while nodes:
            prefix, search_remainder, cur_node = nodes.pop()

            # If we have already found the entire search, then add this node (if it's a word)
            # and add this node's descendents to search next
            if not search_remainder:
                # only add word if it is a word and if we have fulfilled the search
                if cur_node.terminal:
                    words.append(prefix)
                    if len(words) >= limit:
                        break
                for key, node in cur_node.nodes.items():
                    new_prefix = prefix + key
                    nodes.appendleft((new_prefix, search_remainder, node))
            # If we have not found everything yet, find the descendent node that matches the
            # next element in the search string and add it to search next
            else:
                next_letter = search_remainder[0]
                if next_letter in cur_node.nodes:
                    node = cur_node.nodes[next_letter]
                    new_prefix = prefix + next_letter
                    # TODO: this might be very slow. Put letters in deque rather than string?
                    new_search_remainder = search_remainder[1:]
                    nodes.appendleft((new_prefix, new_search_remainder, node))
        end = time.time()
        print(f"Completion took {1000*(end-start)} ms.")
        return words



if __name__ == '__main__':
    word_list = ['a', 'add', 'additional']
    t = Trie(word_list)
    print(t.get_words())