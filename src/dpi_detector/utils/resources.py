import sys
from pathlib import Path
from importlib.resources import files


def find_resource(filename: str) -> Path | None:
    """
    Ищет файл ресурса в следующем порядке:
    1. В текущем рабочем каталоге (переопределение пользователем)
    2. Рядом с .exe (для PyInstaller)
    3. Внутри пакета dpi_detector.data (дефолтный ресурс)
    
    Возвращает Path к найденному файлу или None, если файл не найден.
    """
    # 1. Сначала ищем в текущей директории запуска
    local_path = Path.cwd() / filename
    if local_path.exists():
        return local_path

    # 2. Если запущено из собранного .exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        # Сначала рядом с exe (пользователь может положить свой файл)
        external = exe_dir / filename
        if external.exists():
            return external
        # Потом внутри архива PyInstaller
        meipass = Path(getattr(sys, '_MEIPASS', exe_dir)) / filename
        if meipass.exists():
            return meipass

    # 3. Ищем внутри пакета через importlib.resources
    try:
        data_dir = files("dpi_detector.data")
        package_path = Path(str(data_dir / filename))
        if package_path.exists():
            return package_path
    except (ModuleNotFoundError, TypeError):
        pass

    return None
