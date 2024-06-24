import os
import logging
import time

from shutil import move
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directories

source_dir = "C:/Users/kenes/Downloads"
dest_dir_audio = "C:/Users/kenes/Downloads/Audio"
dest_dir_video = "C:/Users/kenes/Downloads/Video"
dest_dir_image = "C:/Users/kenes/Downloads/Images"
dest_dir_documents = "C:/Users/kenes/Downloads/Documents"

# Extensions

audio_extensions = [".flac", ".mp3", ".wav"]
video_extensions = [".mp4", ".avi", ".mov", ".wmv"]
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".psd", ".svg"]
document_extensions = [".docx", ".txt", ".pdf"]

# DownloadManager Class

class DownloadManager(FileSystemEventHandler):

    def check_file_extension(self, name, extensions):
        for extension in extensions:
            if name.endswith(extension): return True
        return False

    def on_created(self, event):
        if event.is_directory: return None

        name = os.path.basename(event.src_path)
        dest = source_dir

        try:
            if self.check_file_extension(name, audio_extensions): dest = dest_dir_audio
            elif self.check_file_extension(name, video_extensions): dest = dest_dir_video
            elif self.check_file_extension(name, image_extensions): dest = dest_dir_image
            elif self.check_file_extension(name, document_extensions): dest = dest_dir_documents

            if dest != source_dir:
                destination_path = os.path.join(dest, name)
                for _ in range(3):
                    try:
                        move(event.src_path, destination_path)
                        logging.info(f"Moved {name} to {dest}")
                        print(f"Moved {name} to {dest}")
                        break
                    except PermissionError as e:
                        logging.warning(f"PermissionError: {e}. Retrying in 1 second...")
                        time.sleep(1)
            else:
                logging.error(f"Failed to move {name} after several attempts.")
                print(f"Failed to move {name} after several attempts.")

        except Exception as e:
            logging.error(f"Error moving file {name}: {e}")
            print(f"Error moving file {name}: {e}")

# Main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = source_dir
    event_handler = DownloadManager()

    observer = Observer()
    observer.schedule(event_handler, path, recursive = True)
    observer.start()

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()