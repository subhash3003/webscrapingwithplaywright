import json
import pandas as pd

def save_output(data, file_type="json"):
    if file_type == "json":
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return "output.json"

    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)
    return "output.xlsx"
