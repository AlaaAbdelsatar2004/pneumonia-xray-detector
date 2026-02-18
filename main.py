# main.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from predict import predict_pneumonia

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PneumoniaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PneumoAI - Chest X-Ray Analyzer")
        self.geometry("1200x850")
        self.configure(fg_color="#f8fafc")

        # Header (top bar - fixed height)
        self.header = ctk.CTkFrame(self, fg_color="#1e40af", corner_radius=0, height=120)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)  # يمنع التغيير في الارتفاع

        ctk.CTkLabel(self.header, text="PneumoAI", font=("Segoe UI", 42, "bold"), text_color="white").pack(pady=(20, 5))
        ctk.CTkLabel(self.header, text="AI-Powered Diagnostic Tool for Chest X-Rays",
                     font=("Segoe UI", 18), text_color="#dbeafe").pack()

        # Content frame (below header)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Grid inside content frame
        content_frame.grid_columnconfigure(0, weight=1)  # Left: Image
        content_frame.grid_columnconfigure(1, weight=0)  # Right: Result
        content_frame.grid_rowconfigure(0, weight=1)

        # Left side - Image & Upload
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        upload_frame = ctk.CTkFrame(left_frame, fg_color="#ffffff", corner_radius=20, border_width=2, border_color="#e2e8f0")
        upload_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(upload_frame, text="Select Chest X-Ray Image", font=("Segoe UI", 24, "bold"), text_color="#1e293b").pack(pady=20)

        self.upload_btn = ctk.CTkButton(upload_frame, text="Browse Image", command=self.upload_image,
                                        width=320, height=70, font=("Segoe UI", 18, "bold"), corner_radius=12,
                                        fg_color="#3b82f6", hover_color="#2563eb")
        self.upload_btn.pack(pady=30)

        self.image_label = ctk.CTkLabel(upload_frame, text="No image selected", font=("Segoe UI", 16), text_color="#64748b")
        self.image_label.pack(pady=10)

        self.photo = None

        # Right side - Result Sidebar
        right_frame = ctk.CTkFrame(content_frame, fg_color="#f8fafc", corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_propagate(False)
        right_frame.configure(width=400)

        ctk.CTkLabel(right_frame, text="Diagnostic Result", font=("Segoe UI", 26, "bold"), text_color="#1e293b").pack(pady=30)

        self.result_label = ctk.CTkLabel(right_frame, text="Upload an image to receive analysis",
                                         font=("Segoe UI", 22, "bold"), text_color="#1e293b", wraplength=350, justify="center")
        self.result_label.pack(pady=20, padx=20)

        self.prob_label = ctk.CTkLabel(right_frame, text="", font=("Segoe UI", 20), text_color="#475569", justify="center")
        self.prob_label.pack(pady=10)

        self.clear_btn = ctk.CTkButton(right_frame, text="Clear Result", command=self.clear_result,
                                       width=220, height=50, font=("Segoe UI", 16), fg_color="#ef4444", hover_color="#dc2626")
        self.clear_btn.pack(pady=40)

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not path:
            return

        try:
            img = Image.open(path)
            img.thumbnail((600, 600), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.photo, text="")
            self.image_label.image = self.photo
        except Exception as e:
            messagebox.showerror("Error", f"Cannot display image: {str(e)}")
            return

        self.result_label.configure(text="Analyzing... (10-30 seconds)", text_color="blue")
        self.prob_label.configure(text="")
        self.update_idletasks()

        result, conf = predict_pneumonia(path)

        color = "green" if "Normal" in result else "red"
        self.result_label.configure(text=f"Diagnosis: {result}", text_color=color, font=("Segoe UI", 28, "bold"))
        self.prob_label.configure(text=f"Confidence: {conf:.2f}%", text_color=color, font=("Segoe UI", 22, "bold"))
        self.update_idletasks()

    def clear_result(self):
        self.image_label.configure(image=None, text="No image selected")
        self.result_label.configure(text="Upload an image to receive analysis", text_color="#1e293b", font=("Segoe UI", 22, "bold"))
        self.prob_label.configure(text="")
        self.photo = None

if __name__ == "__main__":
    app = PneumoniaApp()
    app.mainloop()