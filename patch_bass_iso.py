from io import BytesIO
from pathlib import Path
from tkinter import filedialog


if __name__ == "__main__":
    old_value = b"steelsky\n\n"
    new_value = b"echo    \n\n"
    assert len(new_value) == len(old_value), len(new_value)
    isoname = filedialog.askopenfilename(
        title="Choose Beneath a Steel Sky CD image",
        filetypes=[("ISO files", "*.iso")]
    )
    with open(isoname, 'rb') as f:
        contents = f.read()
    patched_name = Path(isoname).with_name(f"{Path(isoname).stem}-patched{Path(isoname).suffix}")
    print("Saving patched ISO", patched_name)
    with open(patched_name, 'wb') as f:
        f.write(contents.replace(old_value, new_value))
