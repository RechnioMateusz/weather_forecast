import os
import sys

RESOURCES_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_PATH = os.path.dirname(RESOURCES_PATH)
HARDWARE_PATH = os.path.join(MAIN_PATH, "hardware")
DB_PATH = os.path.join(MAIN_PATH, "wf_mes.db")
