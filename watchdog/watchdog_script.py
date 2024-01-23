import sys
import time
import logging
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'modified' and event.src_path == self.csv_path:
            # Run the script only when the specified CSV file is modified
            logging.info(f"CSV file modified: {event.src_path}")
            script_path = os.path.join(os.path.dirname(__file__), 'pytest.py')
            subprocess.run(["python", script_path])

if __name__ == "__main__":

    # define csv path
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    end_path = '00_Project_Zero_2.0.csv'
    csv_path = os.path.join(root_path, 'watchdog', end_path)

    # print welcome message
    print('--------------------------')
    print('* Watchdog is monitoring *')
    print('--------------------------')
    print("  / \\__")
    print(" (    @\\____")
    print(" /           O")
    print("/   (_____/")
    print("/_____/   U")
    print("                          ")
    print(csv_path)

    # print logging information
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


    event_handler = CustomEventHandler(csv_path)
    observer = Observer()
    observer.schedule(event_handler, root_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
