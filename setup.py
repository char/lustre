from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lustre",
    version="0.2.0",
    description="An opinionated, batteries-included ASGI web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/half-cambodian-hacker-man/lustre/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    package_data={"lustre.forms": ["templates/forms/*.html"]},
    python_requires=">=3.6, <4",
    install_requires=[
        "aiofiles==0.5.0",
        "databases==0.3.2",
        "jinja2==2.11.2",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "orm==0.1.5",
        "python-multipart==0.0.5",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sqlalchemy==1.3.19; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "starlette==0.13.8",
        "typesystem==0.2.4",
    ],
    extras_require={},
    dependency_links=[],
    project_urls={
        "Source": "https://github.com/half-cambodian-hacker-man/lustre/",
    },
)
