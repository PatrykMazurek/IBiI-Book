import os.path, sys
import numpy as np
import pandas as pd

from parse import parse

# path_to_file = os.path.join("file", "OpenSSH", "OpenSSH_2k_log_structured.csv")
path_to_file = os.path.join("file", "OpenSSH", "OpenSSH_2k.log")
list_record = []
with open(path_to_file, "r") as f:
    pattern = "{month} {day} {time} {component} sshd[{pid}]"
    for line in f.readlines():
        # print(line)
        temp_line = line.split(": ")
        # print(temp_line[0])
        result = parse(pattern, temp_line[0])
        # result["context"] =
        result.named["context"] = temp_line[1]
        list_record.append(result.named)
df = pd.DataFrame(list_record, columns=["month", "day", "time", "component", "pid", "context"])
# df = pd.read_csv(path_to_file)
# print(df.info())
# df['Date'] = pd.to_datetime(df['Date'])
print(df.info())


# error_reg = df[df["msg"].str.contains("No instance found for any event")]["req_id"].unique()
# print(error_reg)
