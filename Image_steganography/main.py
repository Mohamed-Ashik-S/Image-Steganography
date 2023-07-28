import tkinter as tk
from tkinter import filedialog
from PIL import Image

def encode_lsb(image_path, secret_message, output_path):
    # Load the image
    img = Image.open(image_path)
    img = img.convert("RGB")

    # Get the binary representation of the secret message
    binary_secret_message = ''.join(format(ord(c), "08b") for c in secret_message)

    # Check if the image can hold the secret message
    if len(binary_secret_message) > img.size[0] * img.size[1] * 3:
        raise ValueError("Image too small to hold the message. Try using a larger image or a shorter message.")

    # Add termination delimiter to the binary message
    binary_secret_message += "00000000"

    # Counter variable to keep track of the binary message index
    message_index = 0
    message_bytes = bytes([int(binary_secret_message[i:i + 8], 2) for i in range(0, len(binary_secret_message), 8)])

    # Embed the secret message into the image using LSB steganography
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel = list(img.getpixel((x, y)))
            for c in range(3):
                if message_index < len(binary_secret_message):
                    # Modify the least significant bit of the pixel value with the bit from the binary message
                    pixel[c] = pixel[c] & ~1 | int(binary_secret_message[message_index])
                    message_index += 1
            img.putpixel((x, y), tuple(pixel))

    # Save the encoded image to the output path
    img.save(output_path)

    print("Message encoded successfully in the image.")

def decode_lsb(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")

    binary_message = ""
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel = img.getpixel((x, y))
            for c in range(3):
                binary_message += format(pixel[c], "08b")[-1]  # Extract the LSB of each color channel

    # Find the end of the message (it is terminated with eight 0 bits)
    end_index = binary_message.find("00000000")
    binary_message = binary_message[:end_index]

    # Pad binary message to be a multiple of 8
    padded_length = (len(binary_message) + 7) // 8 * 8
    binary_message = binary_message.ljust(padded_length, "0")

    return binary_message

def Binary_to_text(binary_string):
    text = ""
    padded_binary = binary_string.ljust((len(binary_string) + 7) // 8 * 8, "0")  # Pad binary message to be a multiple of 8
    for i in range(0, len(padded_binary), 8):
        byte = padded_binary[i:i + 8]
        text += chr(int(byte, 2))
    return text

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)

def encode_message():
    image_path = image_path_var.get()
    secret_message = secret_message_entry.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_path:
        try:
            encode_lsb(image_path, secret_message, output_path)
            status_var.set("Message encoded successfully!")
        except Exception as e:
            status_var.set(f"Error: {e}")

def decode_message():
    image_path = image_path_var.get()
    try:
        decoded_message = decode_lsb(image_path)
        decoded_text = Binary_to_text(decoded_message)
        decoded_message_var.set(decoded_text)
        status_var.set("Message decoded successfully!")
        print("Decoded message:", decoded_message)  # Print the decoded message in the terminal
    except Exception as e:
        status_var.set(f"Error: {e}")

# Create the main application window
root = tk.Tk()
root.title("LSB Steganography Application")

# Image selection
image_path_var = tk.StringVar()
tk.Label(root, text="Image Path:").grid(row=0, column=0)
tk.Entry(root, textvariable=image_path_var, state="readonly").grid(row=0, column=1)
tk.Button(root, text="Open Image", command=open_image).grid(row=0, column=2)

# Secret message entry
tk.Label(root, text="Secret Message:").grid(row=1, column=0)
secret_message_entry = tk.Entry(root)
secret_message_entry.grid(row=1, column=1)

# Encode button
tk.Button(root, text="Encode", command=encode_message).grid(row=2, column=0)

# Decode button
tk.Button(root, text="Decode", command=decode_message).grid(row=2, column=1)

# Decoded message display
decoded_message_var = tk.StringVar()
tk.Label(root, text="Decoded Message:").grid(row=3, column=0)
tk.Label(root, textvariable=decoded_message_var, wraplength=300, anchor="w", justify="left").grid(row=3, column=1)

# Status label
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="red")
status_label.grid(row=4, column=0, columnspan=3)

root.mainloop()

