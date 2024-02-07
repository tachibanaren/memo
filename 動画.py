import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Player with Text Input")

        # Set window size
        self.master.geometry("800x630")  # ウィンドウサイズを調整

        # Create a frame for video display
        self.video_frame = tk.Frame(self.master)
        self.video_frame.pack()

        # Load the default video
        self.video_path = "background_image.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_canvas = tk.Canvas(self.video_frame, width=self.video_width, height=self.video_height)
        self.video_canvas.pack()

        # Load initial frame
        self.load_frame()

        # Create a frame for text input
        self.text_frame = tk.Frame(self.master)  # テキスト入力画面のサイズを調整
        self.text_frame.pack()

        # Text input field
        self.text_input = tk.Text(self.text_frame, height=30, width=75)
        self.text_input.pack(fill=tk.BOTH, expand=True)  # テキスト入力フィールドを水平方向に拡張

        # Create a frame for buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()  # ボタンフレームを配置

        # Button to save text to file
        self.save_button = tk.Button(self.button_frame, text="Save to File", command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT)

        # Button to open file dialog to load text from file
        self.load_button = tk.Button(self.button_frame, text="Load from File", command=self.load_from_file)
        self.load_button.pack(side=tk.LEFT)

        # Start video loop
        self.update_video()

        # Bind window resize event
        self.master.bind("<Configure>", self.resize)

    def load_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.current_frame))
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.master.after(20, self.load_frame)

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video when it ends
        self.master.after(20, self.update_video)

    def resize(self, event):
        window_width = event.width
        window_height = event.height

        # Adjust video frame size
        self.video_canvas.config(width=window_width, height=window_height - 30)

        # Adjust text input frame size
        self.text_frame.config(width=window_width)
        self.text_input.config(width=(window_width // 10))

    def save_to_file(self):
        text = self.text_input.get("1.0", tk.END)
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                file.write(text)

    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "r") as file:
                text = file.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", text)

def main():
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
