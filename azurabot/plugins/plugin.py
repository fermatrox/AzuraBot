"""
The base Plugin class file.

All other plugins inherit this class, directly or indirectly.
"""


class Plugin:

    def __init__(self):
        self.name = "(unnamed plugin)"

    def log(self, msg):
        print(f"[{self.name}] {msg}")
