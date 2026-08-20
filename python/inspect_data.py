import pandas as pd
from pathlib import Path

DATA_DIR = Path("../data")

print("Files found:")
for file in DATA_DIR.iterdir():
    print(file.name)