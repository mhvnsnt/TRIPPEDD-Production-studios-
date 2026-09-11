import sys,yaml
p=sys.argv[1]
with open(p,encoding="utf-8") as f: data=yaml.safe_load(f)
for x in data["projects"]:
    print(x["name"], x["repo"])
