#!/usr/bin/env python3
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

BANNER = r"""
  ___    _    _         ___                 
 | __|__| |__| |___ _ _| __|__ _ _ __ _ ___ 
 | _/ _ \ / _` / -_) '_| _/ _ \ '_/ _` / -_)
 |_|\___/_\__,_\___|_| |_|\___/_| \__, \___|
                                  |___/     
"""

DEFAULT_IGNORED_FOLDERS = [
    "node_modules", "__pycache__", ".git", ".idea", ".vscode", "dist", "build", ".eggs", ".venv"
]

def create_folder_structure(base_path):
    folder_map = {}
    counter = [1]

    def add_folder(path):
        while True:
            console.print(f"\nCurrent path: [bold]{path}[/bold]")
            name = Prompt.ask(f"Enter subfolder name (or empty to stop)")
            if not name:
                return
            folder_path = path / name
            folder_path.mkdir(exist_ok=True)
            folder_map[counter[0]] = folder_path
            console.print(f"Created: {folder_path} [{counter[0]}]")
            counter[0] += 1

            if Confirm.ask(f"Does '{name}' have a subfolder?"):
                add_folder(folder_path)

    add_folder(base_path)
    return folder_map

def build_tree(path, show_files=False):
    tree = {}
    for p in sorted(path.iterdir()):
        if p.is_dir():
            tree[p.name] = build_tree(p, show_files)
        elif show_files:
            tree[p.name] = None
    return tree

def print_tree(d, prefix="", file_handle=None):
    items = list(d.items())
    for i, (name, subtree) in enumerate(items):
        connector = "└── " if i == len(items)-1 else "├── "

        # Only folders (dict) get "/"
        display_name = name + "/" if isinstance(subtree, dict) else name

        line = f"{prefix}{connector}{display_name}"
        console.print(line)
        if file_handle:
            print(line, file=file_handle)
        if isinstance(subtree, dict):
            extension = "    " if i == len(items)-1 else "│   "
            print_tree(subtree, prefix + extension, file_handle=file_handle)

def display_tree(base_path):
    tree_dict = build_tree(base_path)
    console.print(f"{base_path.name}/")
    print_tree(tree_dict)

def create_readmes(folder_map):
    console.print("\nFolders available for README.md creation:")
    for num, folder in folder_map.items():
        console.print(f"[{num}] {folder}")

    choices = Prompt.ask("Enter folder numbers to create README.md (comma-separated)", default="")
    choices = [int(x.strip()) for x in choices.split(",") if x.strip().isdigit()]
    for c in choices:
        folder = folder_map.get(c)
        if folder:
            # Use folder name for the markdown file
            readme = folder / f"{folder.name}.md"
            if not readme.exists():
                readme.write_text(f"# {folder.name}\n")
                console.print(f"Created {readme.name} in: {folder}")

def read_mode(base_path):
    show_files = Confirm.ask("Show files in the diagram?")
    ignore_usual = Confirm.ask(
        "Would you like to ignore usually ignored folders (node_modules/, __pycache__/, .git, etc.)?"
    )
    show_ignored_folder = False
    if ignore_usual:
        show_ignored_folder = Confirm.ask(
            "Do you want to show the ignored folders in the diagram (without their contents)?"
        )

    def build_tree_filtered(path, show_files=False, ignored=None, show_ignored=False):
        ignored = ignored or []
        tree = {}
        for p in sorted(path.iterdir()):
            if p.name in ignored:
                if show_ignored:
                    tree[p.name] = {}  # folder placeholder as empty dict
                continue
            if p.is_dir():
                tree[p.name] = build_tree_filtered(p, show_files, ignored, show_ignored)
            elif show_files:
                tree[p.name] = None  # files remain None
        return tree

    ignored_list = DEFAULT_IGNORED_FOLDERS if ignore_usual else []
    tree_dict = build_tree_filtered(base_path, show_files=show_files, ignored=ignored_list, show_ignored=show_ignored_folder)
    
    console.print(f"{base_path.name}/")
    
    save_tree = Confirm.ask("Do you want to save this diagram as TREE.md?")
    file_handle = open(base_path / "TREE.md", "w", encoding="utf-8") if save_tree else None

    print_tree(tree_dict, file_handle=file_handle)

    if file_handle:
        file_handle.close()
        console.print(f"[bold green]Diagram saved as TREE.md in {base_path}[/bold green]")

def save_tree_diagram(base_path):
    tree_dict = build_tree(base_path)
    file_path = base_path / "TREE.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"```text\n{base_path.name}/\n")
        print_tree(tree_dict, file_handle=f)
        f.write("```\n")
    console.print(f"[bold green]Diagram saved as TREE.md in {base_path}[/bold green]")

def main():
    console.print(BANNER)
    try:
        mode = Prompt.ask("Select mode", choices=["create", "read"])
        base_path = Path.cwd()

        if mode == "create":
            folder_map = create_folder_structure(base_path)
            console.print("\n[bold]Project Structure:[/bold]")
            display_tree(base_path)
            if Confirm.ask("Do you want to create README.md files?"):
                create_readmes(folder_map)
            if Confirm.ask("Do you want to save the folder tree as TREE.md?"):
                save_tree_diagram(base_path)
            console.print("\n[bold green]All done![/bold green]")
        elif mode == "read":
            read_mode(base_path)
        else:
            console.print("[red]Invalid mode[/red]")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user.[/bold yellow]")
        exit(0)

if __name__ == "__main__":
    main()
