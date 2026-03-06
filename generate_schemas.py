"""Generate spec/ from source/.

Copies and formats all JSON schema files from source/schemas/ to spec/schemas/,
and copies service definitions from source/services/ to spec/services/.

Usage: python generate_schemas.py
"""

import json
import shutil
from pathlib import Path

from schema_utils import load_json

SOURCE_DIR = Path("source")
SPEC_DIR = Path("spec")


def generate_schemas():
    """Copy source/schemas/ → spec/schemas/."""
    source_schemas = SOURCE_DIR / "schemas"
    spec_schemas = SPEC_DIR / "schemas"

    # Clean previous output
    if spec_schemas.exists():
        shutil.rmtree(spec_schemas)

    files_generated = 0

    for source_file in sorted(source_schemas.rglob("*.json")):
        relative = source_file.relative_to(source_schemas)
        dest = spec_schemas / relative
        dest.parent.mkdir(parents=True, exist_ok=True)

        data = load_json(source_file)

        with open(dest, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")

        files_generated += 1

    return files_generated


def copy_services():
    """Copy source/services/ → spec/services/."""
    source_services = SOURCE_DIR / "services"
    spec_services = SPEC_DIR / "services"

    if spec_services.exists():
        shutil.rmtree(spec_services)

    files_copied = 0

    if source_services.exists():
        for source_file in sorted(source_services.rglob("*")):
            if source_file.is_dir():
                continue
            relative = source_file.relative_to(source_services)
            dest = spec_services / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, dest)
            files_copied += 1

    return files_copied


def main():
    schemas = generate_schemas()
    services = copy_services()
    total = schemas + services
    print(f"Generated {schemas} schema files to spec/schemas/")
    print(f"Copied {services} service files to spec/services/")
    print(f"Total: {total} files in spec/")


if __name__ == "__main__":
    main()
