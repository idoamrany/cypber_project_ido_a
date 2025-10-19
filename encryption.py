# Author: ido amrany
# Program name: Encrypt or Decrypt
# Description: Encrypt or decrypt a message
# Date: 17:10:2025

import sys
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("encrypt_decrypt.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

ENCRYPTED_FILE = "msg_encrypted.txt"

def get_table():
    encryption_dictionary = {
        "A": 56, "B": 57, "C": 58, "D": 59, "E": 40, "F": 41, "G": 42, "H": 43, "I": 44, "J": 45, "K": 46, "L": 47,
        "M": 48, "N": 49, "O": 60, "P": 61, "Q": 62, "R": 63, "S": 64, "T": 65, "U": 66, "V": 67, "W": 68, "X": 69,
        "Y": 10, "Z": 11,
        "a": 12, "b": 13, "c": 14, "d": 15, "e": 16, "f": 17, "g": 18, "h": 19, "i": 30, "j": 31, "k": 32, "l": 33,
        "m": 34, "n": 35, "o": 36, "p": 37, "q": 38, "r": 39, "s": 90, "t": 91, "u": 92, "v": 93, "w": 94, "x": 95,
        "y": 96, "z": 97,
        " ": 98, ",": 99, ".": 100, "’": 101, "!": 102, "-": 103
    }
    return encryption_dictionary


def encrypt(table):
    what_you_what_to_encrypt = input("What you want to encrypt? ")
    try:
        with open(ENCRYPTED_FILE, "w") as f:
            for letter in what_you_what_to_encrypt:
                try:
                    encrypted_text = str(table[letter])
                    f.write(encrypted_text + ",")
                except KeyError as e:
                    logger.warning(f"Character not supported for encryption: {e}")
        logger.info("Message encrypted and saved to file.")
    except Exception as e:
        logger.error(f"Error during encryption: {e}")


def decrypt(reversed_dict):
    decrypted_text = ""
    try:
        with open(ENCRYPTED_FILE, "r") as f:
            encrypted_text = f.read().strip().split(",")

        for letter in encrypted_text:
            if letter:
                try:
                    decrypted_text += reversed_dict[int(letter)]
                except KeyError as e:
                    logger.warning(f"Value not supported for decryption: {e}")
        logger.info("Message decrypted successfully.")
    except Exception as e:
        logger.error(f"Error during decryption: {e}")
    return decrypted_text


def main():
    if len(sys.argv) < 2:
        logger.error("No mode specified. Use 'encrypt' or 'decrypt'.")
        print("Usage: python script.py encrypt|decrypt")
        return

    mode = sys.argv[1].lower()
    table = get_table()

    if mode == "encrypt":
        encrypt(table)
        print("Message encrypted.")
        logger.info("Encryption mode completed.")

    elif mode == "decrypt":
        reversed_dict = {v: k for k, v in table.items()}
        decrypted_msg = decrypt(reversed_dict)
        print("The decrypted message is:", decrypted_msg)
        logger.info("Decryption mode completed.")
    else:
        logger.error("Invalid mode. Must be 'encrypt' or 'decrypt'.")
        print("Mode must be 'encrypt' or 'decrypt'")


def run_assert_tests():
    table = get_table()
    reversed_dict = {v: k for k, v in table.items()}

    test_string = "Hello, world!"
    encrypted_values = [str(table[char]) for char in test_string]
    encrypted_line = ",".join(encrypted_values)

    with open(ENCRYPTED_FILE, "w") as f:
        f.write(encrypted_line + ",")

    decrypted = decrypt(reversed_dict)
    assert decrypted == test_string, f"Expected '{test_string}', got '{decrypted}'"
    logger.info("Encryption and decryption test passed.")
    print("Encryption and decryption test passed.")


# --- Run assert tests before main ---
if __name__ == "__main__":
    run_assert_tests()
    if len(sys.argv) > 1:
        main()