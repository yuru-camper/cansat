import json
from pprint import pprint

with open("G:\end2end\log.json", 'r') as f:
    log = json.load(f)

log_sorted = sorted(log.items(), key=lambda x: int(x[0]))

with open("C:\\Users\大貴\Desktop\cansat関連\log.json", 'w') as f:
    json.dump(log_sorted, f, indent='\t')