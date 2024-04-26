import pycdlib
import os.path

from io import BytesIO
from pathlib import Path
from tkinter import filedialog


LOADER_NAME = "CDTVBaSS"
LOADER_BYTES = LOADER_NAME.encode("ascii")
ORIGINAL_BYTES = b"steelsky"
assert len(LOADER_BYTES) == len(ORIGINAL_BYTES)


if __name__ == "__main__":
    isoname = filedialog.askopenfilename(
        title="Choose Beneath a Steel Sky CD image",
        filetypes=[("ISO files", "*.iso")]
    )
    with open(isoname, 'rb') as f:
        contents = f.read()

    iso = pycdlib.PyCdlib()
    iso.open_fp(BytesIO(contents))

    # change the startup sequence to run the loader instead
    startup_sequence = BytesIO()
    iso.get_file_from_iso_fp(startup_sequence, iso_path='/s/startup-sequence;1')
    new_value = startup_sequence.getvalue().replace(ORIGINAL_BYTES, LOADER_BYTES)
    print(new_value)
    startup_sequence = BytesIO(new_value)
    iso.modify_file_in_place(
        fp=startup_sequence,
        length=len(new_value),
        iso_path='/s/startup-sequence;1',
    )

    # add uae/dh0/BaSSLoader to the ISO
    with open(os.path.join(os.path.dirname(__file__), "uae", "dh0", "BaSSLoader"), "rb") as f:
        loader = f.read()
    iso.add_fp(
        fp=BytesIO(loader),
        length=len(loader),
        iso_path=(b"/" + LOADER_BYTES + b";1").decode("ascii"),
    )
    iso.force_consistency()
    patched_name = Path(isoname).with_name(f"{Path(isoname).stem}-patched{Path(isoname).suffix}")
    print("Saving patched ISO", patched_name)

    iso.write(patched_name)
    iso.close()
