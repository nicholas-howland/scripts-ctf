import string

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def load_ciphertexts(file_path):
    with open(file_path, 'r') as f:
        return [bytes.fromhex(line.strip()) for line in f if line.strip()]

def load_wordlist(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def is_printable(b):
    try:
        s = b.decode('utf-8')
        return all(c in string.printable for c in s)
    except:
        return False

def try_word_on_all_lines(word, ciphertexts, keystream_len):
    word_bytes = word.encode()
    matches = []
    for i, ct in enumerate(ciphertexts):
        if len(ct) >= keystream_len + len(word_bytes):
            slice_ct = ct[keystream_len:keystream_len + len(word_bytes)]
            guess_keystream = xor_bytes(slice_ct, word_bytes)
            recovered = xor_bytes(slice_ct, guess_keystream)
            if is_printable(recovered):
                matches.append((i, word, recovered.decode(errors='ignore')))
    return matches

# === Setup ===
ciphertexts = load_ciphertexts("chatlog_hex.txt")
keystream = b""

# === Initial keystream seed ===
known = input("Enter known plaintext to seed: ").encode()
line = int(input("Line # that contains this plaintext: "))
keystream = xor_bytes(ciphertexts[line][:len(known)], known)

print("\nInitial keystream seeded. Starting interactive mode.\n")

# === Auto guess mode ===
use_wordlist = input("Load a wordlist for auto-guessing? (y/n): ").strip().lower()
if use_wordlist == 'y':
    words = load_wordlist("wordlist.txt")  # Provide your wordlist file
    print("\nAuto-guessing...")
    for word in words:
        matches = try_word_on_all_lines(word, ciphertexts, len(keystream))
        for idx, guessed_word, result in matches:
            print(f"[{idx}] '{guessed_word}' → {result}")
    print("\nEnd of wordlist pass.\n")

# === Manual guessing loop ===
while True:
    print("\nCurrent Decryption:")
    for i, ct in enumerate(ciphertexts):
        part = xor_bytes(ct[:len(keystream)], keystream)
        print(f"[{i}] {part.decode(errors='replace')}")
    print()

    next_input = input("Next guess (ENTER to quit): ")
    if not next_input:
        break

    try:
        target_line = int(input("Line # this guess corresponds to: "))
        next_bytes = next_input.encode()
        index = len(keystream)

        for i in range(len(next_bytes)):
            ks_byte = ciphertexts[target_line][index + i] ^ next_bytes[i]
            keystream += bytes([ks_byte])
    except (IndexError, ValueError):
        print("Invalid input or message too short.")
        break
