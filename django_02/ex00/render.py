import os
import sys

SETTINGS_FILE = "settings.py"


def read_settings(path):
    """Read 'key = value' lines from settings.py into a dict."""
    settings = {}
    with open(path, "r") as f:
        for line in f:
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            settings[key] = value
    return settings


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <file.template>")
        return

    path = sys.argv[1]
    if not path.endswith(".template"):
        print("Error: the file must have a .template extension")
        return
    if not os.path.isfile(path):
        print(f"Error: '{path}' does not exist")
        return

    settings_path = os.path.join(os.path.dirname(__file__), SETTINGS_FILE)
    if not os.path.isfile(settings_path):
        print(f"Error: {SETTINGS_FILE} not found")
        return

    settings = read_settings(settings_path)

    with open(path, "r") as f:
        content = f.read()

    try:
        content = content.format(**settings)
    except KeyError as e:
        print(f"Error: {e} is not defined in {SETTINGS_FILE}")
        return

    with open(path[:-len(".template")] + ".html", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
