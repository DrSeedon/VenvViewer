import os
import sys
import site
from collections import defaultdict
import datetime
import re
try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("\nWarning: 'matplotlib' module not found. Graphs will not be generated.", file=sys.stderr)

def get_dir_size(path):
    """Calculates the total size of a directory."""
    total_size = 0
    if os.path.exists(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Skip symbolic links that could lead to infinite loops
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def get_site_packages_path(base_path):
    """Determines the site-packages path based on the base Python installation path."""
    if sys.platform == "win32":
        return os.path.join(base_path, 'Lib', 'site-packages')
    else: # Unix/macOS
        # For global, it's typically pythonX.Y/site-packages
        # For venv, it's typically lib/pythonX.Y/site-packages
        return os.path.join(base_path, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')

def analyze_site_packages(site_packages_path, env_name, output_dir, timestamp):
    """
    Analyzes disk space usage of packages in a given site-packages directory.
    Note: This measures disk space, not actual runtime memory usage.
    """
    print(f"\n--- Environment Analysis: {env_name} ({site_packages_path}) ---")
    if not os.path.exists(site_packages_path):
        print("Site-packages directory not found or inaccessible.")
        return

    package_sizes = {}
    total_env_size = 0

    # Iterate through each item in site-packages to find package directories
    for item_name in os.listdir(site_packages_path):
        item_path = os.path.join(site_packages_path, item_name)
        if os.path.isdir(item_path):
            # A simple heuristic: consider top-level directories in site-packages as packages/modules.
            # This covers most installed packages.
            package_size = get_dir_size(item_path)
            package_sizes[item_name] = package_size
            total_env_size += package_size
        elif os.path.isfile(item_path) and item_name.endswith(('.py', '.egg-info', '.dist-info')):
            # Also include top-level .py files and metadata files if they represent modules
            file_size = os.path.getsize(item_path)
            package_sizes[item_name] = file_size
            total_env_size += file_size


    if not package_sizes:
        print("No modules found.")
        return

    sorted_packages = sorted(package_sizes.items(), key=lambda item: item[1], reverse=True)

    print(f"\nTotal environment size: {total_env_size / (1024*1024):.2f} MB\n")
    print("Module summary:")
    for package, size in sorted_packages:
        percentage = (size / total_env_size) * 100 if total_env_size > 0 else 0
        print(f"- {package}: {size / (1024*1024):.2f} MB ({percentage:.2f}%)")

    if MATPLOTLIB_AVAILABLE:
        generate_module_size_chart(sorted_packages, total_env_size, env_name, output_dir, timestamp)

def generate_module_size_chart(sorted_packages, total_env_size, env_name, output_dir, timestamp, top_n=15):
    # Take top-N modules
    top_modules = sorted_packages[:top_n]
    other_size = sum(size for _, size in sorted_packages[top_n:])

    labels = [pkg for pkg, _ in top_modules]
    sizes = [size for _, size in top_modules]

    if other_size > 0:
        labels.append("Others")
        sizes.append(other_size)

    # Convert sizes to MB for plotting
    sizes_mb = [s / (1024*1024) for s in sizes]

    # Calculate percentages for labels
    percentages = [(s / total_env_size) * 100 if total_env_size > 0 else 0 for s in sizes]
    plot_labels = [f'{label} ({p:.2f}%)' for label, p in zip(labels, percentages)]

    fig, ax = plt.subplots(figsize=(10, 0.5 * len(labels) + 2)) # Dynamic figure height
    y_pos = range(len(labels))
    ax.barh(y_pos, sizes_mb, align='center', color='skyblue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_labels)
    ax.invert_yaxis()  # top to bottom
    ax.set_xlabel('Size (MB)')
    ax.set_title(f'Module Size Distribution in {env_name} (Top {top_n} + Others)')

    # Adjust x-axis to show MB with two decimal places
    formatter = mticker.FormatStrFormatter('%.2f')
    ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()
    # Sanitize environment name for filename
    cleaned_env_name = re.sub(r'[^a-zA-Z0-9_]', '', env_name).lower()
    chart_filename = f"venv_analysis_{cleaned_env_name}_{timestamp}.png"
    chart_filepath = os.path.join(output_dir, chart_filename)
    plt.savefig(chart_filepath)
    plt.close(fig)
    print(f"Graph saved to: {chart_filepath}")

def main():
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"venv_analysis_report_{timestamp}.txt"
    output_filepath = os.path.join(script_dir, output_filename)

    original_stdout = sys.stdout
    try:
        output_file = open(output_filepath, 'w', encoding='utf-8')
        sys.stdout = output_file
        print(f"Results will be saved to: {output_filepath}\n")
    except IOError as e:
        sys.stdout = original_stdout
        print(f"Error opening file {output_filepath}: {e}", file=sys.stderr)
        sys.exit(1)
        return

    print("Scanning virtual environments and modules...\n")

    # Global environment
    global_site_packages_path = None
    try:
        global_site_packages_path = get_site_packages_path(sys.base_prefix)

        if global_site_packages_path and os.path.exists(global_site_packages_path):
            analyze_site_packages(global_site_packages_path, "Global Environment", script_dir, timestamp)
        else:
            print(f"Failed to determine global site-packages path via {sys.base_prefix}. Trying site.getsitepackages()...")
            for p in site.getsitepackages():
                if sys.base_prefix in p and os.path.exists(p):
                    global_site_packages_path = p
                    analyze_site_packages(global_site_packages_path, "Global Environment (from site.getsitepackages())", script_dir, timestamp)
                    break
            if not global_site_packages_path:
                print("Could not find global site-packages directory.")

    except Exception as e:
        print(f"Error analyzing global environment: {e}")

    # Current local environment (if active)
    if sys.prefix != sys.base_prefix:
        print("\nSearching for current local environment...")
        current_venv_site_packages_path = None
        try:
            current_venv_site_packages_path = get_site_packages_path(sys.prefix)

            if current_venv_site_packages_path and os.path.exists(current_venv_site_packages_path):
                if current_venv_site_packages_path != global_site_packages_path:
                    analyze_site_packages(current_venv_site_packages_path, "Current Local Environment (activated)", script_dir, timestamp)
                else:
                    print("Current environment matches global environment.")
            else:
                print(f"Failed to determine site-packages path for current local environment via {sys.prefix}.")

        except Exception as e:
            print(f"Error analyzing current local environment: {e}")

    # Scan for other local venvs in the current directory
    print("\nSearching for other virtual environments in the current directory...")
    found_other_venvs = False
    for item in os.listdir('.'):
        potential_venv_path = os.path.abspath(item)
        if os.path.isdir(potential_venv_path) and (item.lower() == 'venv' or item.lower() == '.venv' or 'env' in item.lower()):
            venv_site_packages = get_site_packages_path(potential_venv_path)

            if (venv_site_packages and os.path.exists(venv_site_packages) and
                venv_site_packages != global_site_packages_path and
                (sys.prefix == sys.base_prefix or venv_site_packages != current_venv_site_packages_path)):
                analyze_site_packages(venv_site_packages, f"Discovered Environment: {item}", script_dir, timestamp)
                found_other_venvs = True

    if not found_other_venvs and (sys.prefix == sys.base_prefix):
        print("No other virtual environments found in the current directory.")
    elif not found_other_venvs and (sys.prefix != sys.base_prefix):
        print("No other virtual environments found in the current directory besides the active one.")

    # Close the file and restore stdout
    output_file.close()
    sys.stdout = original_stdout # Restore original stdout

    sys.exit(0)

if __name__ == "__main__":
    main() 