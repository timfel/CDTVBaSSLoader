from pathlib import Path
from tkinter import filedialog


if __name__ == "__main__":
    old_value = b"steelsky\n\n"
    new_value = b"newcli\nss\n"
    assert len(new_value) == len(old_value), len(new_value)
    old_name = b"SteelSky;1"
    new_name = b"ss;1" + b"\0" * (len(old_name) - len(b"ss;1"))
    assert len(new_name) == len(old_name), len(new_name)
    isoname = filedialog.askopenfilename(
        title="Choose Beneath a Steel Sky CD iso or bin",
        filetypes=[("ISO files", "*.iso"), ("BIN files", "*.bin")],
    )
    with open(isoname, 'rb') as f:
        contents = f.read()
    patched_name = Path(isoname).with_name(f"{Path(isoname).stem}-patched{Path(isoname).suffix}")
    print("Saving patched CD image", patched_name)
    with open(patched_name, 'wb') as f:
        f.write(contents.replace(old_value, new_value).replace(old_name, new_name))
