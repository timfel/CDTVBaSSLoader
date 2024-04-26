import pycdlib
import os.path

from io import BytesIO
from pathlib import Path
from tkinter import filedialog


if __name__ == "__main__":
    isoname = filedialog.askopenfilename(
        title="Choose Beneath a Steel Sky CD image",
        filetypes=[("ISO files", "*.iso")]
    )
    with open(isoname, 'rb') as f:
        contents = f.read()

    iso = pycdlib.PyCdlib()
    iso.open_fp(BytesIO(contents))

    # change the startup sequence to run a cli and thus turn on the screen
    startup_sequence = BytesIO()
    iso.get_file_from_iso_fp(startup_sequence, iso_path='/s/startup-sequence;1')
    new_value = b"newcli\n" + startup_sequence.getvalue()
    startup_sequence = BytesIO(new_value)
    iso.modify_file_in_place(
        fp=startup_sequence,
        length=len(new_value),
        iso_path='/s/startup-sequence;1',
    )

    iso.write(
        filedialog.asksaveasfilename(
            title="Save patched ISO",
            filetypes=[("ISO files", "*.iso")]
        )
    )
    iso.close()
