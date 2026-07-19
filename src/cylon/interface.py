import sys, getopt
import os.path
import cylon

class interface:
    """Parsea la línea de comando, recupera los argumentos y opciones, y los guarda para consulta posterior en el diccionario 'model'.
    'model' tiene dos elementos: 'opts', que es a su vez un diccionario con todas las opciones especificadas por CLI, y 'args', que guarda
    los argumentos especificados. De momento estamos usando solo un argumento.
    """
    model = {}
    verbose = False

    def __init__(self, options:str = '') -> None:
        """Toma cada uno de los caracteres en 'options' y revisa si recibió alguno como opción en la CLI. Si detecta una opción en la CLI
        que no fue especificada en 'options', termina con un error."""

        try:
            opts,args = getopt.getopt(sys.argv[1:], options)

        except getopt.GetoptError as err:
            cylon.cprint(f"[r|{err}]. Giving up.\n")
            exit(1)

        self.model = {
            'opts': {},
            'args': args
        }

        for i in options:
            self.model['opts'][i] = False

        for opt,_ in opts:
            opt = opt[1:]
            self.model['opts'][opt] = True

        if self.is_opt('v'):
            self.verbose = True

    def assert_command(self, comm:str) -> bool:
        """Chequea si el comando en línea de comando es 'comm'."""
        if self.model['args'] and len(self.model['args'])>0 and self.model['args'][0] == comm:
            if self.verbose:
                cylon.cprint(f"\b\b> {comm}")
            return True
        else:
            return False

    def is_opt(self, opt:str) -> bool:
        """Chequea si la opción 'opt' fue indicada por CLI."""
        return opt != "" and opt in self.model['opts'] and self.model['opts'][opt]

    def output(self, msg:str, msg_v:str = ''):
        """Si estamos en modo "simple", imprime 'msg'; si estamos en modo verboso, imprime 'msg_v'."""
        cylon.cprint(msg) if not self.verbose else cylon.cprint(msg_v)

    def ask_yes_no(self, txt:str, default:str = 'y', quit_if_yes:bool = False, quit_if_no:bool = False) -> str:
        """Presenta el texto 'txt', y pregunta 'sí' (y) o 'no' (n). Usa 'default' para decidir cuál de las dos opciones es la
        default; si el usuario no ingresa nada, se entiende que escoge la opción default."""
        print(txt + " ", end='')

        match default:
            case 'y':
                qst = "Y/n"
            case 'n':
                qst = "y/N"
            case _:
                qst = "y/n"

        res = input(f"({qst}): ")

        if res == '' and default in ['y','n']:
            res = default

        if (quit_if_yes and res=='y') or (quit_if_no and res=='n'):
            print("OK, no problem")
            exit(0)

        return res

    def ask_for_options(self, options:dict[str,str], question:str) -> str:
        """Presenta la lista 'options' de forma numerada, luego presenta el texto 'question', y pide ingresar un número para las opciones.
        El número 0 se usa para salir del menú."""
        i=0

        cylon.cprint("\t[b|quit> Quit!]\n")
        for tmp in options:
            cylon.cprint(f"\t[b|{tmp}> {options[tmp]}]\n")

        key = ''
        while key == '' or key not in options:
            key = input(question + ' ')

        if key == 'quit':
            exit(0)

        return key

    def pick_remote(self, lcng):
        if self.verbose:
            self.ask_yes_no(f"Do I get options from {lcng.get_remote_url()}?", quit_if_no=True)
        else:
            self.ask_yes_no(f"Check {lcng.get_remote_url()}?", quit_if_no=True)

        rmt = self.get_remote_folders(lcng)

        # Cuantos remote folders tenemos?
        match len(rmt):
            # Si no hay ninguno, estamos jodidos
            case 0:
                cylon.cprint("[r|No cylons available]. Giving up.\n")
                exit(0)

            # Si hay un solo folder remoto, lo guardamos para preguntar si lo bajamos o no.
            case 1:
                self.ask_yes_no(f"Do I download {rmt[0]}?", quit_if_no=True)
                whichone = rmt[0]

            # Si hay más de uno, mostramos los que hay y preguntamos cuál se quiere bajar.
            case _:
                opt = self.ask_for_options(rmt, "Which one do I download?")
                whichone = rmt[opt]
        return whichone

    def get_remote_folders(self, lcng):
        out = False
        rmt = {}

        while not out:
            rmt = cylon.get_remote_folders(lcng.get('remote_server'), lcng.get('remote_path'))
            if not rmt:
                self.ask_yes_no("No answer. Should I try again?", quit_if_no=True)
            else:
                out = True

        return rmt

    def pick_target(self, lcng, whichone):
        # Preguntamos dónde tenemos que bajar el folder remoto
        ok = False
        target = ''

        while not ok:
            if self.verbose:
                target = input(f"Where should I download {whichone} to? (~/lib by default): ")
            else:
                target = input("Where to? (~/lib by default): ")

            if target == '':
                target = '~/lib'

            if os.path.exists(target):
                self.output(
                    f"{target} exists. Pick another.\n",
                    f"[r|{target} already exists]. I refuse to overwrite it. Pick another folder.\n"
                )
            else:
                ok = True
        return target

    def confirm_download(self, whichone, target):
        self.output(
            f"[y|{whichone}] -> [y|{target}]. ",
            f"I'll download [b|{whichone}] to [b|{target}]. "
        )
        self.ask_yes_no("Is that OK?", quit_if_no=True)

    def confirm_patching(self, folder):
        if self.verbose:
            self.ask_yes_no(f"Do I point the env var to {folder}?", default='y', quit_if_no=True)
        else:
            self.ask_yes_no(f"env var -> {folder}?", default='y', quit_if_no=True)
