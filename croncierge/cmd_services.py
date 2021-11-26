import shlex
import subprocess
from datetime import datetime


def revise_cmd(cmd) -> list:
    if isinstance(cmd, str):
        return shlex.split(cmd)
    elif isinstance(cmd, list):
        return cmd
    else:
        err_msg = f"Command type must be str or list, no {type(cmd)}"
        TypeError(err_msg)

class CommandResponse():

    def __init__(self, stdout, stderr, status, started_at, exited_at):
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.status: int = status
        self.started_at: datetime = started_at
        self.exited_at: datetime = exited_at

    def __str__(self) -> str:
        return  "\n\n".join(
            f"{label}:\n{data}" for label, data in zip(
                ['status', 'stdout', 'stderr', 'started at', 'exited at'],
                [self.status, self.stdout, self.stderr, self.started_at, self.exited_at]
            ))


def run_cmd(cmd, timeout=None):
    cmd = revise_cmd(cmd)
    started_at = datetime.now()
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8')

    process.wait(timeout=timeout)
    exited_at = datetime.now()

    return CommandResponse(
        stdout=process.stdout.read(),
        stderr=process.stderr.read(),
        status=process.returncode,
        started_at=started_at,
        exited_at=exited_at,
    )
    
