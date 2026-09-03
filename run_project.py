import os
import webbrowser
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def main():
    os.chdir(BASE_DIR)
    print("My Lab Documentation Hub")
    print("Applying migrations...")
    os.system("python manage.py migrate")
    print()
    print("Project is starting on http://127.0.0.1:8000/")
    print("Admin login:")
    print("Username: Gulshan")
    print("Password: 369963")
    print()
    webbrowser.open("http://127.0.0.1:8000/")
    os.system("python manage.py runserver")


if __name__ == "__main__":
    main()
