import os
import sys
from distutils.core import setup
from pathlib import Path
from setuptools import find_packages

# Loads the version from package
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from buttons import __version__ as version  # noqa

this_directory = Path(__file__).parent
readme_file = this_directory / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text()
else:
    long_description = None

setup(
    name="django-buttons",
    version=version,
    author="François GUÉRIN",
    author_email="fguerin@ville-tourcoing.fr",
    description="An application providing some template-tags to add buttons to pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frague59/django-buttons",
    license="MIT",
    keywords=[
        "django",
        "buttons",
        "bootstrap3",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "django-appconf",
    ],
    extras_require={
        "fa4": [
            "django-fontawesome",
        ],
        "fa5": [
            "django-fontawesome-5",
        ],
    },
    # Source files
    packages=find_packages("."),
    # Includes static files
    include_package_data=True,
)
