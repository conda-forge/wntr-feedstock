"""
Patch a conda-forge feedstock recipe/meta.yaml using Grayskull output.

Usage:
    python patch_meta.py <grayskull_meta.yaml> <feedstock_meta.yaml>

Reads version and sha256 from the Grayskull-generated meta.yaml, then updates
those fields plus the build number in the feedstock recipe. All other content
is left unchanged.
"""
import re
import sys

grayskull_path, feedstock_path = sys.argv[1], sys.argv[2]

with open(grayskull_path) as f:
    grayskull = f.read()

version = re.search(r'version:\s*["\']?([^\s"\']+)["\']?', grayskull).group(1)
sha256 = re.search(r'sha256:\s*(\S+)', grayskull).group(1)

with open(feedstock_path) as f:
    content = f.read()

current_version = re.search(r'{%\s*set version\s*=\s*"([^"]+)"', content).group(1)
current_build = int(re.search(r'number:\s*(\d+)', content).group(1))
build_number = 0 if version != current_version else current_build + 1

pypi_url = 'https://pypi.io/packages/source/W/wntr/wntr-{{ version }}.tar.gz'

content = re.sub(r'({% set version = ")[^"]+(")', f'\\g<1>{version}\\2', content)
content = re.sub(r'url:\s*\S+', f'url: {pypi_url}', content)
content = re.sub(r'(sha256:\s*)\S+', f'\\g<1>{sha256}', content)
content = re.sub(r'(number:\s*)\d+', f'\\g<1>{build_number}', content)

with open(feedstock_path, 'w') as f:
    f.write(content)

print(f"Patched {feedstock_path}: version={version}, sha256={sha256}, build number={build_number}")
