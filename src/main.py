from pathlib import Path
import shutil
import re
from parser import markdown_to_html_node


def gen_public(project_root: Path):
    static_dir = project_root / "static"
    public_dir = project_root / "public"

    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)


def extract_title(markdown: str) -> str:
    match = re.match(r"^# (.*?)\n\n", markdown.strip(), re.DOTALL)
    if match is None:
        raise Exception("no header no bueno >:(")

    return match.group(1).strip()


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        content = from_path.read_text(encoding="utf-8")
        template = template_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(exc)
        raise

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    html_text = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(html_text, encoding="utf-8")


def generate_site(content_dir: Path, template_path: Path, public_dir: Path):
    for md_path in content_dir.rglob("*.md"):
        rel = md_path.relative_to(content_dir)
        out_rel = rel.with_suffix(".html")
        out_path = public_dir / out_rel

        generate_page(md_path, template_path, out_path)


def main():
    here = Path(__file__).resolve().parent
    project_root = here.parent

    content_dir = project_root / "content"
    template_path = project_root / "template.html"
    public_dir = project_root / "public"

    gen_public(project_root)
    generate_site(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()

