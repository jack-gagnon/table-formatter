
import re
import pyperclip


def format_table(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Remove Markdown code fences if present.
    lines = [
        line for line in lines
        if not line.startswith("```")
    ]

    if len(lines) < 2:
        raise ValueError("No valid Markdown table found.")

    rows = []

    for line in lines:
        # Allow tables with or without outer pipes.
        line = line.strip().strip("|")

        cells = [
            cell.strip()
            for cell in re.split(r"(?<!\\)\|", line)
        ]

        rows.append(cells)

    columns = len(rows[0])

    if any(len(row) != columns for row in rows):
        raise ValueError("Table rows have inconsistent columns.")

    # Validate separator row.
    if not all(
        re.fullmatch(r":?-{3,}:?", cell)
        for cell in rows[1]
    ):
        raise ValueError("Invalid Markdown separator row.")

    # Calculate widths, excluding separator row.
    content_rows = [rows[0]] + rows[2:]

    widths = [
        max(3, *(len(row[i]) for row in content_rows))
        for i in range(columns)
    ]

    def format_row(row):
        cells = [
            row[i].ljust(widths[i])
            for i in range(columns)
        ]
        return "| " + " | ".join(cells) + " |"

    separator = (
        "| " +
        " | ".join("-" * width for width in widths) +
        " |"
    )

    output = [
        format_row(rows[0]),
        separator
    ]

    output.extend(format_row(row) for row in rows[2:])

    return "\n".join(output)


def main():
    print("Markdown Table Formatter")
    print("------------------------")

    try:
        original = pyperclip.paste()

        if not original.strip():
            print("Clipboard is empty.")
            return

        formatted = format_table(original)

        pyperclip.copy(formatted)

        print("Success! Formatted table copied to clipboard.")
        print()
        print(formatted)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
