def get_flp_mode(flp_paths):
    results = []

    for path in flp_paths:
        try:
            with open(path, "rb") as file:
                file.seek(0x44)  # Offset 0x44 = 68 decimal
                byte = file.read(1)

                if not byte:
                    mode = "unknown"
                elif byte == b'\x20':
                    mode = "song_mode"
                elif byte in (b'\x00', b'\x01'):
                    mode = "pattern_mode"
                else:
                    mode = f"unknown_byte_{byte.hex()}"

                results.append((path, mode))

        except Exception as e:
            results.append((path, f"error: {str(e)}"))

    return results


"""
B song
Web pattern
"""

flp_files = [
    r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BEYKEL\B.flp",
    r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BEYKEL\Web.flp"
]

modes = get_flp_mode(flp_files)

for path, mode in modes:
    print(f"{path} → {mode}")


def dump_flp_header(flp_path, byte_count=128):
    with open(flp_path, "rb") as file:
        header = file.read(byte_count)
    print(f"\nHex dump of {flp_path} (first {byte_count} bytes):")
    print(" ".join(f"{b:02X}" for b in header))


#dump_flp_header(
    #r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BEYKEL\Web_pattern.flp")
#dump_flp_header(
    #r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BEYKEL\Web_song.flp")
