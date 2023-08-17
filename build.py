import PyInstaller.__main__
import sys

if __name__ == '__main__':
    # env_path = '.env'
    # if sys.platform == 'win32':
    #     env_path += ';'
    # else:
    #     env_path += ':'
    # env_path += '.env'
    PyInstaller.__main__.run(
        [
            "src/main.py",
            "-F",
            "-n", "python_app",
            # "--add-data", env_path,
            "--exclude-module", "pyinstaller",
            "--exclude-module", "pyinstaller-hooks-contrib",
            "--exclude-module", "setuptools",
        ]
    )
