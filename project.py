import cv2
import hashlib
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_message(message, key):
    print("[*] Encrypting message...")
    key_hash = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key_hash, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ct_bytes  # Prepend IV for decryption

def embed_data_in_image(image_path, data, output_path):
    import numpy as np
    print("[*] Embedding data into image...")

    image = cv2.imread(image_path)
    binary_data = ''.join(format(byte, '08b') for byte in data)

    # Step 1: Add a 32-bit header indicating the length of the data
    data_len = len(binary_data)
    header = format(data_len, '032b')  # 32-bit header
    full_binary = header + binary_data

    idx = 0
    for row in image:
        for pixel in row:
            for i in range(3):
                if idx < len(full_binary):
                    original = int(pixel[i])
                    pixel[i] = np.uint8((original & ~1) | int(full_binary[idx]))
                    idx += 1
                else:
                    break
    cv2.imwrite(output_path, image)
    print(f"[+] Data embedded and saved as: {output_path}")


def extract_data_from_image(image_path, key):
    print("[*] Extracting data from image...")
    image = cv2.imread(image_path)
    binary_data = ""

    for row in image:
        for pixel in row:
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    # Step 1: Read first 32 bits to get data length
    header = binary_data[:32]
    data_len = int(header, 2)

    # Step 2: Extract that many bits
    encrypted_bits = binary_data[32:32+data_len]
    all_bytes = [encrypted_bits[i:i+8] for i in range(0, len(encrypted_bits), 8)]
    encrypted_data = bytes([int(b, 2) for b in all_bytes])

    key_hash = hashlib.sha256(key.encode()).digest()
    iv = encrypted_data[:16]
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)

    try:
        decrypted = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
        return decrypted.decode()
    except:
        return "[!] Decryption failed. Possibly wrong key or corrupted image."


if __name__ == "__main__":
    # === INPUTS ===
    secret_message = "This is a top secret message."
    secret_key = "mysecurekey123"
    input_image = "original.png"
    stego_image = "stego.png"

    # === ENCRYPT & EMBED ===
    encrypted = encrypt_message(secret_message, secret_key)
    embed_data_in_image(input_image, encrypted, stego_image)

    # === EXTRACT & DECRYPT ===
    result = extract_data_from_image(stego_image, secret_key)
    print("[+] Decrypted message:", result)
