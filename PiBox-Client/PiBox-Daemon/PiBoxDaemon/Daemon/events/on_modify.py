from PiBoxDaemon.Daemon import sync
from PiBoxDaemon.config import TO_IGNORE, DIRECTORY

def on_modify(event):
    # Check if the event is in TO_IGNORE
    for extension in TO_IGNORE:
        if (extension in event.src_path):
            return

    # Sync the folder we a modifying
    event.src_path.split(DIRECTORY)
    sync.syncDirectory(''.join(event.src_path.split(DIRECTORY)))