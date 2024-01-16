import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os


class VideoCutterApp:
    def __init__(self, master):
        self.master = master
        master.title("Découpage de Vidéo")

        self.input_file_var = tk.StringVar()
        self.num_segments_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()
        self.output_format_var = tk.StringVar(value=".mp4")
        self.video_duration_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Fichier Vidéo:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        entry_file = tk.Entry(self.master, width=40, textvariable=self.input_file_var)
        entry_file.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        tk.Button(self.master, text="Parcourir", command=self.browse_file).grid(
            row=0, column=3, padx=5, pady=5
        )

        tk.Label(self.master, text="Durée de la Vidéo:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        tk.Label(self.master, textvariable=self.video_duration_var).grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )

        tk.Label(self.master, text="Nombre de Segments:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        entry_segments = tk.Entry(
            self.master, width=5, textvariable=self.num_segments_var
        )
        entry_segments.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Dossier de Sortie:").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        entry_output_folder = tk.Entry(
            self.master, width=40, textvariable=self.output_folder_var
        )
        entry_output_folder.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(
            self.master, text="Parcourir", command=self.browse_output_folder
        ).grid(row=3, column=2, padx=5, pady=5)

        tk.Label(self.master, text="Format de Sortie:").grid(
            row=4, column=0, padx=5, pady=5, sticky="e"
        )
        entry_output_format = tk.Entry(
            self.master, width=5, textvariable=self.output_format_var
        )
        entry_output_format.grid(row=4, column=1, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(
            self.master, orient="horizontal", length=300, mode="determinate"
        )
        self.progress_bar.grid(row=5, column=0, columnspan=4, pady=10)

        tk.Button(
            self.master,
            text="Découper Vidéo",
            command=self.start_processing,
        ).grid(row=6, column=0, columnspan=4, pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.input_file_var.set(filename)

        duration = self.get_duration(filename)
        if duration is not None:
            self.video_duration_var.set(f"{round(duration, 2)} secondes")

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        self.output_folder_var.set(folder)

    def start_processing(self):
        input_file = self.input_file_var.get()
        num_segments = int(self.num_segments_var.get())
        output_folder = self.output_folder_var.get()
        output_format = self.output_format_var.get()

        if not input_file or not num_segments or not output_folder:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        self.progress_bar["value"] = 0
        self.decoupage_video(input_file, num_segments, output_folder, output_format)

    def decoupage_video(self, input_file, num_segments, output_folder, output_format):
        total_duration = self.get_duration(input_file)

        if total_duration is None:
            return

        segment_duration = total_duration / num_segments

        start_time = 0
        end_time = segment_duration

        segment_number = 1

        output_folder = os.path.join(os.getcwd(), output_folder)
        os.makedirs(output_folder, exist_ok=True)

        for _ in range(num_segments):
            try:
                output_file = os.path.join(
                    output_folder, f"output_{segment_number}{output_format}"
                )
                ffmpeg_extract_subclip(
                    input_file, start_time, end_time, targetname=output_file
                )

                start_time = end_time
                end_time += segment_duration
                segment_number += 1

                self.update_progress(start_time, total_duration)
            except Exception as e:
                print(f"Ignoré une erreur lors de la découpe de la vidéo : {e}")

        print("Fin du processus de découpe")

        self.input_file_var.set("")
        self.num_segments_var.set("")
        self.output_folder_var.set("")
        self.output_format_var.set(".mp4")
        self.video_duration_var.set("")
        self.progress_bar["value"] = 0

    def update_progress(self, current_time, total_duration):
        progress_value = (current_time / total_duration) * 100
        self.progress_bar["value"] = progress_value
        self.progress_bar.update_idletasks()

    def get_duration(self, input_file):
        try:
            with VideoFileClip(input_file) as video_clip:
                total_duration = video_clip.duration
            return total_duration
        except OSError:
            print("Le fichier n'existe pas")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCutterApp(root)
    root.mainloop()
