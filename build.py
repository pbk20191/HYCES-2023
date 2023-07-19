import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run(
        [
            "src/main.py",
            "-F",
            "--path", "venv/lib/python3.11/site-packages",
            "-n", "python_app",
        ]
    )
