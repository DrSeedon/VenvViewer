# VenvAnalyzer

## Table of Contents

*   [English](#english)
*   [Русский](#русский)

---

<a name="english"></a>

## English

### Overview

VenvAnalyzer is a simple Python script designed to help you analyze the disk space usage of modules within your global and virtual Python environments. It generates a detailed text report and illustrative graphs (horizontal bar charts) showing the size of each module and its percentage contribution to the total environment size.

### Features

*   **Global and Local Environment Analysis:** Scans modules in the active virtual environment and attempts to locate other virtual environments in the current directory, as well as the global Python environment.
*   **Text Report:** Saves a detailed summary of modules (size in MB and percentage of total volume) to an easy-to-read text file.
*   **Data Visualization:** Generates PNG graphs (horizontal bar charts) for each environment, clearly demonstrating the distribution of module sizes (Top-15 + Others).
*   **Standalone Executable:** Can be compiled into an `.exe` file for execution without a Python installation (requires PyInstaller).

### Usage

#### Running as a Python Script

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd VenvViewer
    ```
2.  **Install dependencies:**
    For proper script functionality (especially for graph generation), you will need `matplotlib`.
    ```bash
    pip install matplotlib
    ```
3.  **Run the script:**
    Navigate to the directory containing `venv_memory_analyzer.py` and execute:
    ```bash
    python venv_memory_analyzer.py
    ```
    A report (`venv_analysis_report_YYYYMMDD_HHMMSS.txt`) and graphs (`venv_analysis_global_environment_YYYYMMDD_HHMMSS.png`, `venv_analysis_discovered_environment_venv_name_YYYYMMDD_HHMMSS.png`) will be created in the same directory as the script.

#### Running as an Executable (.exe)

If you are using the `.exe` version (assuming it was compiled with PyInstaller):

1.  **Copy `VenvAnalyzer.exe`** to any folder you wish to analyze (e.g., a folder containing your `venv` virtual environment).
2.  **Double-click** `VenvAnalyzer.exe`.
3.  **Results:** In the same folder as `VenvAnalyzer.exe`, the following will be generated:
    *   Text report: `venv_analysis_report_YYYYMMDD_HHMMSS.txt`
    *   One or more graphs: `venv_analysis_global_environment_YYYYMMDD_HHMMSS.png`, `venv_analysis_discovered_environment_venv_name_YYYYMMDD_HHMMSS.png`, etc.

### Building the Executable (.exe) from Source

To build your own executable, you will need `PyInstaller`.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Build the `.exe`:**
    Navigate to the directory containing `venv_memory_analyzer.py` and execute:
    ```bash
    pyinstaller --onefile --name VenvAnalyzer venv_memory_analyzer.py
    ```
    The `VenvAnalyzer.exe` executable will be created in the `dist` folder within the project's root directory.

### Notes

*   **Memory vs. Disk Space Measurement:** The script measures the **disk space** occupied by modules in the `site-packages` folder, not their actual runtime RAM consumption. This is a more practical way to assess the "weight" of installed packages.
*   **"Unnecessary" Modules:** The definition of "unnecessary" modules depends on your specific projects and needs. The script provides data to help you decide whether to remove unused packages.

### License

This project is distributed under the MIT License. See the `LICENSE` file (if applicable) for details.

---

<a name="русский"></a>

## Русский

### Обзор

VenvAnalyzer — это простой Python-скрипт, который помогает анализировать использование дискового пространства модулями в ваших глобальных и виртуальных окружениях Python. Он генерирует подробный текстовый отчет и наглядные графики (горизонтальные гистограммы), показывающие размеры каждого модуля и их процентный вклад в общий объем окружения.

### Возможности

*   **Анализ локальных и глобальных окружений:** Сканирует модули в активном виртуальном окружении, а также пытается найти другие виртуальные окружения в текущей директории и глобальное окружение Python.
*   **Отчет в текстовом файле:** Сохраняет детализированную сводку по модулям (размер в МБ и процент от общего объема) в удобный для чтения текстовый файл.
*   **Визуализация данных:** Генерирует PNG-графики (горизонтальные гистограммы) для каждого окружения, наглядно демонстрируя распределение размеров модулей (Топ-15 + Прочие).
*   **Автономная работа:** Может быть скомпилирован в исполняемый `.exe` файл для запуска без установки Python (требует PyInstaller).

### Использование

#### Запуск как Python-скрипта

1.  **Клонируйте репозиторий** (если вы еще этого не сделали):
    ```bash
    git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
    cd VenvViewer
    ```
2.  **Установите зависимости:**
    Для корректной работы скрипта (особенно для генерации графиков) вам понадобится `matplotlib`.
    ```bash
    pip install matplotlib
    ```
3.  **Запустите скрипт:**
    Перейдите в директорию, содержащую `venv_memory_analyzer.py`, и выполните:
    ```bash
    python venv_memory_analyzer.py
    ```
    Отчет (`venv_analysis_report_ГГГГММДД_ЧЧММСС.txt`) и графики (`venv_analysis_global_окружение_ГГГГММДД_ЧЧММСС.png`, `venv_analysis_обнаруженное_окружение_имя_venv_ГГГГММДД_ЧЧММСС.png`) будут созданы в той же директории, где находится скрипт.

### Запуск как исполняемого файла (.exe)

Если вы используете версию `.exe` (предполагается, что она была скомпилирована с помощью PyInstaller):

1.  **Скопируйте `VenvAnalyzer.exe`** в любую папку, которую вы хотите проанализировать (например, в папку, содержащую ваше виртуальное окружение `venv`).
2.  **Дважды кликните** по `VenvAnalyzer.exe`.
3.  **Результаты:** В той же папке, где находится `VenvAnalyzer.exe`, будут сгенерированы:
    *   Текстовый отчет: `venv_analysis_report_ГГГГММДД_ЧЧММСС.txt`
    *   Один или несколько графиков: `venv_analysis_global_окружение_ГГГГММДД_ЧЧММСС.png`, `venv_analysis_обнаруженное_окружение_имя_venv_ГГГГММДД_ЧЧММСС.png` и т.д.

## Сборка исполняемого файла (.exe) из исходного кода

Для сборки собственного исполняемого файла вам понадобится `PyInstaller`.

1.  **Установите PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Соберите `.exe`:**
    Перейдите в директорию, содержащую `venv_memory_analyzer.py`, и выполните:
    ```bash
    pyinstaller --onefile --name VenvAnalyzer venv_memory_analyzer.py
    ```
    Исполняемый файл `VenvAnalyzer.exe` будет создан в папке `dist` в корневой директории проекта.

## Примечания

*   **Измерение памяти vs. Дисковое пространство:** Скрипт измеряет **дисковое пространство**, занимаемое модулями в папке `site-packages`, а не их реальное потребление оперативной памяти во время выполнения. Это более практичный способ оценить "вес" установленных пакетов.
*   **"Лишние" модули:** Определение "лишних" модулей зависит от ваших конкретных проектов и потребностей. Скрипт предоставляет данные, которые помогут вам принять решение об удалении неиспользуемых пакетов.

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле `LICENSE` (если применимо). 