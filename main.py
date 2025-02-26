import tkinter as tk
from tkinter import filedialog, scrolledtext
import pyttsx3
import fitz
import threading


class AudioBook:
    def __init__(self, window):
        self.root = window
        self.root.geometry("1920x1080")
        self.root.title("AudioBook App")
        photo = tk.PhotoImage(file="icon.png")
        root.wm_iconphoto(False, photo)
        self.is_pause = False
        self.is_reading = False

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 150)  # Adjust speech rate
        self.engine.setProperty("volume", 0.7)  # Set volume
        voices = self.engine.getProperty("voices")  # get voices
        self.engine.setProperty("voice", voices[14].id)

        self.text_area = scrolledtext.ScrolledText(
            window, wrap=tk.WORD, width=50, height=10
        )
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack()

        self.open_btn = tk.Button(
            self.btn_frame, text="Open file", command=self.open_file
        )
        self.open_btn.grid(row=0, column=0, padx=5, pady=5)

        self.play_btn = tk.Button(self.btn_frame, text="Play", command=self.play)
        self.play_btn.grid(row=0, column=1, padx=5, pady=5)

        self.stop_btn = tk.Button(self.btn_frame, text="Stop", command=self.stop)
        self.stop_btn.grid(row=0, column=4, padx=5, pady=5)

        self.text_content = ""

    def open_file(self):
        file_path = filedialog.askopenfile(filetypes=[("Pdf file", "*.pdf")])
        if file_path:
            try:
                doc = fitz.open(file_path)
                extracted_text = []

                for page in doc:
                    text = page.get_text("text")
                    if isinstance(text, list):
                        text = "\n".join(map(str, text))
                    extracted_text.append(text)

                text = "\n".join(extracted_text)

                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, text)

            except Exception as e:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, "Error opening file: " + str(e))

    def speak(self, text):
        self.is_reading = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_reading = False

    def play(self):
        if not self.is_reading:
            text = self.text_area.get(1.0, tk.END).strip()
            if text:
                thread = threading.Thread(target=self.speak, args=(text,))
                thread.start()

    def pause(self):
        self.engine.stop()
        self.is_pause = True

    def resume(self):
        if self.is_pause:
            self.play()
            self.is_reading = True

    def stop(self):
        self.engine.stop()
        self.is_reading = False


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioBook(root)
    root.mainloop()
