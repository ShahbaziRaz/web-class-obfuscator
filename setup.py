from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="web-class-obfuscator",
    version="1.0.0",
    author="Mohammad Reza Shahbazi-Raz",
    author_email="mohammadreza844@gmail.com",
    description="Professional CSS class name obfuscator for web projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShahbaziRaz/web-class-obfuscator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "web-obfuscate=web_obfuscator:main",
        ],
    },
    include_package_data=True,
)