import sys

from pathlib import Path
from importlib.resources import files
from .resources import find_resource

try:
    import yaml
except ImportError:
    print("[!] Ошибка: Не установлена библиотека PyYAML.")
    print("Установите зависимости: pip install pyyaml")
    sys.exit(1)



def load_config():
    yml_path = find_resource("config.yml")

    if yml_path is None or not yml_path.exists():
        print("[!] КРИТИЧЕСКАЯ ОШИБКА: Файл конфигурации не найден!")
        print("Проверенные пути:")
        print(f"  - {Path.cwd() / 'config.yml'} (текущая директория)")
        if getattr(sys, 'frozen', False):
            print(f"  - {Path(sys.executable).parent / 'config.yml'} (рядом с exe)")
        print(f"  - dpi_detector/data/config.yml (внутри пакета)")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    try:
        with open(yml_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)

        if not isinstance(config_data, dict):
            raise ValueError("Файл config.yml пуст или имеет неверный формат.")

        for key, value in config_data.items():
            if key.isupper():
                globals()[key] = value

    except Exception as e:
        print(f"[!] КРИТИЧЕСКАЯ ОШИБКА при чтении config.yml:")
        print(f"{e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)


load_config()
