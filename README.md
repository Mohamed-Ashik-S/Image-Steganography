# LSB Steganography Application

This is a Python application for performing Least Significant Bit (LSB) steganography on images. LSB steganography is a technique for hiding a secret message within an image by modifying the least significant bit of each pixel's color channel. The application provides the functionality to encode a secret message into an image and decode a hidden message from an encoded image.

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
  - [Encoding a Message](#encoding-a-message)
  - [Decoding a Message](#decoding-a-message)
- [Security](#security)
- [Contributing](#contributing)

## Requirements

To run this application, you need the following dependencies:

- Python 3.x
- tkinter (Python's standard GUI library)
- Pillow (PIL) library for image processing

You can install the required libraries using pip:

bash
pip install pillow


## Usage

### Encoding a Message

1. Launch the application by running the `lsb_steganography.py` script.

2. Open an image by clicking the "Open Image" button. Supported image formats are PNG, JPG, and JPEG.

3. Enter the secret message you want to hide in the "Secret Message" input field.

4. Optionally, set a password in the "Password" input field. This password will be used to decode the message later.

5. Click the "Set Password" button to confirm the password (if set).

6. Click the "Encode" button to hide the secret message in the selected image. The encoded image will be saved with a `.png` extension.

   ![Encoding](https://github.com/Mohamed-Ashik-S/Image-Steganography/blob/main/encoding_image.png)

### Decoding a Message

1. Launch the application by running the `lsb_steganography.py` script.

2. Open the encoded image (with the hidden message) by clicking the "Open Image" button.

3. Enter the password (if set during encoding) in the "Enter PIN" input field.

4. Click the "Decode" button to reveal the hidden message. The decoded message will be displayed in the "Decoded Message" section.

   ![Decoding](https://github.com/Mohamed-Ashik-S/Image-Steganography/blob/main/Decoding_image.png)

## Security

- *Password Protection*: If you choose to set a password during encoding, the application will require the correct password during decoding to ensure that only authorized users can access the hidden message.

- *Encryption*: This application focuses on steganography (hiding data), not encryption (protecting data). If you have sensitive information, consider encrypting it separately before using this tool.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.
