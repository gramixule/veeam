import os
import shutil
import time
import argparse
from datetime import datetime


def sync_folders(source_path, replica_path, log_file):
    try:
        # Check if source folder exists
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source folder '{source_path}' does not exist.")

        # Create replica folder if it doesn't exist
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)

        # Sync source folder to replica folder
        for root, _, files in os.walk(source_path):
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_path, os.path.relpath(source_file, source_path))

                if not os.path.exists(replica_file) or (os.path.getmtime(source_file) > os.path.getmtime(replica_file)):
                    shutil.copy2(source_file, replica_file)
                    log_operation(log_file, f"Copied {source_file} to {replica_file}")

        # Remove files in replica folder that don't exist in source folder
        for root, _, files in os.walk(replica_path):
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_path, os.path.relpath(replica_file, replica_path))

                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    log_operation(log_file, f"Removed {replica_file}")

    except Exception as e:
        log_operation(log_file, f"Error: {str(e)}")


def log_operation(log_file, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    # Log to console
    print(log_message)

    # Log to file
    with open(log_file, "a") as file:
        file.write(log_message + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source_path", help="Source folder path")
    parser.add_argument("replica_path", help="Replica folder path")
    parser.add_argument("sync_interval", type=int, help="Synchronization interval (in seconds)")
    parser.add_argument("log_file", help="Log file path")

    args = parser.parse_args()

    while True:
        sync_folders(args.source_path, args.replica_path, args.log_file)
        time.sleep(args.sync_interval)
