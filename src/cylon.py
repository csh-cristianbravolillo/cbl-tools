import sys
from cbl_tools import skin
from termcolor import colored

if __name__ == '__main__':
    # En esta parte la interfaz puede hacerse cargo de buscar un folder desde donde cargar un skin.
    # Pero de momento, lo que hacemos simplemente es confiar en que tenemos un folder en un lugar
    # estándar.

    #> Creamos un skin
    skin = skin.Skin("/home/cbravo/lib")
    args = sys.argv[1:]

    #> Help
    if len(args) == 0 or args[0] == 'help':
        print(colored('cylon', 'red'), "- Get skins and use them to keep your desk sync")
        print("\tcylon info: Displays info about the current copy.")
        print("\tcylon pull|push: Does a pull|push from/to the remote and reports the result.")
        print("\tcylon list: Lists all available remotes to download")
        exit()

    #> El resto de los argumentos
    match args[0]:
        case 'info':
            base = skin.section('base')
            local = skin.section('local')
            remote = skin.section('remote')
            print(colored(f"{local['system']} {local['machine']} ({local['node']})", 'light_blue'), f"update:{base['update']}", base['last_modified'])
            print(colored(local['id'], 'red'), f"({local['description']}):", colored(f"{remote['server']}:{remote['path']}", 'red'))

        case 'list':
            pass

        case 'pull':
            pass

        case 'push':
            pass

        case _:
            print(f"What is that? {args[0]}?")
