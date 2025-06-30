import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib

class Steganography:
    def __init__(self):
        self.key = None
        
    def generate_key(self, password):
        """Generate AES key from password"""
        return hashlib.sha256(password.encode()).digest()
    
    def encrypt_message(self, message, password):
        """Encrypt message using AES encryption"""
        key = self.generate_key(password)
        cipher = AES.new(key, AES.MODE_CBC)
        
        # Pad message and encrypt
        padded_message = pad(message.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded_message)
        
        # Combine IV and encrypted data
        encrypted_data = cipher.iv + encrypted
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_message(self, encrypted_data, password):
        """Decrypt message using AES decryption"""
        try:
            key = self.generate_key(password)
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # Extract IV and encrypted message
            iv = encrypted_bytes[:16]
            encrypted_message = encrypted_bytes[16:]
            
            # Decrypt
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_message)
            decrypted = unpad(decrypted_padded, AES.block_size)
            
            return decrypted.decode()
        except Exception as e:
            return f"Decryption failed: {str(e)}"
    
    def text_to_binary(self, text):
        """Convert text to binary"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    def binary_to_text(self, binary):
        """Convert binary to text"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def embed_message(self, image_path, message, password, output_path='stego.png'):
        """Embed encrypted message in image using LSB steganography"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return False, "Could not read image file"
            
            # Encrypt message
            encrypted_msg = self.encrypt_message(message, password)
            
            # Convert to binary and add delimiter
            binary_msg = self.text_to_binary(encrypted_msg + "###END###")
            
            # Check if image can hold the message
            total_pixels = img.shape[0] * img.shape[1] * img.shape[2]
            if len(binary_msg) > total_pixels:
                return False, "Image too small to hold the message"
            
            # Embed message in LSB
            data_index = 0
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(img.shape[2]):
                        if data_index < len(binary_msg):
                            # Modify LSB
                            img[i][j][k] = (img[i][j][k] & 0xFE) | int(binary_msg[data_index])
                            data_index += 1
                        else:
                            break
                    if data_index >= len(binary_msg):
                        break
                if data_index >= len(binary_msg):
                    break
            
            # Save stego image
            cv2.imwrite(output_path, img)
            return True, f"Message embedded successfully in {output_path}"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def extract_message(self, image_path, password):
        """Extract and decrypt message from stego image"""
        try:
            # Read stego image
            img = cv2.imread(image_path)
            if img is None:
                return False, "Could not read image file"
            
            # Extract binary data from LSB
            binary_msg = ""
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(img.shape[2]):
                        binary_msg += str(img[i][j][k] & 1)
                        
                        # Check for end delimiter
                        if len(binary_msg) >= 72:  # 9 characters * 8 bits
                            if binary_msg[-72:] == self.text_to_binary("###END###"):
                                # Remove delimiter
                                binary_msg = binary_msg[:-72]
                                break
                    else:
                        continue
                    break
                else:
                    continue
                break
            
            # Convert binary to text
            encrypted_msg = self.binary_to_text(binary_msg)
            
            # Decrypt message
            decrypted_msg = self.decrypt_message(encrypted_msg, password)
            return True, decrypted_msg
            
        except Exception as e:
            return False, f"Error: {str(e)}"

def main():
    stego = Steganography()
    
    print("=== Advanced Steganography Tool ===")
    print("1. Hide message in image")
    print("2. Extract message from image")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        # Hide message
        image_path = input("Enter image path (or press Enter for 'sample.png'): ").strip()
        if not image_path:
            image_path = "sample.png"
            
        message = input("Enter message to hide: ")
        password = input("Enter password for encryption: ")
        
        output_path = input("Enter output path (or press Enter for 'stego.png'): ").strip()
        if not output_path:
            output_path = "stego.png"
        
        success, result = stego.embed_message(image_path, message, password, output_path)
        if success:
            print(f"✓ {result}")
        else:
            print(f"✗ {result}")
    
    elif choice == '2':
        # Extract message
        image_path = input("Enter stego image path: ")
        password = input("Enter password for decryption: ")
        
        success, result = stego.extract_message(image_path, password)
        if success:
            print(f"✓ Extracted message: {result}")
        else:
            print(f"✗ {result}")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
