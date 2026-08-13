import os
import re
from setuptools import setup, find_packages

def get_version():
    init_py = os.path.join(os.path.dirname(__file__), "bugpilot", "__init__.py")
    with open(init_py, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return re.search(r'"([^"]+)"', line).group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bugpilot-cli",
    version=get_version(),
    author="LAKSHMIKANTHAN K",
    author_email="letchupkt.dev@gmail.com",
    description="AI-Powered Autonomous Penetration Testing CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l3tchupkt/bugpilot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.36",
        "google-generativeai>=0.3.0",
        "anthropic>=0.7.0",
        "groq>=0.4.0",

        "PyYAML>=6.0",
        "requests>=2.31.0",
    ],
    include_package_data=True,
    package_data={
        "bugpilot": ["core/config/*.yaml", "*.yaml"],
    },
    entry_points={
        "console_scripts": [
            "bugpilot=bugpilot.__main__:main",
        ],
    },
)
