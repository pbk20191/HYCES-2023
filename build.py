import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run(
        [
            "src/main.py",
            "-F",
            "-n", "python_app",
            "--add-data", ".env:."
        ]
    )
