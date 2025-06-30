
# 🔐 Image Steganography with AES Encryption

This project hides encrypted messages inside images using AES encryption and LSB steganography.

## 📂 How it Works
1. Encrypts message using AES (CBC mode)
2. Converts encrypted data to binary
3. Embeds binary in least significant bits of pixels
4. Extracts and decrypts data from stego-image

## 🛠️ Tech Stack
- Python
- OpenCV
- PyCryptodome (AES, Padding)
- NumPy

## 🚀 How to Run
1. Clone the repo
2. Run: `pip install -r requirements.txt`
3. Run the script: `python main.py`
4. View output: `stego.png` and decrypted message

## 🖼️ Screenshots
(Attach or embed screenshots from `/screenshots`)

## 🔗 References
Listed in the PPT or project report.

## 📃 License
MIT License
