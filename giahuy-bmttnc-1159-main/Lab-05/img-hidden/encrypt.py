import sys
from PIL import Image

def encode_image(image_path, message):
    try:
        # Open the image
        img = Image.open(image_path)
        width, height = img.size

        # Convert the message to binary and add a delimiter
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '1111111111111110'  # Delimiter to mark the end of the message

        data_index = 0
        for row in range(height):
            for col in range(width):
                pixel = list(img.getpixel((col, row)))

                # Modify the pixel's color channels to encode the message
                for color_channel in range(3):
                    if data_index < len(binary_message):
                        pixel[color_channel] = int(
                            format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2
                        )
                        data_index += 1

                img.putpixel((col, row), tuple(pixel))

                # Stop encoding if the entire message is embedded
                if data_index >= len(binary_message):
                    break
            if data_index >= len(binary_message):
                break

        # Save the encoded image with a proper file extension
        encoded_image_path = 'encoded_image.png'
        img.save(encoded_image_path)
        print("Steganography complete. Encoded image saved as", encoded_image_path)

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == "__main__":
    main()