def run_txt_script(lines, hid):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        if line.startswith("WAIT:"):
            ms = int(line[5:])
            hid.wait(ms)

        elif line.startswith("PRESS:"):
            key = line[6:]
            hid.press(key)

        elif line.startswith("RELEASE:"):
            key = line[8:]
            hid.release(key)

        elif line.startswith("CLICK:"):
            btn = line[6:]
            hid.click(btn)

        elif line.startswith("MOVE:"):
            parts = line[5:].split(":")
            dx, dy = int(parts[0]), int(parts[1])
            hid.move(dx, dy)

        elif line.startswith("TYPE:"):
            text = line[5:]
            hid.type_text(text)

        elif line.startswith("PRESS_AND_RELEASE:"):
            key = line[18:]
            hid.press_and_release(key)

        elif line.startswith("COMBO:"):
            keys = [k.strip() for k in line[6:].split(",")]
            hid.combo(keys)

        elif line.startswith("REPEAT:"):
            count = int(line[7:].split("{")[0])
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "}":
                block.append(lines[i].strip())
                i += 1
            for _ in range(count):
                run_txt_script(block, hid)

        i += 1
