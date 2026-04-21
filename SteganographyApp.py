import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import pickle

selected_image_path = None
selected_algorithm = None
len_text = 0

def choose_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        selected_image_path = file_path
        update_thumbnail()

def update_thumbnail():
    if selected_image_path:
        image = Image.open(selected_image_path)
        image.thumbnail((100, 100))
        tk_image = ImageTk.PhotoImage(image)
        thumbnail_label.config(image=tk_image)
        thumbnail_label.image = tk_image

def choose_algorithm(algorithm):
    global selected_algorithm
    selected_algorithm = algorithm

def process_image():
    global selected_image_path, selected_algorithm
    if not selected_algorithm:
        return
    if selected_image_path and selected_algorithm == "encrypt_text_lsb":
        encrypt_text_lsb()
    elif selected_algorithm == "decrypt_text_lsb":
        decrypt_text_lsb()
    elif selected_image_path and selected_algorithm == "hide_text_in_image_brightness":
        hide_text_in_image_brightness()
    elif selected_algorithm == "extract_text_from_image_brightness":
        extract_text_from_image_brightness()
    elif selected_algorithm == "embed_message":
        embed_message()
    elif selected_algorithm == "extract_message":
        extract_message()

def encrypt_text_lsb():
    text = entry_text.get()
    image = Image.open(selected_image_path)
    binary_text = ''.join(format(ord(char), '016b') for char in text)
    binary_text += '1111111111111110'
    data_index = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = list(image.getpixel((i, j)))
            for k in range(3):
                if data_index < len(binary_text):
                    pixel[k] = int(format(pixel[k], '016b')[:-1] + binary_text[data_index], 2)
                    data_index += 1
            image.putpixel((i, j), tuple(pixel))
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        image.save(save_path)

def decrypt_text_lsb():
    image = Image.open(selected_image_path)
    binary_text = ''
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = list(image.getpixel((i, j)))
            for k in range(3):
                binary_text += format(pixel[k], '016b')[-1]

    text = ''
    for i in range(0, len(binary_text), 16):
        byte = binary_text[i:i + 16]
        if byte == '1111111111111110':
            break
        text += chr(int(byte, 2))
    entry_result.delete(1.0, tk.END)
    entry_result.insert(tk.END, text)

def hide_text_in_image_brightness():
    text = entry_text.get()
    binary_secret_text = ''.join(format(ord(char), '08b') for char in text)
    global len_text
    len_text = len(binary_secret_text) // 8
    img = Image.open(selected_image_path)
    pixels = img.load()
    data_index = 0
    for i in range(img.height):
        for j in range(img.width):
            if data_index < len(binary_secret_text):
                r, g, b = pixels[i, j]
                if binary_secret_text[data_index] == '1':
                    b += round(0.1 * (0.2989 * r + 0.58662 * g + 0.11448 * b))
                if binary_secret_text[data_index] == '0':
                    b -= round(0.1 * (0.2989 * r + 0.58662 * g + 0.11448 * b))
                pixels[i, j] = (r, g, b)
                data_index += 1

    output_image_path = Image.new('RGB', (img.width, img.height))
    for y in range(img.height):
        for x in range(img.width):
            pixel_value = pixels[x, y]
            output_image_path.putpixel((x, y), pixel_value)
    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_image_path:
        img.save(output_image_path)

def extract_text_from_image_brightness():
    original_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    output_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if original_image_path and output_image_path:
        img = Image.open(original_image_path)
        pixels = img.load()
        img1 = Image.open(output_image_path)
        pixels1 = img1.load()

        s_text = ''
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b = pixels[i, j]
                r1, g1, b1 = pixels1[i, j]
                if b < b1 or b == b1 == 255:
                    s_text += '1'
                if b > b1 or b == b1 == 0:
                    s_text += '0'

        extracted_text = ''.join([chr(int(s_text[i:i + 8], 2)) for i in range(0, len(s_text), 8)])
        text = ''
        for i in range(len(extracted_text)):
            if len_text >= i + 1:
                text += extracted_text[i]
        entry_result.delete(1.0, tk.END)
        entry_result.insert(tk.END, text)

def embed_message():
    image_path = filedialog.askopenfilename()
    if image_path:
        message = entry_message.get()
        if message:
            img = Image.open(image_path)
            width, height = img.size
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            if len(binary_message) > width * height:
                status.set("Слишком длинное сообщение для данного изображения")
                return
            embed_indices = random.sample(range(width * height), len(binary_message))
            embedded_img = img.copy()
            pixels = embedded_img.load()
            key = random.randint(0, 2**32 - 1)
            metadata = {'indices': embed_indices, 'key': key}
            embedded_img.putalpha(Image.new("L", img.size, 255))
            for i, bit in enumerate(binary_message):
                x = embed_indices[i] % width
                y = embed_indices[i] // width
                pixel = list(pixels[x, y])
                pixel[-1] = (pixel[-1] & 0xFE) | int(bit)
                pixels[x, y] = tuple(pixel)
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                embedded_img.save(save_path)
                with open(save_path.replace('.png', '.dat'), 'wb') as f:
                    pickle.dump(metadata, f)
                status.set("Сообщение успешно встроено в изображение и сохранено")
                status.set("Ключ: " + str(key))
            else:
                status.set("Отменено сохранение изображения")
        else:
            status.set("Введите сообщение")

def extract_message():
    embedded_image_path = filedialog.askopenfilename()
    if embedded_image_path:
        key = entry_key.get()
        if not key:
            status.set("Введите ключ")
            return
        try:
            key = int(key)
            with open(embedded_image_path.replace('.png', '.dat'), 'rb') as f:
                metadata = pickle.load(f)
            embed_indices = metadata['indices']
            img = Image.open(embedded_image_path)
            width, height = img.size
            binary_message = ''
            for index in embed_indices:
                x = index % width
                y = index // width
                pixel = img.getpixel((x, y))
                lsb = pixel[-1] & 1
                binary_message += str(lsb)

            message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
            status.set("Расшифрованный текст: " + message)
        except FileNotFoundError:
            status.set("Файл с метаданными не найден")
        except Exception as e:
            status.set("Ошибка при извлечении сообщения: " + str(e))

app = tk.Tk()
app.title("STEGO APP")

thumbnail_label = tk.Label(app)
thumbnail_label.pack(pady=10)

btn_choose_image = tk.Button(app, text="Выбрать изображение", command=choose_image)
btn_choose_image.pack(pady=5)

label_for_entrytext = tk.Label(app, text="Ввести текст:")
label_for_entrytext.pack(pady=5)
entry_text = tk.Entry(app, width=25)
entry_text.pack(pady=5)

label_for_method_1 = tk.Label(app, text="LEAST SIGNIFICANT BIT:")
label_for_method_1.pack(pady=5)

btn_encrypt_lsb = tk.Button(app, text="Зашифровать текст (LSB)", command=lambda: choose_algorithm("encrypt_text_lsb"))
btn_encrypt_lsb.pack(pady=5)

btn_decrypt_lsb = tk.Button(app, text="Расшифровать текст (LSB)", command=lambda: choose_algorithm("decrypt_text_lsb"))
btn_decrypt_lsb.pack(pady=5)

label_for_method_2 = tk.Label(app, text="KUTTER-JORDAN-BOSSON:")
label_for_method_2.pack(pady=5)

btn_encrypt_brightness = tk.Button(app, text="Зашифровать текст (KJB)", command=lambda: choose_algorithm("hide_text_in_image_brightness"))
btn_encrypt_brightness.pack(pady=5)

btn_decrypt_brightness = tk.Button(app, text="Расшифровать текст (KJB)", command=lambda: choose_algorithm("extract_text_from_image_brightness"))
btn_decrypt_brightness.pack(pady=5)

btn_process = tk.Button(app, text="Обработать", command=process_image)
btn_process.pack(pady=10)

label_for_extractedtext = tk.Label(app, text="Расшифрованный текст:")
label_for_extractedtext.pack(pady=5)

entry_result = tk.Text(app, height=1, width=25)
entry_result.pack(pady=10)

label_for_method_3 = tk.Label(app, text="PSEUDO-RANDOM INTERVAL:")
label_for_method_3.pack(pady=5)

frame_pri = tk.Frame(app)
frame_pri.pack(side=tk.TOP)

label_message = tk.Label(frame_pri, text="Ввести текст:")
label_message.pack(side=tk.LEFT)

entry_message = tk.Entry(frame_pri)
entry_message.pack(side=tk.LEFT)

button_embed = tk.Button(frame_pri, text="Зашифровать текст (PRI)", command=embed_message)
button_embed.pack(side=tk.LEFT)

button_extract = tk.Button(frame_pri, text="Расшифровать текст (PRI)", command=extract_message)
button_extract.pack(side=tk.LEFT)

frame_key = tk.Frame(app)
frame_key.pack(side=tk.TOP)
label_key = tk.Label(frame_key, text="Ключ:")
label_key.pack(side=tk.LEFT)
entry_key = tk.Entry(frame_key)
entry_key.pack(side=tk.LEFT)
status = tk.StringVar()
status.set("Выберите изображение и введите сообщение для встраивания")
label_status = tk.Label(app, textvariable=status)
label_status.pack()
app.mainloop()