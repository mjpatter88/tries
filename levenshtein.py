import time
from functools import lru_cache
from trie import Trie

def basic_rec(word1, word2, index1, index2):
    if index1 >= len(word1):
        return len(word2) - index2
    if index2 >= len(word2):
        return len(word1) - index1
    # Cost of substitution is 0 if letters match, 1 otherwise
    sub_cost = 0 if word1[index1] == word2[index2] else 1
    return min([
        basic_rec(word1, word2, index1+1, index2) + 1, # insertion
        basic_rec(word1, word2, index1, index2+1) + 1, # deletion
        basic_rec(word1, word2, index1+1, index2+1) + sub_cost, # substitution (if necessary)
    ])

@lru_cache(maxsize=None)
def dynamic_rec(word1, word2, index1, index2):
    if index1 >= len(word1):
        return len(word2) - index2
    if index2 >= len(word2):
        return len(word1) - index1
    # Cost of substitution is 0 if letters match, 1 otherwise
    sub_cost = 0 if word1[index1] == word2[index2] else 1
    return min([
        dynamic_rec(word1, word2, index1+1, index2) + 1, # insertion
        dynamic_rec(word1, word2, index1, index2+1) + 1, # deletion
        dynamic_rec(word1, word2, index1+1, index2+1) + sub_cost, # substitution (if necessary)
    ])

# Use this approach: https://en.wikipedia.org/wiki/Levenshtein_distance#Iterative_with_full_matrix
def iterative_mat(word1, word2):
    dist = 0

    # Initial matrix to all 0s
    matrix = []
    for _ in range(len(word2)+1):
        matrix.append([0] * (len(word1) + 1))

    # Initialize the first row and column
    # Which represent comparisons to empty words
    for col in range(1,len(word1)+1):
        matrix[0][col] = col
    for row in range(1,len(word2)+1):
        matrix[row][0] = row

    for row in range(1,len(word2)+1):
        for col in range(1,len(word1)+1):
            # Cost of substitution is 0 if letters match, 1 otherwise
            sub_cost = 0 if word1[col-1] == word2[row-1] else 1
            matrix[row][col] = min([
                matrix[row-1][col] + 1, # deletion
                matrix[row][col-1] + 1, # insertion
                matrix[row-1][col-1] + sub_cost, # substitutation (if necessary)
            ])

    return matrix[len(word2)][len(word1)]

# http://stevehanov.ca/blog/?id=114
# https://cslu.ohsu.edu/~bedricks/courses/cs655/pdf/w10_lec1.pdf
# https://github.com/umbertogriffo/Trie
def trie_lev(word, trie, max_dist):

    cur_row = [x for x in range(len(word)+1)]
    results = []

    # try each branch from the root
    for letter, node in trie.root.nodes.items():
        trie_search(node, letter, word, cur_row, results, max_dist, letter)

    return results

def trie_search(node, letter, word, prev_row, results, max_dist, prefix):
    num_cols = len(word) + 1
    cur_row = []
    cur_row.append(prev_row[0] + 1)

    # build out the current row, similar to the iterative_mat method above
    for col in range(1, num_cols):
        sub_cost = 0 if word[col-1] == letter else 1

        new_val = min([
            prev_row[col] + 1, # deletion
            cur_row[col-1] + 1, # insertion
            prev_row[col-1] + sub_cost, # substitutation (if necessary)
        ])
        cur_row.append(new_val)

    if cur_row[-1] <= max_dist and node.terminal:
        results.append(prefix)
    
    if min(cur_row) <= max_dist:
        for new_letter, new_node in node.nodes.items():
            trie_search(new_node, new_letter, word, cur_row, results, max_dist, prefix+new_letter)


MAX_DIST = 2
def distance(filename):

    with open(filename) as in_file:
        lines = [line.strip() for line in in_file.readlines()]
    trie = Trie(lines)

    while True:
        word = input('Enter a word to find its fuzzy matches: ')
        start = time.time()
        print(trie_lev(word, trie, MAX_DIST))
        end = time.time()
        print(f"Time: {(end-start) * 1000} ms")

if __name__ == '__main__':
    distance('words.txt')

