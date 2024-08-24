import re
import subprocess

class process:
    command = None
    returncode = None
    stdout = None
    stderr = None

    def __str__(self) -> str:
        if not self.command:
            return "<Empty tools.run.run object>"
        else:
            out = f"({self.command})->{self.returncode}\n"
            if self.stdout:
                out += ''.join(map(lambda x: 'O: '+x+'\n', self.stdout))
            if self.stderr:
                out += ''.join(map(lambda x: 'E: '+x+'\n', self.stderr))
            return out

    def reset(self) -> None:
        self.command = None
        self.returncode = None
        self.stdout = None
        self.stderr = None

    def run(self, comm:str, fail_if_not_ok:bool = False) -> None:
        cp = subprocess.run(comm.split(" "), capture_output=True, text=True)
        self.command = comm
        self.returncode = cp.returncode
        if cp.stdout != '':
            self.stdout = cp.stdout.rstrip(" \n").split("\n")
        if cp.stderr != '':
            self.stderr = cp.stderr.rstrip(" \n").split("\n")
        if fail_if_not_ok and not self.is_ok():
            print(self)
            exit(1)

    def is_ok(self) -> bool:
        return self.returncode==0

    def is_there_stdout(self) -> bool:
        return self.stdout and len(self.stdout)>0

    def is_there_stderr(self) -> bool:
        return self.stderr and len(self.stderr)>0

    def search(self, pat:str, stdout:bool = True) -> list:
        wheretolook = self.stdout if stdout else self.stderr
        if not wheretolook:
            return None

        mtch = re.compile(pat)
        lst = []
        for line in wheretolook:
            ret = mtch.search(line)
            if ret:
                lst.append(list(ret.groups()))

        return lst
