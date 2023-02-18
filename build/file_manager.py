from tkinter import filedialog
import os
from datetime import datetime
import csv


class FileManager():
    """Select, import and create files."""

    def __init__(self):
        pass

    def file_selector(self, merge=bool):
        """Select file(s) via Tkinter filedialog"""

        list_of_files = []
        filetypes = "ASC files", ".ASC .asc"
        initialdir = os.getcwd()

        if not merge:
            file = filedialog.askopenfilename(
                initialdir=initialdir,
                title='Open .ASC File to convert',
                filetypes=[(filetypes)]
                )
            list_of_files.append(file)
            return list_of_files

        list_of_files = filedialog.askopenfilenames(
            initialdir=initialdir,
            title='Open .ASC Files to merge',
            filetypes=[(filetypes)]
            )
        return list_of_files

    def import_data(self, file):
        """Get data from files."""

        with open(file, encoding="ISO-8859-1") as file_to_convert:
            data = file_to_convert.read().splitlines()
        return data

    def create_output_file(
            self, data, output_path, partnumber, open_file):
        """Create an output .csv file."""

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(
            output_path, f"{partnumber}_{now}.csv")

        with open(path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(data)

        # open output file or folder
        if open_file:
            os.startfile(path)
            return
        os.system(output_path)
        return
