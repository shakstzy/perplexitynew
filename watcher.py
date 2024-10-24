import time
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

def compute_file_hash(file_path):
    """Compute the MD5 hash of the file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_hash = compute_file_hash("text.txt")

    def on_modified(self, event):
        if event.src_path.endswith("text.txt"):
            current_hash = compute_file_hash("text.txt")
            if current_hash != self.last_hash:
                print(f"{event.src_path} has been modified. Running textparser.py...")
                subprocess.run(["python", "textparser.py"])
                # Update the hash after running the parser
                self.last_hash = compute_file_hash("text.txt")

if __name__ == "__main__":
    path = "."
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()