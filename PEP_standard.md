# Understanding PEP Standards

**What standards does pip follow?**

`pip` adheres to several Python Enhancement Proposals (PEPs) that define how Python packages are specified, installed, and managed. Understanding these standards helps you work effectively with pip and understand how it relates to other tools.

## 1. PEP 440 - Version Identification and Dependency Specification

**PEP 440** defines how Python package versions are identified and compared. pip uses this standard for version specifiers in requirements files and dependency declarations.

### 1.1 Version specifier formats

```text
# Exact version
package==1.2.3

# Version ranges
package>=1.2.3          # At least version 1.2.3
package<2.0.0           # Less than version 2.0.0
package>=1.2.3,<2.0.0    # Between 1.2.3 (inclusive) and 2.0.0 (exclusive)

# Compatible release (approximately equivalent to >=X.Y, <(X+1).0)
package~=1.2.3          # Same as >=1.2.3,<1.3.0

# Pre-release versions
package>=1.2.3a1        # Alpha/beta/rc versions
package==1.2.3.post1     # Post-release versions

# Any version
package                 # Latest available version
```

### 12 Version format

- Format: `[N!]N(.N)*[{a|b|rc}N][.postN][.devN]`
- Examples: `1.0`, `1.2.3`, `1.2.3a1`, `1.2.3.post1`, `2024.1`

## 2. PEP 508 - Dependency Specification

**PEP 508** defines the format for specifying dependencies, including version requirements, extras, and environment markers. This is what pip uses when parsing requirements files and `pyproject.toml` dependencies.

### 2.1 Dependency specification format

```text
# Basic format
package-name
package-name>=1.0.0
package-name[extra]>=1.0.0

# With extras (optional features)
requests[security]>=2.25.0
pandas[excel]>=1.3.0

# With environment markers (conditional dependencies)
pkg>=1.0.0; python_version >= "3.8"
pkg>=1.0.0; sys_platform == "linux"
pkg>=1.0.0; platform_machine == "x86_64"

# With URL or VCS sources
pkg @ git+https://github.com/user/repo.git@branch
pkg @ file:///local/path/to/package
```

### 2.2 Environment markers

- `python_version` - Python version (e.g., `"3.11"`)
- `sys_platform` - Operating system (e.g., `"linux"`, `"darwin"`, `"win32"`)
- `platform_machine` - Machine architecture (e.g., `"x86_64"`, `"arm64"`)
- `os_name` - OS name (e.g., `"posix"`, `"nt"`)

## 3. PEP 517/518 - Build System Interface

**PEP 517** and **PEP 518** define how Python projects specify their build system. While pip itself is an installer (not a build system), it uses these standards to understand how to install packages that need building.

### 3.1 How pip uses PEP 517/518

1. **PEP 518** (`pyproject.toml` build-system specification):

   ```toml
   [build-system]
   requires = ["setuptools>=61.0", "wheel"]
   build-backend = "setuptools.build_meta"
   ```

2. **PEP 517** (build backend interface):
   - Defines the interface between pip and build tools
   - Allows pip to build packages using different build systems (setuptools, poetry-core, flit, etc.)
   - pip calls the build backend to build source distributions and wheels

### 3.2 Modern pip workflow

- pip reads `pyproject.toml` to determine build requirements
- Installs build dependencies in an isolated environment
- Uses the specified build backend to build the package
- Installs the built package

## 4. PEP 621 - Project Metadata

**PEP 621** defines a standard way to specify project metadata in `pyproject.toml` using the `[project]` section. Modern pip (21.3+) can read and use this metadata.

### 4.1 PEP 621 format

```toml
[project]
name = "my-package"
version = "1.0.0"
description = "A sample package"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["package", "example"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
]

dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
]
```

### 4.2 Key points

- **Standard format:** Used by pip, uv, and other modern tools
- **Interoperable:** Works across different package managers
- **Replaces setup.py:** Modern alternative to `setup.py` and `setup.cfg`
- **pip support:** pip 21.3+ can install packages directly from `pyproject.toml` with PEP 621 metadata

## 5. Requirements File Format (De Facto Standard)

While not a formal PEP, the requirements file format is a widely-adopted de facto standard used by pip.

### 5.1 Requirements file format

```text
# Simple requirements
package-name
package-name==1.2.3
package-name>=1.2.3,<2.0.0

# With extras
package-name[extra]==1.2.3

# With environment markers
package-name==1.2.3; python_version >= "3.8"

# From URLs/VCS
git+https://github.com/user/repo.git@branch#egg=package-name
https://example.com/package-1.2.3.tar.gz

# Editable installs (development)
-e .
-e /path/to/local/package
-e git+https://github.com/user/repo.git@branch#egg=package-name

# Comments
# This is a comment
package-name==1.2.3  # Inline comment

# Constraints files (for pinning transitive dependencies)
-c constraints.txt
```

### 5.2 Common requirements file patterns

- `requirements.txt` - Main dependencies
- `requirements-dev.txt` - Development dependencies
- `requirements-prod.txt` - Production dependencies
- `requirements-test.txt` - Test dependencies
- `constraints.txt` - Pinned transitive dependencies

## 6. Summary: pip Standards

| Standard | Purpose | Used By pip |
|----------|---------|-------------|
| **PEP 440** | Version identification and specifiers | ✓ Yes - for parsing version requirements |
| **PEP 508** | Dependency specification format | ✓ Yes - for requirements files and dependencies |
| **PEP 517/518** | Build system interface | ✓ Yes - for building packages from source |
| **PEP 621** | Project metadata in pyproject.toml | ✓ Yes - pip 21.3+ supports installing from PEP 621 projects |
| **Requirements.txt** | De facto standard for dependency lists | ✓ Yes - primary dependency file format |

### Modern pip features

- Can install directly from `pyproject.toml` with PEP 621 metadata (pip 21.3+)
- Supports PEP 517/518 build system (can build packages using various backends)
- Follows PEP 440 for version resolution
- Uses PEP 508 for dependency specification parsing
