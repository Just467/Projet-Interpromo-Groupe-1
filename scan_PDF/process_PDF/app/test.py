import pandas as pd

import sys
import os
sys.path.append("scan_pdf/utils")
from table_viewer import show_table

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Score": [85, 90, 95]
}
df = pd.DataFrame(data)
show_table(df)