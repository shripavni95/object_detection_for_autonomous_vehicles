import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from detector import ObjectDetector

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection for Autonomous Vehicles")
        self.root.geometry("800x600")

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Buttons
        self.load_button = tk.Button(self.root, text="Load Image/Video", command=self.load_file)
        self.load_button.pack(pady=10)

        self.detect_button = tk.Button(self.root, text="Run Object Detection", command=self.run_detection)
        self.detect_button.pack(pady=10)

        self.file_path = None

        # Initialize Object Detector
        self.detector = ObjectDetector()

    def load_file(self):
        file_types = [("Image/Video Files", "*.jpg *.jpeg *.png *.mp4 *.avi")]
        self.file_path = filedialog.askopenfilename(title="Select Image or Video",  filetypes=file_types)

        if self.file_path:
            if self.file_path.lower().endswith((".jpg", ".jpeg", ".png")):
                self.display_image(self.file_path)
            elif self.file_path.lower().endswith((".mp4", ".avi")):
                messagebox.showinfo("Info", "Video loaded. Object detection will run on it.")

    def display_image(self, path):
        image = Image.open(path)
        image = image.resize((600, 400))
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

    def run_detection(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please load an image or video first.")
            return

        if self.file_path.lower().endswith((".jpg", ".jpeg", ".png")):
            detected_image = self.detector.detect_image(self.file_path)
            self.display_detected_image(detected_image)
        elif self.file_path.lower().endswith((".mp4", ".avi")):
            messagebox.showinfo("Info", "Video detection is under development.")

    def display_detected_image(self, image):
        img = Image.fromarray(image)
        img = img.resize((600, 400))
        photo = ImageTk.PhotoImage(img)

        self.image_label.config(image=photo)
        self.image_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()
