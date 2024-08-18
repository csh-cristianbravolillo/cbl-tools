from cbl_tools import skin

skin = skin.Skin("/home/cbravo/lib")

for section in skin.sections():
    print(f"Section: {section}")
    for opt in skin.keys(section):
        print(f"\t({opt}) = ({skin.get(section, opt)})")

print("---------------------")
print(skin.items('symlinks'))
