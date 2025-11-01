# Understanding pip, poetry, and uv

## 1. pip, poetry, and uv

### 1.1 pip

`pip` is the standard installer for Python packages (from PyPI or other indexes). It handles installing/uninstalling dependencies, but does not by itself manage virtual environments or lock files in a sophisticated way.

**Good for:** Simple scripts or projects with minimal dependencies.

### 1.2 Poetry

`Poetry` is a higher-level project/dependency manager for Python: it handles dependencies + lock files + virtual environment creation + packaging/publishing. It uses a `pyproject.toml` and `poetry.lock` file, supports grouping (dev vs prod deps), etc.

**Good for:** More structured projects (apps, libraries) where reproducibility and packaging matter.

### 1.3 uv

`uv` is a newer Python tool (written in Rust) that aims to be a fast installer and manager — essentially a modern replacement/enhancement for `pip` + `venv` + maybe `virtualenv` etc. It emphasizes speed, reproducible installs, modern workflows (lock files, etc).

**Good for:** When you prioritize fast installs or want a newer workflow, especially in CI or bigger projects.

### 1.4 When to use which

- **Use `pip`** if you just need to quickly install a package or you have a simple project.
- **Use `Poetry`** when you're developing a project (library/app) where you want dependency resolution, lock files, reproducible builds, environment isolation.
- **Use `uv`** when you want that same structured workflow but prioritize install speed, modern tooling, possibly replacing `pip` + `virtualenv` workflows.

## 2. Project overview

Let's say the project is named `my_data_app` and uses `pandas` for data-manipulation and `DuckDB` for running SQL queries (for example, joining data or doing aggregations). `DuckDB` integrates nicely with `pandas` frames.

We'll assume Python 3.11.5 (or a compatible version). We'll have three dependencies:

- `pandas`
- `duckdb`
- `pytest`

### 2.1 Using pip

1. Create and activate a virtual environment manually:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # on Linux/Mac
   # or .venv\Scripts\activate     # on Windows
   ```

2. Install dependencies:

   ```bash
   pip install pandas duckdb
   pip install pytest
   ```

3. Generate a requirements file:

   ```bash
   pip freeze > requirements.txt
   ```

4. Project structure might look like:

   ```zsh
   dir/
     .venv/
     src/
       __init__.py
       main.py
     tests/
       test_main.py
     requirements.txt
   ```

5. Example `main.py` code:

   ```python
   import pandas as pd
   import duckdb

   def load_data():
       # sample pandas DataFrame
       df = pd.DataFrame({"id": [1,2,3,4], "value": [10,20,30,40]})
       return df

   def query_data(df: pd.DataFrame):
       con = duckdb.connect()        # in-memory by default
       # register DataFrame as a table
       con.register("t", df)
       # run SQL
       result = con.execute("SELECT id, value, value*2 AS value2 FROM t WHERE value >= 20 ORDER BY id DESC").df()
       return result

   if __name__ == "__main__":
       df = load_data()
       print("Input:\n", df)
       out = query_data(df)
       print("Result:\n", out)
   ```

   This shows how `DuckDB` can be used on a `pandas` DataFrame.

6. To replicate environment elsewhere:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

#### 2.1.1 Understanding pip's Virtual Environment (.venv)

When using `pip`, you manually create virtual environments using Python's built-in `venv` module:

**What is a virtual environment?**
A virtual environment is an isolated Python environment that:

- Has its own Python interpreter
- Has its own site-packages directory (where packages are installed)
- Prevents conflicts between different projects' dependencies
- Is completely separate from your system Python

**How pip's .venv works:**

1. **Creation:** `python3 -m venv .venv` creates a directory structure:

   ```text
   .venv/
   ├── bin/              # Scripts and executables (Linux/Mac)
   │   ├── activate      # Activation script
   │   ├── python        # Python interpreter symlink
   │   └── pip           # pip executable
   ├── lib/              # Installed packages
   │   └── python3.11/
   │       └── site-packages/  # Your installed packages go here
   ├── include/          # Header files
   └── pyvenv.cfg        # Configuration file
   ```

2. **Activation:** `source .venv/bin/activate` modifies your shell's PATH:
   - Adds `.venv/bin` to the front of PATH
   - Changes your prompt to show `(.venv)`
   - Makes `python` and `pip` point to the virtual environment versions

3. **Installation:** When you run `pip install`, packages are installed into `.venv/lib/python3.11/site-packages/`

4. **Deactivation:** `deactivate` removes the virtual environment from your PATH

**Characteristics:**

- Virtual environment is project-specific (created in project directory)
- Must be manually activated before use
- Can be easily deleted and recreated
- Works the same way across pip, Poetry, and uv (they all use Python's venv internally)

#### 2.1.2 Understanding requirements.txt

**What is requirements.txt?**
A simple text file that lists Python packages and their versions. It's generated by `pip freeze` and used to recreate an environment.

**Example requirements.txt:**

```text
duckdb==1.4.1
numpy==2.3.4
pandas==2.3.3
pytest==8.4.2
python-dateutil==2.9.0.post0
pytz==2025.2
```

**How it works:**

- **Generation:** `pip freeze > requirements.txt` captures all currently installed packages with exact versions
- **Installation:** `pip install -r requirements.txt` installs all listed packages
- **Format:** One package per line, format: `package==version` or `package>=version,<version`

**Limitations:**

- No automatic dependency resolution (you must list all transitive dependencies)
- No grouping (can't separate dev vs production dependencies)
- No lock file guarantees (someone else installing might get different versions of sub-dependencies)
- Manual management (must remember to update when adding/removing packages)

- **Pros:** Simple, familiar, minimal tooling.
- **Cons:** You need to manage the virtual environment yourself; you don't automatically get a lockfile; reproducibility is weaker (unless you pin versions carefully); no built-in grouping of dev vs prod deps.

### 2.2 Using Poetry

1. Install `Poetry` (if not already):

   ```bash
   pip install poetry
   # or follow official install instructions
   ```

2. In your project directory:

   ```bash
   poetry init
   ```

   And answer prompts (or you can manually craft `pyproject.toml`).

3. Example `pyproject.toml` for our case:

   ```toml
   [tool.poetry]
   name = "my_data_app"
   version = "0.1.0"
   description = "A simple data app using pandas + DuckDB"
   authors = ["Your Name <you@example.com>"]

   [tool.poetry.dependencies]
   python = "^3.11"
   pandas = "^2.0"
   duckdb = "^1.3"

   [tool.poetry.group.dev.dependencies]
   pytest = "^8.0"

   [build-system]
   requires = ["poetry-core"]
   build-backend = "poetry.core.masonry.api"
   ```

   (Versions are illustrative; check latest versions.)

4. Install dependencies:

   ```bash
   poetry install
   ```

   This will create a virtual environment (by default) and install dependencies along with a `poetry.lock` file.

5. To add a new dependency later, e.g.:

   ```bash
   poetry add flask
   poetry add --group dev black
   ```

6. Running your code:

   ```bash
   poetry run python my_data_app/main.py
   ```

7. If you want to install for production (no dev deps):

   ```bash
   poetry install --without dev
   ```

#### 2.2.1 Understanding pyproject.toml (TOML Format)

**What is TOML?**
TOML (Tom's Obvious Minimal Language) is a configuration file format designed to be easy to read and write. It's similar to INI files but with better structure.

**What is pyproject.toml?**
`pyproject.toml` is a standard Python project configuration file (PEP 518, PEP 621) that can be used by multiple tools including Poetry, uv, pip, setuptools, and others. It replaces multiple older configuration files like `setup.py`, `setup.cfg`, `requirements.txt`, etc.

**Basic TOML syntax:**

```toml
# Comments start with #
key = "value"
number = 42
boolean = true
array = ["item1", "item2"]
nested = { key = "value" }

[section]
key = "value"

[[array-of-tables]]
key = "value"
```

**Poetry's pyproject.toml structure:**

```toml
[tool.poetry]
name = "my_data_app"
version = "0.1.0"
description = "A simple data app"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"           # Caret (^) means compatible version
pandas = "^2.0"            # Same as >=2.0,<3.0
duckdb = "^1.3"            # Same as >=1.3,<2.0

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Key sections:**

- `[tool.poetry]` - Project metadata (name, version, description, authors)
- `[tool.poetry.dependencies]` - Production dependencies
- `[tool.poetry.group.dev.dependencies]` - Development dependencies (grouped)
- `[build-system]` - Specifies how to build the package

**Version specifiers:**

- `^3.11` - Compatible version (>=3.11,<4.0)
- `~3.11.0` - Compatible release (>=3.11.0,<3.12.0)
- `>=2.0,<3.0` - Version range
- `==2.3.3` - Exact version
- `*` - Any version

#### 2.2.2 Understanding poetry.lock

**What is poetry.lock?**
`poetry.lock` is Poetry's lock file that records the exact versions of all dependencies (including transitive dependencies) that were resolved and installed. It ensures reproducible builds across different machines and environments.

**Purpose:**

- **Reproducibility:** Everyone gets the exact same dependency versions
- **Security:** Prevents unexpected updates that might introduce vulnerabilities
- **Stability:** Ensures the same environment every time you install

**File structure:**

```toml
# This file is automatically @generated by Poetry and should not be changed by hand.
package = []

[metadata]
lock-version = "2.1"
python-versions = ">=3.11"
content-hash = "f5666f5625d676c506924a57dc0520a1f3ed2b2c774baed3dc85353594f8473d"

[[package]]
name = "pandas"
version = "2.3.3"
description = "Powerful data structures for data analysis"
category = "main"
optional = false
python-versions = ">=3.11"
# ... more details including all sub-dependencies
```

**How it works:**

1. **Generation:** Created automatically when you run `poetry install` or `poetry add`
2. **Resolution:** Poetry resolves all dependencies and writes exact versions to the lock file
3. **Installation:** `poetry install` reads the lock file and installs exact versions
4. **Updates:** Run `poetry update` to update dependencies and regenerate the lock file

**Important points:**

- **Should be committed to version control** - Ensures team consistency
- **Don't edit manually** - Poetry manages it automatically
- **Contains full dependency tree** - Lists all transitive dependencies with exact versions
- **Platform-specific info** - May include platform-specific package hashes

**When lock file is updated:**

- When you run `poetry add <package>` - adds new dependency
- When you run `poetry remove <package>` - removes dependency
- When you run `poetry update` - updates dependencies within version constraints
- When you manually edit `pyproject.toml` and run `poetry install`

#### 2.2.3 Understanding Poetry's Virtual Environment Management

**How Poetry manages virtual environments:**

1. **Automatic creation:** Poetry automatically creates a virtual environment when you run `poetry install` if one doesn't exist

2. **Location:** By default, Poetry creates virtual environments in:
   - `{cache-dir}/virtualenvs/` (usually `~/.cache/pypoetry/virtualenvs/`)
   - Named with pattern: `{project-name}-{hash}-py3.11`
   - You can configure this location in `poetry config`

3. **Activation:** Unlike pip, you don't need to manually activate:
   - Use `poetry run <command>` to run commands in the virtual environment
   - Use `poetry shell` to spawn a shell with the virtual environment activated
   - Poetry automatically finds and uses the correct virtual environment

4. **Configuration:**

   ```bash
   # Use .venv in project directory (like pip)
   poetry config virtualenvs.in-project true
   
   # View virtual environment location
   poetry env info
   
   # List all Poetry virtual environments
   poetry env list
   ```

5. **Benefits:**
   - No manual activation needed
   - Automatic environment detection
   - Project-specific isolation
   - Can have multiple projects with different Python versions

**Example workflow:**

```bash
poetry install                    # Creates venv and installs dependencies
poetry run python src/main.py    # Runs in venv automatically
poetry shell                      # Activates venv for interactive use
poetry add flask                  # Adds dependency and updates lock file
poetry env remove python3.11      # Removes virtual environment
```

#### 2.2.4 Pros and cons for Poetry

- **Pros:** Automatic virtual env, lock-file ensures reproducibility, clear separation of dev vs prod deps, packaging support (ready for publishing).
- **Cons:** Another tool to learn; some overhead if your project is tiny/simple; sometimes version resolution can be slower than plain `pip`.

#### 2.2.5 Troubleshooting: "No file/folder found for package" error

If you encounter this error when running `poetry install`:

```text
Error: The current project could not be installed: No file/folder found for package pip-poetry-and-uv
```

**What's happening:**

When you run `poetry install`, Poetry tries to:

1. Install your dependencies (like pandas, duckdb)
2. Install your project itself as a package

It fails at step 2 because it can't find your package code.

**The problem:**

Your project structure might look like:

```text
pip-poetry-and-uv/
├── src/
│   ├── __init__.py
│   └── main.py          ← Your code is here
└── pyproject.toml
```

Poetry expects either:

- A package directory matching your project name: `src/pip-poetry-and-uv/`
- Or configuration in `pyproject.toml` telling it where to find the package

If your `pyproject.toml` uses PEP 621 format (`[project]` section) instead of Poetry's traditional format, Poetry may not know where your package code is located.

**Solutions:**

- Option 1: Disable package mode:

Simplest for scripts/apps that don't need to be installed as packages.

Add this to your `pyproject.toml`:

```toml
[tool.poetry]
package-mode = false
```

This tells Poetry to only manage dependencies, not install your project as a package.

- Option 2: Install without the project:

Run:

```bash
poetry install --no-root
```

This installs dependencies but skips installing your project itself.

- Option 3: Configure package location:

If you want Poetry to install your project as a package, tell it where the code is. Add to `pyproject.toml`:

```toml
[tool.poetry]
packages = [{include = "your_package_name", from = "src"}]
```

Or restructure your project to have a package directory matching your project name:

```text
pip-poetry-and-uv/
├── src/
│   └── pip-poetry-and-uv/    ← Package directory matches project name
│       ├── __init__.py
│       └── main.py
└── pyproject.toml
```

**Note:** For simple scripts/apps, Option 1 (package-mode = false) is usually the best choice.

### 2.3 Using uv

1. Install `uv` (via its official method, e.g.):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or via pip: pip install uv (if supported)
   ```

   Then verify:

   ```bash
   uv --version
   ```

2. In your project directory, create a `pyproject.toml`. For example:

   ```toml
   [project]
   name = "my_data_app"
   version = "0.1.0"
   dependencies = [
     "pandas>=2.0,<3.0",
     "duckdb>=1.3,<2.0"
   ]

   [tool.uv.dependency-groups.dev]
   dependencies = [
     "pytest>=8.0,<9.0"
   ]
   ```

   (Note: `uv` uses the `[tool.uv.dependency-groups.dev]` section for dev deps. See [uv documentation](https://docs.astral.sh/uv/) for more details.)

3. Create and sync the environment:

   ```bash
   uv venv .venv           # creates a .venv virtual env
   uv sync                 # install the dependencies as specified (and create a lockfile if needed)
   ```

4. To run the project:

   ```bash
   uv run python my_data_app/main.py
   ```

5. To add new dependency:

   ```bash
   uv add flask
   uv add --group dev black
   ```

6. If you want to run only dev group or freeze sync:

   ```bash
   uv sync --group dev     # to include dev dependencies
   uv sync --frozen        # to install exactly as lockfile (no changes)
   ```

#### 2.3.1 Understanding uv's pyproject.toml (PEP 621 Format)

**uv uses PEP 621 standard format:**

Unlike Poetry's custom format, `uv` uses the standard PEP 621 `[project]` section, making it compatible with other modern Python tools.

**Example pyproject.toml for uv:**

```toml
[project]
name = "my_data_app"
version = "0.1.0"
description = "A simple data app using pandas + DuckDB"
authors = [
    {name = "Mark Pham", email = "minh.pham@insurify.com"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.3.3",
    "duckdb>=1.4.1",
]

[tool.uv.dependency-groups.dev]
dependencies = [
    "pytest>=8.0,<9.0",
]

[tool.poetry]
packages = [{include = "src", from = "."}]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

**Key differences from Poetry format:**

1. **`[project]` section (PEP 621):**
   - Standard Python project metadata
   - Used by pip, uv, and other PEP 621-compliant tools
   - More interoperable than Poetry's custom format

2. **`[tool.uv.dependency-groups.dev]` section:**
   - uv's way of defining development dependencies
   - Similar to Poetry's groups but uses standard structure
   - Can have multiple groups: `dev`, `test`, `docs`, etc.

3. **Version specifiers:**
   - Uses standard version specifiers: `>=2.3.3`, `>=2.0,<3.0`
   - More explicit than Poetry's `^` and `~` operators
   - Same as pip's version specifiers

**Benefits of PEP 621 format:**

- **Standard:** Works with multiple tools (pip, uv, setuptools)
- **Interoperable:** Can be used by different package managers
- **Future-proof:** Official Python standard (PEP 621)
- **Flexible:** Can mix Poetry and uv sections if needed

#### 2.3.2 Understanding uv.lock

**What is uv.lock?**
`uv.lock` is uv's lock file format. Like `poetry.lock`, it records exact versions of all dependencies, but uses a different structure optimized for speed and cross-platform compatibility.

**Purpose:**

- **Reproducibility:** Ensures identical dependency versions across environments
- **Speed:** Binary format allows fast resolution and installation
- **Cross-platform:** Handles platform-specific dependencies elegantly
- **Deterministic:** Same input always produces same output

**File structure (excerpt):**

```toml
version = 1
revision = 3
requires-python = ">=3.11"
resolution-markers = [
    "python_full_version >= '3.12'",
    "python_full_version < '3.12'",
]

[[package]]
name = "duckdb"
version = "1.4.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/...", hash = "sha256:...", size = 18461687 }
wheels = [
    { url = "https://files.pythonhosted.org/.../duckdb-1.4.1-cp311-cp311-macosx_11_0_arm64.whl", 
      hash = "sha256:...", size = 13756223 },
    # ... more platform-specific wheels
]

[[package]]
name = "pandas"
version = "2.3.3"
# ... dependency details
```

**Key features:**

1. **Platform-specific wheels:** Lists all available wheels for different platforms (macOS, Linux, Windows, different architectures)

2. **Hash verification:** Each package includes SHA256 hashes for security and integrity verification

3. **Resolution markers:** Handles Python version-specific dependencies

4. **Revision tracking:** The `revision` field increments when lock file is regenerated

**How it works:**

1. **Generation:** Created automatically when you run `uv sync` or `uv add`
2. **Resolution:** uv resolves dependencies using Rust-based resolver (very fast)
3. **Installation:** `uv sync` reads the lock file and installs exact versions
4. **Updates:** Run `uv sync` with updated `pyproject.toml` to regenerate, or `uv lock --upgrade` to update

**Important points:**

- **Should be committed to version control** - Like poetry.lock
- **Don't edit manually** - uv manages it automatically
- **Platform-aware** - Contains platform-specific package information
- **Fast resolution** - Binary resolver is orders of magnitude faster than Python-based resolvers

**When lock file is updated:**

- When you run `uv add <package>` - adds new dependency
- When you run `uv remove <package>` - removes dependency
- When you run `uv sync` with changed `pyproject.toml`
- When you run `uv lock --upgrade` - updates all dependencies

**Comparison with poetry.lock:**

- **uv.lock:** Faster, more platform-specific details, binary resolver
- **poetry.lock:** More human-readable, better tooling support (older ecosystem)

#### 2.3.3 Understanding uv's Virtual Environment Management

**How uv manages virtual environments:**

1. **Manual creation:** Unlike Poetry, uv requires explicit virtual environment creation:

   ```bash
   uv venv .venv    # Creates .venv in project directory
   ```

2. **Location:**
   - Default: `.venv` in project directory (can specify different location)
   - Same structure as Python's `venv` module
   - Can use existing `.venv` or create new ones

3. **Activation:** Similar to pip, but uv provides convenience commands:

   ```bash
   # Traditional activation (like pip)
   source .venv/bin/activate
   
   # Or use uv run (no activation needed)
   uv run python src/main.py
   uv run pytest
   ```

4. **Sync command:** `uv sync` is the key command:
   - Creates virtual environment if it doesn't exist
   - Installs all dependencies from `pyproject.toml`
   - Creates/updates `uv.lock` file
   - Installs the project itself as editable package

5. **Python version management:**

   ```bash
   # Create venv with specific Python version
   uv venv .venv --python 3.11
   
   # uv can also install Python versions
   uv python install 3.11
   uv python list
   ```

6. **Workflow:**

   ```bash
   uv venv .venv           # Create virtual environment
   uv sync                  # Install dependencies and create lock file
   uv run python src/main.py  # Run without activation
   # OR
   source .venv/bin/activate  # Traditional activation
   python src/main.py
   ```

**Benefits:**

- **Fast:** Extremely fast installation (written in Rust)
- **Unified:** Replaces multiple tools (venv, pip, pip-tools, pyenv)
- **Simple:** Straightforward workflow, similar to pip
- **Flexible:** Can use with or without activation
- **Python management:** Can install and manage Python versions

**Key differences from Poetry:**

- **Explicit venv creation:** Must run `uv venv` first
- **Project directory venv:** Defaults to `.venv` in project (like pip)
- **Can use traditional activation:** Works with standard `source .venv/bin/activate`
- **Faster:** Much faster dependency resolution and installation

**Key differences from pip:**

- **Lock file:** Automatically generates `uv.lock` for reproducibility
- **Dependency resolution:** Handles transitive dependencies automatically
- **Project installation:** Can install project as editable package
- **Speed:** Much faster than pip

#### 2.3.4 Pros and cons for uv

- **Pros:** Very fast installations; manages virtual envs automatically; lock-file support; modern workflow; avoids juggling separate tools (`venv` + `pip` + `pip-tools` + `pyenv`) because `uv` tries to unify them.
- **Cons:** It's newer, so ecosystem/tools/support may be less mature than `pip`/`Poetry`; some team members might not be familiar with it yet.

---

## 3. File Formats and Lock Files Comparison

### 3.1 Configuration Files

| Tool | Configuration File | Format | Standard |
|------|-------------------|--------|----------|
| `pip` | `requirements.txt` | Plain text | De facto standard |
| `Poetry` | `pyproject.toml` | TOML (custom format) | Poetry-specific |
| `uv` | `pyproject.toml` | TOML (PEP 621) | Python standard |

**Key differences:**

- **requirements.txt (pip):**
  - Simple text file, one package per line
  - No grouping, no metadata
  - Manual management required

- **pyproject.toml (Poetry):**
  - Uses `[tool.poetry]` sections
  - Rich metadata (name, version, authors, description)
  - Built-in dependency groups
  - Poetry-specific format

- **pyproject.toml (uv):**
  - Uses `[project]` section (PEP 621)
  - Standard Python format
  - Interoperable with other tools
  - Uses `[tool.uv.dependency-groups]` for dev dependencies

### 3.2 Lock Files Comparison

| Tool | Lock File | Format | Purpose |
|------|-----------|--------|---------|
| `pip` | None (or `requirements.txt`) | Plain text | Version pinning (manual) |
| `Poetry` | `poetry.lock` | TOML | Automatic dependency locking |
| `uv` | `uv.lock` | TOML | Automatic dependency locking |

**Comparison:**

**requirements.txt (pip):**

- Manual creation with `pip freeze`
- Lists all installed packages with exact versions
- No dependency resolution information
- No platform-specific details
- Easy to read and edit manually

**poetry.lock:**

- Automatically generated by Poetry
- Contains full dependency tree
- Includes dependency relationships
- Platform-specific information
- Human-readable TOML format
- Should be committed to version control

**uv.lock:**

- Automatically generated by uv
- Contains full dependency tree
- Platform-specific wheel information
- Hash verification for security
- Optimized for fast resolution
- Should be committed to version control

**Key differences:**

- **poetry.lock:** More detailed dependency metadata, better for analysis
- **uv.lock:** Faster resolution, more platform-specific wheel details
- **requirements.txt:** Simplest but least informative

### 3.3 Virtual Environment Comparison

| Tool | Venv Creation | Location | Activation | Management |
|------|---------------|---------|------------|------------|
| `pip` | Manual (`python -m venv`) | Project dir (`.venv`) | Manual (`source .venv/bin/activate`) | Manual |
| `Poetry` | Automatic (`poetry install`) | Cache dir (configurable) | Automatic (`poetry run`) or `poetry shell` | Automatic |
| `uv` | Manual (`uv venv`) | Project dir (`.venv`) | Manual or `uv run` | Semi-automatic |

**Workflow comparison:**

**pip:**

```bash
python3 -m venv .venv           # Create
source .venv/bin/activate       # Activate
pip install -r requirements.txt # Install
# ... work ...
deactivate                      # Deactivate
```

**Poetry:**

```bash
poetry install                  # Creates venv + installs (if needed)
poetry run python script.py     # Run without activation
# OR
poetry shell                    # Spawn activated shell
python script.py
```

**uv:**

```bash
uv venv .venv                   # Create
uv sync                         # Install dependencies
uv run python script.py         # Run without activation
# OR
source .venv/bin/activate       # Traditional activation
python script.py
```

**Key differences:**

- **pip:** Full manual control, traditional workflow
- **Poetry:** Automatic venv management, less manual steps
- **uv:** Fast, flexible (can use traditional or modern workflow)

---

## 4. Summary table for this specific project (pandas + DuckDB)

| Tool    | Workflow complexity | Virtual env handled? | Lockfile support              | Use case suitability for pandas+DuckDB project                                     |
| ------- | ------------------- | -------------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| `pip`   | Low                 | Manual               | Basic (`requirements.txt`)    | Good for simple, small projects with minimal tooling.                              |
| `Poetry`| Medium              | Yes                  | Yes (`poetry.lock`)           | Excellent when you want reproducibility, dev/prod separation, packaging readiness. |
| `uv`    | Medium/Modern       | Yes                  | Yes (`uv.lock`)               | Great when you want speed, modern workflow, fewer tooling overhead.                |

- If you just need something quick and local: **`pip`** is fine.
- If you anticipate the project growing (tests, dev dependencies, packaging, reproducibility) → go with **`Poetry`**.
- If you're comfortable trying newer tools and you value speed + modern workflow → **`uv`** is a solid choice.
