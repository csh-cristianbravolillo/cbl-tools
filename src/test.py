from cbl_tools import cylon_config

x = cylon_config.CylonConfig("/home/cbravo/lib")

print(f"sections: {x.values.sections()}")

for sect in x.sections():
    print(f"Section: {sect}")
    for opt in x.items(sect):
        print(f"\t({opt}) = ({x.get(sect, opt)})")
