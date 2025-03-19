class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        num_of_columns = int(len(text) / key)
        num_of_rows = key
        num_of_shaded_boxes = (num_of_columns * num_of_rows) - len(text)

        decrypted_text = [''] * num_of_columns
        col = 0
        row = 0

        for symbol in text:
            decrypted_text[col] += symbol
            col += 1

            if (col == num_of_columns) or (col == num_of_columns - 1 and row >= num_of_rows - num_of_shaded_boxes):
                col = 0
                row += 1

        return ''.join(decrypted_text)
