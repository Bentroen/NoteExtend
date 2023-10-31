import sys
import tkinter as tk
from tkinter import filedialog

from noteextend.main import generate_pack


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


def request_nbs_file() -> str:
    filename = filedialog.askopenfilename(
        title="Select a NBS file", filetypes=[("Note Block Song", "*.nbs")]
    )
    return filename


def request_output_path() -> str:
    folder = filedialog.askdirectory(title="Select an output folder")
    return folder


def main():
    window = tk.Tk()
    window.title("NoteExtend")
    window.configure(padx=10)
    window.configure(background="#f0f0f0")

    label = tk.Label(
        window,
        text="Select a NBS file and an output folder to begin.\nClick 'Generate' to generate the resource pack.",
        pady=10,
    )
    label.grid(row=0, columnspan=3)

    # Create two file input fields, one for the NBS file and one for the output folder
    song_path = tk.StringVar()
    output_path = tk.StringVar()

    song_path_label = tk.Label(window, text="NBS file", width=12, anchor="e")
    output_path_label = tk.Label(window, text="Output folder", width=12, anchor="e")

    song_path_entry = tk.Entry(
        window, textvariable=song_path, state="disabled", width=50
    )
    output_path_entry = tk.Entry(
        window, textvariable=output_path, state="disabled", width=50
    )

    # Create a button to pick the NBS file
    def pick_nbs_file():
        song_path.set(request_nbs_file())
        update_convert_button_state()

    song_path_button = tk.Button(
        window, text="Select...", command=pick_nbs_file, width=12
    )

    # Create a button to pick the output folder
    def pick_output_folder():
        output_path.set(request_output_path())
        update_convert_button_state()

    output_path_button = tk.Button(
        window, text="Select...", command=pick_output_folder, width=12
    )

    song_path_label.grid(column=0, row=1)
    song_path_button.grid(column=1, row=1, padx=5, pady=5)
    song_path_entry.grid(column=2, row=1)

    output_path_label.grid(column=0, row=2)
    output_path_button.grid(column=1, row=2, padx=5, pady=5)
    output_path_entry.grid(column=2, row=2)

    # Create a button to start the conversion
    def convert():
        generate_pack(song_path.get(), output_path.get(), callback=window.update)

    def update_convert_button_state():
        if output_path.get() != "" and song_path.get() != "":
            convert_button.configure(state="normal")
        else:
            convert_button.configure(state="disabled")

    convert_button = tk.Button(
        window, text="Generate", command=convert, width=20, state="disabled"
    )
    convert_button.grid(row=3, columnspan=3, pady=10)

    # Create a text box to display the conversion progress
    output_text = tk.Text(window, wrap="word", width=50, height=10, state="disabled")
    output_text.grid(row=4, columnspan=3, sticky="nsew", padx=5, pady=5)
    output_text.tag_configure("stdout", foreground="black")
    output_text.tag_configure("stderr", foreground="red")

    sys.stdout = TextRedirector(output_text, "stdout")
    sys.stderr = TextRedirector(output_text, "stderr")

    # Start the window's main loop
    window.mainloop()


if __name__ == "__main__":
    main()
