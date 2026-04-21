# SteganographyApp

SteganographyApp is a Python-based desktop application designed for hiding and extracting text within digital images using various steganographic algorithms. The project provides a graphical user interface (GUI) to make complex data-hiding techniques accessible and easy to use.

## Features

* **LSB (Least Significant Bit):** A classic method that embeds data into the least significant bits of image pixels, ensuring minimal visual distortion.
* **KJB (Kutter-Jordan-Bossen):** A robust method that hides information by modifying the brightness of the blue channel, making it more resistant to certain image transformations.
* **PRI (Pseudo-Random Interval):** Uses a pseudo-random sequence to determine embedding locations, significantly increasing the security of the hidden message.
* **Interactive GUI:** Built with `tkinter`, featuring image previews, method selection, and real-time processing.

## Installation

### Prerequisites
* `Python 3.x`
* `pip` (Python package installer)

### Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/SteganographyApp.git](https://github.com/your-username/SteganographyApp.git)
    cd SteganographyApp
    ```
2.  **Install dependencies:** The project relies on the `Pillow` library for image manipulation:
    ```bash
    pip install Pillow
    ```

## Usage

1.  **Launch:** Start the application by running the main script:
    ```bash
    python SteganographyApp.py
    ```
2.  **Select an Image:** Click the **"Выбрать изображение"** button to load a `.png` or `.jpg` file.
3.  **Choose a Method:**
    * For **LSB**, select **"Зашифровать текст (LSB)"** or **"Расшифровать текст (LSB)"**.
    * For **KJB**, use the **"Скрыть текст (KJB)"** and **"Расшифровать текст (KJB)"** options.
    * For **PRI**, enter your secret message in the **"Ввести текст"** field and use the corresponding **PRI** buttons.
4.  **Process:** Click the specific algorithm button or **"Обработать"** to execute the data hiding or extraction.

## Technical Background

This project explores the trade-offs between data capacity, invisibility, and robustness in digital steganography. Key technical implementations include:
* **Bit-Plane Manipulation:** Direct modification of pixel color channels using the `Pillow` library.
* **Robustness Algorithms:** Implementation of the **Kutter-Jordan-Bossen** method, which utilizes blue channel brightness modification for resistance against basic image processing.
* **Security Layers:** Use of **Pseudo-Random Interval (PRI)** sequences to distribute data unpredictably across the carrier image, preventing simple statistical analysis.
* **GUI Integration:** Event-driven architecture using `tkinter` to bridge complex backend algorithms with a user-friendly interface.
