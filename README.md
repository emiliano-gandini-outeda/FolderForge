# FolderForge

FolderForge is a Python CLI tool that helps you quickly create and organize project folder structures. It supports nested folders, optional README.md creation, and beautifully formatted folder tree diagrams. You can also read and visualize existing project structures with files included. Optionally, the tree diagram can be saved as `TREE.md` in the main project folder.

---

## Features

- **Create nested folders** interactively.
- **Numbered folder selection** for README.md creation (numbers do not appear in tree output).
- **Beautiful folder tree** with `├──`, `└──`, `│` style.
- **Optional README.md creation** in selected folders (README contains the folder name).
- **Read mode** to display folder and file structures in the same tree style.
- **Save tree diagram** as `TREE.md` in the project root.
- Professional CLI banner for an engaging interface.

---

# **Installation**

### Step 1 – Install Python and Dependencies

Make sure Python 3 is installed on your system, and install the required `rich` library:

```bash
pip install rich
```

#### Step 2 – Clone the Repository

Clone FolderForge to a location of your choice:

```bash
git clone https://github.com/emiliano-gandini-outeda/FolderForge
cd FolderForge
```

#### Step 3 – Make the CLI Tool Globally Accessible (Optional but Recommended)

To use FolderForge from **any folder**:

1. Ensure the script has executable permissions:

```bash
chmod +x folderforge-cli.py
```

2. Move it to a directory in your `PATH` (for example, `/usr/local/bin` on Unix-like systems):

```bash
sudo mv folderforge-cli.py /usr/local/bin/folderforge
```

> Now you can run `folderforge` from any folder without being inside the repository.

---

## Usage

Run the CLI tool from your project folder:

```bash
folderforge
```

### Select Mode

* **create**: Interactively create folders and optionally add README.md files.
* **read**: Display an existing project structure, optionally including files.

### Create Mode

1. Enter subfolder names. You will be prompted recursively for nested folders.
2. After folder creation, choose if you want to create README.md files in selected folders. Folder numbers will be shown **only for selection purposes**.
3. Optionally, save the folder tree as `TREE.md` in the main folder.
4. View the project tree in the terminal.

Example project tree (numbers not shown):

```text
my-project/
├── main-app/
│   ├── linux-compatibility/
│   ├── networking/
│   ├── algorithms/
│   └── docker/
├── web-app/
│   ├── html/
│   ├── css/
│   ├── javascript/
│   └── django/
└── python-tools/
    ├── scripts/
    └── notebooks/
```

Folder numbers will appear like this **only when selecting folders for README.md**:

```text
[1] general-cs/
[2] linux/
[3] networking/
[4] algorithms/
[5] docker/
[6] web-development/
...
```

### Read Mode

1. Choose whether to include files in the diagram.
2. Optionally, save the tree diagram as `TREE.md`.
3. View the project structure in the same tree style.

Example output including files:

```text
my-project/
├── general-cs/
│   ├── linux-compatibility/
│   │   ├── README.md
│   │   └── install.sh
│   ├── networking/
│   │   └── README.md
│   ├── algorithms/
│   │   ├── README.md
│   │   └── sorting.py
│   └── docker/
│       └── Dockerfile
├── web-development/
│   ├── html/
│   │   └── index.html
│   ├── css/
│   │   └── style.css
│   ├── javascript/
│   │   └── app.js
│   └── django/
│       ├── manage.py
│       └── settings.py
└── python-tools/
    ├── scripts/
    │   └── utils.py
    └── notebooks/
        └── analysis.ipynb

```
---

## License

This project is licensed under the MIT License.

