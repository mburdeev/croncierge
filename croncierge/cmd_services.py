import subprocess
import shlex

def revise_cmd(cmd) -> list:
    if isinstance(cmd, str):
        return shlex.split(cmd)
    elif isinstance(cmd, list):
        return cmd
    else:
        err_msg = f"Command type must be str or list, no {type(cmd)}"
        TypeError(err_msg)

class CommandResponse():

    def __init__(self, stdout, stderr, status) -> None:
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.status: int = status

    def __str__(self) -> str:
        return  "\n\n".join(
            f"{label}:\n{data}" for label, data in zip(
                ['status', 'stdout', 'stderr'],
                [self.status, self.stdout, self.stderr]
            ))


def run_cmd(cmd, timeout=None):
    cmd = revise_cmd(cmd)
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8')

    process.wait(timeout=timeout)

    return CommandResponse(
        stdout=process.stdout.read(),
        stderr=process.stderr.read(),
        status=process.returncode
    )
    
