import random
leet_dict = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "$"}
with open("/usr/share/dict/american-english") as f:
    words = [line.strip() for line in f.readlines()]
random_word = random.choice(words)
leet_username = "".join([leet_dict.get(char.lower(), char) for char in random_word])
print(leet_username)
