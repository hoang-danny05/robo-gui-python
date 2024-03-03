import json
import glob

properties = {
    # "name": 0,
    "tape": 1,
    "tube": 1,
    "tray": 0,
    "custom": 0
}

fextension = "./components/*"
comps = glob.glob(fextension)

for c in comps:
    c = c[len(fextension)-1:]
    fpath = fextension[:-1]+c
    print(fpath)
    with open(fpath, "w") as file:
        file.write(json.dumps(properties))