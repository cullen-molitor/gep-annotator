import subprocess
import time

from config import TARGET_KML_PATH


def launch_gep() -> None:
    print("Launching Google Earth Pro...")
    subprocess.Popen(["open", "-a", "Google Earth Pro"])
    print("Waiting for Google Earth Pro to initialize...")
    time.sleep(5)
    print("Ready.\n")


def open_target_kml() -> None:
    subprocess.Popen(
        ["open", "-a", "Google Earth Pro", str(TARGET_KML_PATH.resolve())]
    )
