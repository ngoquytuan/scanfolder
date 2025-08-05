import tkinter as tk
from tkinter import filedialog
import os
import csv
from datetime import datetime
import json
import logging
import stat

class FolderScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Scanner")
        self.root.geometry("600x400")

        self.config = self.load_config()
        self.setup_logging()

        # Create GUI elements
        self.select_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=20)

        self.status_label = tk.Label(root, text="No folder selected", wraplength=500)
        self.status_label.pack(pady=10)

        self.scan_button = tk.Button(root, text="Scan and Generate Report", command=self.scan_folder)
        self.scan_button.pack(pady=20)

        self.result_text = tk.Text(root, height=10, width=60)
        self.result_text.pack(pady=20)

        self.selected_folder = None

    def load_config(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'config.json')
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error("config.json not found. Using default values.")
            return {
                "log_file": "folder_scan.log",
                "max_files_to_scan": 1000,
                "generate_tree_limit": 100,
                "scan_hidden_files": True
            }

    def setup_logging(self):
        log_file = self.config.get('log_file', 'folder_scan.log')
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.status_label.config(text=f"Selected folder: {self.selected_folder}")

    def is_hidden(self, filepath):
        """Checks if a file or directory is hidden."""
        try:
            # For Windows
            if os.name == 'nt':
                attrs = os.stat(filepath).st_file_attributes
                return attrs & stat.FILE_ATTRIBUTE_HIDDEN
            # For Unix-like systems
            else:
                return os.path.basename(filepath).startswith('.')
        except OSError:
            return False

    def _generate_tree_map(self, folder, file_limit):
        tree_string = f"# Folder Tree for `{folder}`\n\n"
        file_count = 0
        scan_hidden = self.config.get("scan_hidden_files", True)

        for root, dirs, files in os.walk(folder):
            if not scan_hidden:
                dirs[:] = [d for d in dirs if not self.is_hidden(os.path.join(root, d))]
                files = [f for f in files if not self.is_hidden(os.path.join(root, f))]

            level = root.replace(folder, '').count(os.sep)
            indent = ' ' * 4 * level
            tree_string += f"{indent}📂 {os.path.basename(root)}/\n"
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if file_count < file_limit:
                    tree_string += f"{sub_indent}📄 {f}\n"
                    file_count += 1
                else:
                    break
            if file_count >= file_limit:
                tree_string += f"{sub_indent}...\n"
                break
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, 'output.md')
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(tree_string)
        logging.info(f"Generated folder tree map in {output_path}")

    def scan_folder(self):
        if not self.selected_folder:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please select a folder first!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"folder_scan_{timestamp}.csv"
        
        try:
            file_count = 0
            scan_hidden = self.config.get("scan_hidden_files", True)
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['File Name', 'Size (bytes)', 'Path'])
                
                for root, dirs, files in os.walk(self.selected_folder):
                    if not scan_hidden:
                        dirs[:] = [d for d in dirs if not self.is_hidden(os.path.join(root, d))]
                        files = [f for f in files if not self.is_hidden(os.path.join(root, f))]

                    for file in files:
                        if file_count >= self.config['max_files_to_scan']:
                            logging.warning(f"Reached max file scan limit of {self.config['max_files_to_scan']}.")
                            break
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        writer.writerow([file, file_size, file_path])
                        file_count += 1
                    if file_count >= self.config['max_files_to_scan']:
                        break
            
            if file_count < self.config['generate_tree_limit']:
                self._generate_tree_map(self.selected_folder, self.config['generate_tree_limit'])

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Scan complete!\nReport saved as: {csv_filename}\nFound {file_count} files.")
            logging.info(f"Scan complete. Report: {csv_filename}. Found {file_count} files.")

        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error occurred: {str(e)}")
            logging.error(f"An error occurred during scanning: {e}", exc_info=True)

def main():
    root = tk.Tk()
    app = FolderScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
