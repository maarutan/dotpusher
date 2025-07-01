from setuptools import setup, find_packages

setup(
    name="dotpusher",
    version="0.1.3",
    description="Dotpusher is a declarative method for synchronizing local files or directories with remote ones using git.",
    author="Marat Arzymatov",
    author_email="maratarzymatov288@gmail.com",
    url="https://github.com/maarutan/dotpusher",
    packages=find_packages(include=["core", "modules", "core.*", "modules.*"]),
    python_requires=">=3.8",
    install_requires=[
        "argcomplete>=3.6.2",
        "setuptools>=80.9.0",
        "wheel>=0.45.1",
    ],
    entry_points={
        "console_scripts": [
            "dotpusher=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
