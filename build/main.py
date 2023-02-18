import tkinter
from tkinter import filedialog
import sys
import os
from file_manager import FileManager
from data_processor import DataProcessor


class MainGui(tkinter.Tk):
    """Main tkinter GUI."""

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.eval('tk::PlaceWindow . center')
        self.iconbitmap(default="convert.ico")
        self.title(".ASC converter")
        self.resizable(False, False)
        path = tkinter.StringVar(
            self,
            value=os.path.join(os.getcwd(), "output"))
        self.convert_or_merge = tkinter.IntVar()
        self.convert_or_merge.set(1)
        self.after_execution = tkinter.IntVar()
        self.after_execution.set(1)

        tkinter.Label(
            text="Output File Path:").grid(
                row=2, column=0, padx=10, pady=10)
        self.output_path_entry = tkinter.Entry(
            textvariable=path, width=40)
        # need to grid separately to use .get()
        self.output_path_entry.grid(
            row=2, column=1, columnspan=2, padx=5, pady=5)
        tkinter.Button(
            text="Browse", command=self.browse_output, width=11).grid(
                row=2, column=3, padx=10, pady=10)

        tkinter.Label(
            text="After execution:").grid(
                row=3, column=0, columnspan=2, sticky='W', padx=5)
        tkinter.Radiobutton(
            text="Open file",
            variable=self.after_execution,
            value=1,
            tristatevalue=0).grid(
                row=4, column=0, sticky='W', padx=10)
        tkinter.Radiobutton(
            text="Open folder",
            variable=self.after_execution,
            value=2,
            tristatevalue=0).grid(
                row=4, column=1, sticky='W')
        tkinter.Radiobutton(
            text="Do nothing",
            variable=self.after_execution,
            value=3,
            tristatevalue=0).grid(
                row=4, column=2, sticky='W')

        tkinter.Button(
            text='Convert',
            width=12,
            command=lambda: self.execute_process(merge=False)).grid(
                row=5, column=1,  padx=5, pady=10, sticky='E')
        tkinter.Button(
            text='Merge',
            width=12,
            command=lambda: self.execute_process(merge=True)).grid(
                row=5, column=2,  padx=5, pady=10)
        tkinter.Button(
            text='Cancel',
            width=12,
            command=sys.exit).grid(
                row=5, column=3,  padx=5, pady=10, sticky='W')

    def execute_process(self, merge=bool):
        """Choose input file(s), process them and create output file."""
        list_of_files = FileManager().file_selector(merge)
        for idx, file in enumerate(list_of_files):
            imported_data = FileManager().import_data(file)
            partnumber, data = DataProcessor().data_cleaner(
                imported_data)
            if idx == 0:
                final_data = data
            else:
                final_data.extend(data[1:])

        if self.after_execution.get() == 1:
            open_file = True
        elif self.after_execution.get() == 2:
            open_file = False
        else:
            open_file = None

        output_path = self.output_path_entry.get()
        FileManager().create_output_file(
            data=final_data,
            output_path=output_path,
            partnumber=partnumber,
            open_file=open_file
            )

    def browse_output(self):
        """Browse file system for output folder."""
        path = filedialog.askdirectory(
            initialdir=os.getcwd(),
            title="Choose output directory")
        self.output_path_entry.delete(0, tkinter.END)
        self.output_path_entry.insert(0, path)


if __name__ == "__main__":
    main_gui = MainGui()
    main_gui.mainloop()
