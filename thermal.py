import re
import cv2
import pytesseract
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def extract_max_temperature(image_path):
    # Load image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # OCR
    text = pytesseract.image_to_string(gray)

    # Regex patterns
    temp_patterns = {
        "C": [
            r'(\d+\.?\d*)\s?°\s?[Cc]',
            r'(\d+\.?\d*)\s?[Cc]',
            r'(\d+\.?\d*)\s?deg\s?[Cc]',
        ],
        "F": [
            r'(\d+\.?\d*)\s?°\s?[Ff]',
            r'(\d+\.?\d*)\s?[Ff]',
            r'(\d+\.?\d*)\s?deg\s?[Ff]',
        ]
    }

    temperatures = []

    for unit, patterns in temp_patterns.items():
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match)
                    temperatures.append((value, unit))
                except ValueError:
                    pass

    if temperatures:
        max_temp = max(temperatures, key=lambda x: x[0])
        return f"Max temperature in thermal camera field of view: {max_temp[0]} °{max_temp[1]}"
    else:
        return "No temperature references found."

def launch_gui(image_path, result_text):
    root = tk.Tk()
    root.title("Spot Thermal Camera Analytics")

    # Title (48 after 20% reduction)
    title_label = ttk.Label(root, text="Spot Thermal Camera Analytics",
                            font=("Helvetica", 48, "bold"))
    title_label.pack(pady=20)

    # Result text (2x large font)
    result_label = ttk.Label(root, text=result_text,
                             font=("Helvetica", 28))
    result_label.pack(pady=10)

    # Display image (resized to 400x400)
    try:
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        img_label = ttk.Label(root, image=tk_img)
        img_label.image = tk_img  # Keep reference
        img_label.pack(pady=10)
    except Exception as e:
        error_label = ttk.Label(root, text=f"Error loading image: {e}",
                                font=("Helvetica", 18), foreground="red")
        error_label.pack(pady=10)

    # Exit button
    exit_button = ttk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    image_file = "photo.jpg"  # Replace with your actual file
    result = extract_max_temperature(image_file)
    launch_gui(image_file, result)
