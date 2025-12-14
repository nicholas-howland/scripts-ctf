import string
from datetime import datetime

def log_guess(plaintext, line_number, result, offset, log_path="guess_log.txt"):
    with open(log_path, "a") as log_file:
        log_file.write(f"[{datetime.now()}] Line {line_number}, Offset {offset}\n")
        log_file.write(f"  Guess:    {plaintext}\n")
        log_file.write(f"  Revealed: {result}\n\n")

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

def display_recovered(ciphertexts, keystream):
    print("\n🔍 Recovered Messages:")
    for i, ct in enumerate(ciphertexts):
        recovered = xor_bytes(ct[:len(keystream)], keystream)
        print(f"[{i}] {recovered.decode(errors='replace')}")
    print()

# === Setup ===
ciphertexts = load_ciphertexts("chatlog_hex.txt")
keystream = b""

# === Initial keystream seed ===
known = input("Enter known plaintext to seed: ").encode()
line = int(input("Line # that contains this plaintext: "))
keystream = xor_bytes(ciphertexts[line][:len(known)], known)

print("\nInitial keystream seeded. Starting interactive mode.\n")


# === Manual guessing loop ===
# Track keystream history for undo
keystream_history = [keystream]

while True:
    display_recovered(ciphertexts, keystream)

    print("Options:")
    print("  [guess] Enter a plaintext guess")
    print("  [preview] Try a guess without modifying the keystream")
    print("  [undo] Undo the last guess")
    print("  [exit] Quit\n")

    choice = input("Enter option: ").strip().lower()

    if choice == "exit":
        break

    elif choice == "undo":
        if len(keystream_history) > 1:
            keystream_history.pop()
            keystream = keystream_history[-1]
            print("🔁 Last guess undone.\n")
        else:
            print("⚠️ Nothing to undo.\n")

    elif choice == "preview":
        test_input = input("Preview plaintext guess: ").encode()
        try:
            line_index = int(input("Line # to test this guess on: "))
            offset = len(keystream)

        # Generate a temporary extension of the keystream
            temp_ks = bytearray(keystream)
            for i in range(len(test_input)):
                ks_byte = ciphertexts[line_index][offset + i] ^ test_input[i]
                temp_ks.append(ks_byte)

            print("\n🕵️ Preview result with your guess applied:")
            for i, ct in enumerate(ciphertexts):
                recovered = xor_bytes(ct[:len(temp_ks)], temp_ks)
                print(f"[{i}] {recovered.decode(errors='replace')}")
            print()

        except Exception as e:
            print(f"⚠️ Error during preview: {e}\n")


    elif choice == "guess":
        next_input = input("Enter plaintext guess: ").encode()
        try:
            target_line = int(input("Line # this guess corresponds to: "))
            index = len(keystream)
            new_ks = bytearray()

            for i in range(len(next_input)):
                ks_byte = ciphertexts[target_line][index + i] ^ next_input[i]
                new_ks.append(ks_byte)

            keystream += bytes(new_ks)
            keystream_history.append(keystream)
            decoded_snippet = xor_bytes(
                ciphertexts[target_line][index:index + len(next_input)],
                bytes(new_ks)
            ).decode(errors="replace")

            log_guess(
                plaintext=next_input.decode(errors="replace"),
                line_number=target_line,
                result=decoded_snippet,
                offset=index
            )
            print("✅ Guess applied and logged.\n")

        except Exception as e:
            print(f"⚠️ Error applying guess: {e}\n")

    else:
        print("⚠️ Unknown option. Use 'guess', 'preview', 'undo', or 'exit'.\n")
