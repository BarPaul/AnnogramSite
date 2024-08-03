MIN_LEN, MAX_LEN = 3, 10
with open('all_words.txt', encoding='utf-8') as f:
    data = f.read().splitlines()

with open('words.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(filter(lambda word: MIN_LEN <= len(word) <= MAX_LEN, data)))