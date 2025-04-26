# utils/logger.py

import datetime

class Logger:
    @staticmethod
    def Log_info(msg):
        print(f"[INFO] {Logger._timestamp()} - {msg}")

    @staticmethod
    def Log_warning(msg):
        print(f"[WARNING] {Logger._timestamp()} - {msg}")

    @staticmethod
    def Log_error(msg):
        print(f"[ERROR] {Logger._timestamp()} - {msg}")

    @staticmethod
    def _timestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")