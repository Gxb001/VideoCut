from pytube import YouTube
from threading import Thread
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class VideoDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Téléchargement de Vidéo")

        self.input_link_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()
        self.output_extension_var = tk.StringVar(value=".mp4")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Lien de la Vidéo:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        entry_link = tk.Entry(self.master, width=40, textvariable=self.input_link_var)
        entry_link.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(self.master, text="Dossier de Téléchargement:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        entry_output_folder = tk.Entry(
            self.master, width=40, textvariable=self.output_folder_var
        )
        entry_output_folder.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        tk.Button(self.master, text="Parcourir", command=self.browse_folder).grid(
            row=1, column=3, padx=5, pady=5
        )

        tk.Label(self.master, text="Extension de Sortie:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        entry_output_extension = tk.Entry(
            self.master, width=5, textvariable=self.output_extension_var
        )
        entry_output_extension.grid(row=2, column=1, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(
            self.master, orient="horizontal", length=300, mode="determinate"
        )
        self.progress_bar.grid(row=3, column=0, columnspan=4, pady=10)

        tk.Button(
            self.master,
            text="Télécharger Vidéo",
            command=self.start_downloading,
        ).grid(row=4, column=0, columnspan=4, pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_var.set(folder_path)

    def start_downloading(self):
        link = self.input_link_var.get()
        output_folder = self.output_folder_var.get()
        output_extension = self.output_extension_var.get()

        if not link or not output_folder:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        self.progress_bar["value"] = 0

        try:
            Thread(
                target=self.download_video,
                args=(link, output_folder, output_extension),
            ).start()
        except Exception as e:
            self.master.after(1000, lambda error=e: self.show_error_message(error))

    def download_video(self, link, output_folder, output_extension):
        try:
            yt = YouTube(link)
            video_stream = yt.streams.filter(
                file_extension="mp4", progressive=True
            ).first()

            default_filename = "video"
            output_file = os.path.join(output_folder, f"{default_filename}{output_extension}")
            video_stream.download(output_folder, filename=default_filename+output_extension)

            self.progress_bar["value"] = 100
            self.master.after(1000, lambda: self.show_success_message(output_file))
        except Exception as e:
            self.master.after(1000, lambda error=e: self.show_error_message(error))

    def show_success_message(self, output_file):
        messagebox.showinfo(
            "Succès", f"La vidéo a été téléchargée avec succès à {output_file}"
        )

    def show_error_message(self, error):
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
