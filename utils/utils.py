def escape_html_symbols(text: str) -> str:
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    return "".join(html_escape_table.get(c, c) for c in text)
