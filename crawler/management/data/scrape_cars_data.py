# Scrape data from back4app

import json
import requests
import pandas as pd

try:
    headers = {
        "X-Parse-Application-Id": "",
        "X-Parse-Master-Key": "",
    }
    i = 0
    df = pd.DataFrame({"Make": [], "Model": [], "Year": []})
    while True:
        print(f"Running another {i}")
        url = f"https://parseapi.back4app.com/classes/Car_Model_List?skip={i}&limit=100"
        data = json.loads(requests.get(url, headers=headers).content.decode("utf-8"))["results"]
        if len(data) == 0:
            break

        df_new = pd.DataFrame({"Make": [], "Model": [], "Year": []})
        for car in data:
            df_new = df_new._append({"Make": car["Make"], "Model": car["Model"], "Year": car["Year"]}, ignore_index=True)

        df = pd.concat([df, df_new])
        i += 100
except KeyboardInterrupt:
    df = df.sort_values("Make")
    df.to_csv("data.csv", encoding="utf-8", index=False)
else:
    df = df.sort_values("Make")
    df.to_csv("data.csv", encoding="utf-8", index=False)
