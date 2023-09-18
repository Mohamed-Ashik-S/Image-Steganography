import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Password for encoding and decoding
password = ""

def encode_lsb(image_path, secret_message, output_path):
    global password  # Access the global password variable

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
    global password  # Access the global password variable

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

    # Extract the secret message
    secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    return secret_message

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)

def set_password():
    global password
    password = password_entry.get()

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
        entered_pin = pin_entry.get()
        if password:  # If password is set, use it for decoding
            if entered_pin == password:  # Check if the entered PIN matches the password
                decoded_message_var.set(decoded_message)
                status_var.set("Message decoded successfully!")
            else:
                decoded_message_var.set("Error: Wrong PIN.")
        else:  # If no password is set, display the secret message directly
            decoded_message_var.set(decoded_message)
            status_var.set("Message decoded successfully!")
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

# Password entry
tk.Label(root, text="Password:").grid(row=2, column=0)
password_entry = tk.Entry(root, show='*')  # Mask the password with asterisks
password_entry.grid(row=2, column=1)

# Set Password button
tk.Button(root, text="Set Password", command=set_password).grid(row=2, column=2)

# Encode button
tk.Button(root, text="Encode", command=encode_message).grid(row=3, column=0)

# Decode button
tk.Button(root, text="Decode", command=decode_message).grid(row=3, column=1)

# Decoded message display
decoded_message_var = tk.StringVar()
tk.Label(root, text="Decoded Message:").grid(row=4, column=0)
tk.Label(root, textvariable=decoded_message_var, wraplength=300, anchor="w", justify="left").grid(row=4, column=1)

# PIN entry
tk.Label(root, text="Enter PIN:").grid(row=5, column=0)
pin_entry = tk.Entry(root)
pin_entry.grid(row=5, column=1)

# Status label
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="red")
status_label.grid(row=6, column=0, columnspan=3)


root.mainloop()
