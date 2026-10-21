import pandas as pd
import numpy as np
import seaborn as sns
import os

def read_file(file_path):

    data = pd.read_csv(file_path)
    print(data.info())
    # data.to_csv(os.path.join("file", "Games_2.csv"), decimal=";", index=False)
    print(data["year"])
    

if __name__=="__main__":
    path_to_file = os.path.join("file","Games_2.csv")
    read_file(path_to_file)