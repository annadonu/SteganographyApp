Markdown
# SteganographyApp

SteganographyApp is a Python-based desktop application designed for hiding and extracting text within digital images using various steganographic algorithms. The project provides a graphical user interface (GUI) to make complex data-hiding techniques accessible and easy to use.

## Features

- **LSB (Least Significant Bit):** A classic method that embeds data into the least significant bits of image pixels, ensuring minimal visual distortion.
- **KJB (Kutter-Jordan-Bossen):** A robust method that hides information by modifying the brightness of the blue channel, making it more resistant to certain image transformations.
- **PRI (Pseudo-Random Interval):** Uses a pseudo-random sequence to determine embedding locations, significantly increasing the security of the hidden message.
- **Interactive GUI:** Built with `tkinter`, featuring image previews, method selection, and real-time processing.

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/SteganographyApp.git](https://github.com/your-username/SteganographyApp.git)
   cd SteganographyApp
Install dependencies:
The project relies on the Pillow (PIL) library for image manipulation:

Bash
pip install Pillow
Usage
Launch the app:

Bash
python SteganographyApp.py
Select an Image: Click "Выбрать изображение" to load a PNG or JPG file.

Choose a Method:

For LSB, select "Зашифровать текст (LSB)" or "Расшифровать текст (LSB)".

For KJB, use the "Скрыть текст (KJB)" and "Расшифровать текст (KJB)" options.

For PRI, enter your text in the "Ввести текст" field and use the corresponding PRI buttons.

Process: Click "Обработать" or the specific algorithm button to execute.

Technical Background
This project explores the trade-offs between data capacity, invisibility, and robustness in digital steganography. It implements:

Standard LSB replacement.

Brightness-based modification (Kutter-Jordan-Bossen).

Randomized embedding intervals for enhanced security.
