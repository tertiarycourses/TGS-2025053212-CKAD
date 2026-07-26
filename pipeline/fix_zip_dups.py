"""
Fix ZIP duplicate entries in a PPTX file.
python-pptx sometimes writes duplicate slide XML entries when saving
a file that already had duplicate entries (from earlier builds).

This script re-packages the PPTX keeping only the LAST occurrence of
each duplicate entry (matching python-pptx's read behaviour).
"""
import sys, os, zipfile, shutil, tempfile

def fix(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    tmp = tempfile.mktemp(suffix=".pptx")
    seen = {}
    with zipfile.ZipFile(input_path, 'r') as zin:
        entries = zin.infolist()
        # Build last-occurrence index
        for info in entries:
            seen[info.filename] = info  # last one wins

        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for name, info in seen.items():
                data = zin.read(name)
                zout.writestr(info, data)

    shutil.move(tmp, output_path)
    dup_count = len(entries) - len(seen)
    print(f"Fixed: {len(entries)} entries -> {len(seen)} (removed {dup_count} duplicates)")
    print(f"Saved to: {output_path}")
    return dup_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_zip_dups.py <input.pptx> [output.pptx]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    fix(inp, out)
