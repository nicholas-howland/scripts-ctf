import binascii

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def load_ciphertexts(file_path):
    with open(file_path, 'r') as f:
        return [bytes.fromhex(line.strip()) for line in f if line.strip()]

# === Path to your ciphertext log file ===
cipher_file = "chatlog_hex.txt"

# === Load ciphertexts from file ===
ciphertexts = load_ciphertexts(cipher_file)

# === Known plaintext prefix ===
known_plaintext = input("Enter known plaintext: ").encode()

# Recover initial keystream using the first ciphertext
keystream = xor_bytes(ciphertexts[0][:len(known_plaintext)], known_plaintext)
current_guess = known_plaintext

print("\n=== Interactive Decryption Mode ===")
print("Type the next character(s) you want to guess. Press Enter to quit.\n")

while True:
    print("Recovered Messages:")
    for i, ct in enumerate(ciphertexts):
        partial = xor_bytes(ct[:len(keystream)], keystream)
        print(f"[{i}] {partial.decode(errors='replace')}")
    print()

    known_plaintext = input("Next plaintext guess (ENTER to quit): ")
    if not known_plaintext:
        break

    try:
        target_line = int(input("Which line # does this guess match? "))
        if target_line < 0 or target_line >= len(ciphertexts):
            print("Invalid line number.")
            continue
    except ValueError:
        print("Please enter a valid number.")
        continue

    next_bytes = known_plaintext.encode()
    index = len(keystream)
    try:
        for i in range(len(next_bytes)):
            ks_byte = ciphertexts[target_line][index + i] ^ next_bytes[i]
            keystream += bytes([ks_byte])
            current_guess += bytes([next_bytes[i]])
    except IndexError:
        print("Guess extends beyond the length of the selected message.")
        break

