import sys

INPUT_FILE = "periodic_table.txt"
OUTPUT_FILE = "periodic_table.html"
CSS_FILE = "periodic_table.css"
COLUMNS = 18

CSS = """\
body {
  font-family: Arial, Helvetica, sans-serif;
  margin: 20px;
}

caption {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 20px;
}

table {
  border-collapse: collapse;
  margin: 0 auto;
}

td {
  padding: 10px;
  vertical-align: top;
}

td.element {
  border: 1px solid black;
  background-color: #f5f5f5;
}

td.element h4 {
  margin: 0 0 5px 0;
}

td.element ul {
  margin: 0;
  padding-left: 15px;
  font-size: 12px;
}
"""


def parse_line(line):
    """'Hydrogen = position:0, number:1, ...' -> dict of the element."""
    name, attributes = line.split("=")
    element = {"name": name.strip()}
    for attribute in attributes.split(","):
        key, value = attribute.split(":")
        element[key.strip()] = value.strip()
    element["position"] = int(element["position"])
    return element


def read_elements(filename):
    with open(filename, "r") as f:
        return [parse_line(line) for line in f if line.strip()]


def split_into_rows(elements):
    """Start a new row each time the position goes back to the left."""
    rows = []
    previous = COLUMNS
    for element in elements:
        if element["position"] <= previous:
            rows.append([])
        rows[-1].append(element)
        previous = element["position"]
    return rows


def electron_text(electron):
    total = sum(int(n) for n in electron.split())
    return f"{total} electron" if total == 1 else f"{total} electrons"


def element_cell(element):
    return (
        f'      <td class="element">\n'
        f'        <h4>{element["name"]}</h4>\n'
        f'        <ul>\n'
        f'          <li>No {element["number"]}</li>\n'
        f'          <li>{element["small"]}</li>\n'
        f'          <li>{element["molar"]}</li>\n'
        f'          <li>{electron_text(element["electron"])}</li>\n'
        f'        </ul>\n'
        f'      </td>\n'
    )


def empty_cell():
    return '      <td class="empty"></td>\n'


def table_row(row):
    """Build one <tr>, filling the gaps between elements with empty cells."""
    html = "    <tr>\n"
    column = 0
    for element in row:
        while column < element["position"]:
            html += empty_cell()
            column += 1
        html += element_cell(element)
        column += 1
    while column < COLUMNS:
        html += empty_cell()
        column += 1
    html += "    </tr>\n"
    return html


def generate_html(rows):
    body = "".join(table_row(row) for row in rows)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>Periodic Table of the Elements</title>\n"
        f'  <link rel="stylesheet" href="{CSS_FILE}">\n'
        "</head>\n"
        "<body>\n"
        "  <table>\n"
        "    <caption>Periodic Table of the Elements</caption>\n"
        f"{body}"
        "  </table>\n"
        "</body>\n"
        "</html>\n"
    )


def main():
    try:
        elements = read_elements(INPUT_FILE)
        #print(elements)
    except OSError as e:
        print(f"Error: cannot read {INPUT_FILE}: {e.strerror}", file=sys.stderr)
        sys.exit(1)

    rows = split_into_rows(elements)
    #print(rows)
    with open(OUTPUT_FILE, "w") as f:
        f.write(generate_html(rows))
    with open(CSS_FILE, "w") as f:
        f.write(CSS)


if __name__ == "__main__":
    main()
