# Web Class Obfuscator

Professional-grade tool for obfuscating CSS class names in web projects. Protect your frontend code by automatically renaming CSS classes across HTML, CSS, and inline styles.

## 🚀 Features

- **Multiple Obfuscation Methods**: Character shift, MD5 hash, or hex encoding
- **Smart Link Updates**: Automatically updates CSS file references in HTML
- **Safe Processing**: Creates backups, never overwrites originals
- **Exclusion System**: Preserve specific classes (e.g., framework classes)
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Progress Tracking**: Visual progress bars with detailed logging
- **Interactive & CLI Modes**: User-friendly menu or powerful command-line interface

## 📦 Installation

```bash
git clone https://github.com/ShahbaziRaz/web-class-obfuscator.git
cd web-class-obfuscator
pip install -r requirements.txt
```

## 🎯 Quick Start
Interactive Mode:

```bash
python web_obfuscator.py

```


CLI Mode:

```bash
# Basic usage
python web_obfuscator.py --path ./my-website

# Advanced usage
python web_obfuscator.py \
  --path ./my-website \
  --suffix "_min" \
  --method hash \
  --exclude "active" "visible" "modal-*" \
  --backup \
  --verbose

```
## 📋 Command-Line Options

| Option          | Description                                | Default            |
| --------------- | ------------------------------------------ | ------------------ |
| `-p, --path`    | Project folder path                        | (interactive mode) |
| `-s, --suffix`  | Output file suffix                         | `_obfuscated`      |
| `--method`      | Obfuscation method: `shift`, `hash`, `hex` | `shift`            |
| `--exclude`     | Space-separated list of classes to exclude | (none)             |
| `--backup`      | Create `.backup` files before processing   | `False`            |
| `-v, --verbose` | Show detailed logs                         | `False`            |
| `-h, --help`    | Show help message                          | -                  |

## 🏗️ Project Structure
Your project will be transformed like this:

```
project/
├── index.html              → index_obfuscated.html
├── styles/
│   ├── main.css           → main_obfuscated.css
│   └── layout.css         → layout_obfuscated.css
├── about.html             → about_obfuscated.css
└── contact.html           → contact_obfuscated.css
```

## 🔒 Obfuscation Methods

### 1. Character Shift (Default)
Shifts letters based on string length:  `.container` → `.eqorwvug0`

### 2. Short Hash
MD5-based unique names:  `.button-primary` → `.c3a9f2b1`

### 3. Hex Encoding
Hex representation: `.nav-item` → `.c6e61762d6974656d`

---

## 🔧 Advanced Usage

### Exclude Classes
Preserve framework or utility classes:
```bash
python web_obfuscator.py --path ./project --exclude "active" "show" "hidden" "btn-*"
```
### Create Backups
```bash
python web_obfuscator.py --path ./project --backup
# Creates: style.css.backup
```
### Custom Suffix
```bash
python web_obfuscator.py --path ./project --suffix "_prod"
# Generates: style_prod.css
```
## 🧪 Testing
### Run tests (when implemented):
```bash
pip install pytest
pytest tests/
```
## 🛠 Contributing

1. Fork the repository
2. Create a feature branch ( `git checkout -b feature/amazing` )
3. Commit changes ( `git commit -m 'Add amazing feature'` )
4. Push branch ( `git push origin feature/amazing` )
5. Open a Pull Request

---

## 📜 License

MIT License - see LICENSE file for details.

---

## ⚠️ Security Notice

This tool provides obfuscation, not encryption. It protects against casual inspection but not determined reverse engineering. For production security, combine with proper minification and code splitting.

---

## 🚀 Roadmap

- [ ] JavaScript class obfuscation
- [ ] Source map generation
- [ ] Configuration file support ( `obfuscate.config.json` )
- [ ] Webpack/Vite plugins
- [ ] React/Vue/Angular integration helpers

## .gitignore

```gitignore
Python
pycache/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
```
## Virtual environments
```gitignore
.env
.venv
env/
venv/
ENV/
```
## IDE
```gitignore
.vscode/
.idea/
*.swp
*.swo
*~
```
##  OS
```gitignore
.DS_Store
Thumbs.db
```
## Project specific
```gitignore
*.backup
_obfuscated.
*.log
```
## Testing
```gitignore
.pytest_cache/
.coverage
htmlcov/
.tox/
```
## 4. 🏗️ Architectural Improvements Explained

### **A. Professional Project Structure**
```python
web-class-obfuscator/
├── web_obfuscator.py      # Main entry point
├── obfuscator.py          # Core logic
├── requirements.txt       # Dependencies
├── setup.py              # Package installer
├── README.md             # Comprehensive documentation
├── LICENSE               # MIT license
├── .gitignore            # Git ignore rules
└── tests/                # Unit tests (future)
└── test_obfuscator.py
```

### **B. Key Enhancements Made**

1. **Full English Translation**: All Persian text replaced with professional English
2. **Type Hints**: Complete type annotations for maintainability
3. **Logging System**: Replaced print() with configurable logging
4. **Error Handling**: Try/except blocks with meaningful error messages
5. **Progress Bars**: `tqdm` integration for large projects
6. **Backup System**: `--backup` flag creates `.backup` files before processing
7. **Exclusion Lists**: `--exclude` parameter to protect framework classes
8. **Multiple Obfuscation Methods**: Three strategies (shift, hash, hex)
9. **CLI + Interactive Modes**: Both menu and command-line interfaces
10. **Cross-Platform Support**: Proper path handling with `pathlib`
11. **Package Structure**: `setup.py` for PyPI distribution
12. **Documentation**: README with examples, badges, and clear instructions
13. **Collision Prevention**: Ensures unique obfuscated names
14. **Performance**: Memory-efficient processing with generators

### **C. User Experience Improvements**

- **Clear Console Command**: `clear_screen()` for Windows/Unix
- **Better Input Validation**: Prevents crashes from invalid choices
- **Esc Key Support**: Natural "back" navigation in menus
- **Verbose Mode**: Debug-level logging for troubleshooting
- **Summary Reports**: End-of-run statistics with file counts
- **Keyboard Interrupt Handling**: Graceful Ctrl+C exit
- **File Dialog Z-Index**: Ensures dialog appears on top

### **D. GitHub-Ready Features**

1. **MIT License**: Standard open-source license
2. **setup.py**: Enables `pip install -e .` and PyPI publishing
3. **requirements.txt**: Standard dependency management
4. **README.md**: Professional documentation with:
   - Badges (add shields.io badges)
   - Installation instructions
   - Usage examples
   - CLI options table
   - Security notice
   - Roadmap for contributors
5. **.gitignore**: Comprehensive ignore patterns
6. **Entry Points**: `console_scripts` for `web-obfuscate` command
7. **Semantic Versioning**: Version 1.0.0 in `setup.py`

### **E. Advanced Recommendations**

1. **Add GitHub Actions** (`.github/workflows/`)
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
         - run: pip install -r requirements.txt
         - run: pytest
2. **Add Code Quality Tools:**
```bash
pip install black flake8 mypy
# Add pre-commit hooks
```
3. **Create a Demo Folder: Add example-project/ with before/after samples**

4. **Add Issues Templates: For bug reports and feature requests**

5. **Publish to PyPI:**
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```