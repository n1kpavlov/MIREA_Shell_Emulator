import tarfile
import xml.etree.ElementTree as ET
import tkinter as tk
import os

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.tar_path = None
        self.start_script_path = None
        self.load_config()

    def load_config(self):
        tree = ET.parse(self.config_file)
        root = tree.getroot()
        self.tar_path = root.find('tar_path').text
        self.start_script_path = root.find('start_script_path').text

class FileSystem:
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.root = '/'
        self.current_dir = self.root
        self.file_system = {}
        self.load_tar()

    def load_tar(self):
        with tarfile.open(self.tar_path, 'r') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    self.file_system[member.name] = {
                        'type': 'file',
                        'size': member.size,
                        'content': tar.extractfile(member).read().decode('utf-8')
                    }
                else:
                    self.file_system[member.name] = {
                        'type': 'dir',
                        'size': None,
                        'content': None
                    }

class ShellGUI:
    def __init__(self, config):
        self.config = config
        self.file_system = FileSystem(self.config.tar_path)
        self.root = tk.Tk()
        self.root.title('Shell Emulator')

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(self.output_frame, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X)

        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.root.mainloop()

if __name__ == '__main__':
    config = Config('config.xml')
    shell_gui = ShellGUI(config)
