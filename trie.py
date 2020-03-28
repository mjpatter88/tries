import time
from collections import deque

class Node:
    def __init__(self, terminal=False):
        self.terminal = terminal
        # map of value -> node
        self.nodes = {}


class Trie:
    def __init__(self, word_list):
        start = time.time()
        self.root = Node(False)
        # TODO: this could be much faster if we new the incoming word list was sorted, which we do.
        # Try a recursive implementation. When a word is added, start at that node for the next word.
        # If the path isn't in the new word, then back up one level and try, etc.
        for word in word_list:
            self.add(word)
        end = time.time()
        print(f"Building trie took {end-start} seconds.")
    
    def add(self, word):
        cur_node = self.root
        for letter in word:
            if letter in cur_node.nodes:
                cur_node = cur_node.nodes[letter]
            else:
                cur_node.nodes[letter] = Node(False)
                cur_node = cur_node.nodes[letter]
        # after going through the whole word, update the terminal value on the last node
        assert cur_node.terminal == False, f"Duplicate words are not allowed. {letter}"
        cur_node.terminal = True
    
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


