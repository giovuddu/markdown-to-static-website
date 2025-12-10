from pathlib import Path
import shutil
import re
from parser import markdown_to_html_node


def gen_public():
    here = Path(__file__).resolve().parent
    project_root = here.parent
    static_dir = project_root / "static"
    public_dir = project_root / "public"

    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir()

    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)


def extract_title(markdown: str) -> str:
    match = re.match(r"^# (.*?)\n\n", markdown.strip(), re.DOTALL)
    if match is None:
        raise Exception("no header no bueno >:(")  # ):<

    return match.group(1).strip()


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as file:
            content = file.read()
        with open(template_path, "r") as file:
            template = file.read()
    except Exception as exc:
        print(exc)
        exit(1)

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    html_text = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    try:
        with open(dest_path, "w") as file:
            file.write(html_text)
    except Exception as exc:
        print(exc)
        exit(1)


def main():
    gen_public()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
