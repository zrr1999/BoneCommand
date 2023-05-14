#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/1 12:09
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from typing import TYPE_CHECKING
from subprocess import Popen, PIPE
from pydantic import BaseModel
import shlex

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath
    from typing import Sequence, Union, Any, Optional, Iterable

    CMD = Union[StrOrBytesPath, Sequence[StrOrBytesPath]]


def gen_default_kwargs(kwargs: dict[str, Any]):
    if kwargs.get("stdin") is None:
        kwargs["stdin"] = PIPE
    if kwargs.get("stderr") is None:
        kwargs["stderr"] = PIPE
    if kwargs.get("stdout") is None:
        kwargs["stdout"] = PIPE
    return kwargs


def wait_popen(popen: Popen, status: Status, timeout: float | None = None):
    with popen:
        status.returncode = popen.wait(timeout=timeout)
        status.finished = True
        if popen.stdout is not None:
            status.stdout = popen.stdout.read()
        if isinstance(status.stdout, bytes):
            status.stdout = status.stdout.decode()


class SubprocessError(Exception):
    def __init__(self, return_code):
        self.return_code = return_code
        super().__init__(f"Subprocess returned non-zero exit status {return_code}")


class Status(BaseModel):
    popen: Popen
    finished: bool = False
    returncode: Optional[int] = None
    stdout: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class CommandBase:
    def __init__(self, timeout: float | None = None):
        self.timeout = timeout
        self.statuses: list[Status] = []

    def run(self) -> list[Status] | Status:
        raise NotImplementedError()

    async def async_run(self) -> list[Status] | Status:
        return self.run()

    def finished(self) -> bool:
        for s in self.statuses:
            if not s.finished:
                return False
        return True

    def get_code(self) -> int | None:
        for code in self.get_codes():
            if code != 0:
                return code
        return 0

    def get_output(self) -> str | None:
        return str(self.get_outputs())

    def get_codes(self) -> list[int | None]:
        codes = []
        for s in self.statuses:
            codes.append(s.returncode)
        return codes

    def get_outputs(self) -> list[str | None]:
        outputs = []
        for s in self.statuses:
            outputs.append(s.stdout)
        return outputs


class ShellCommand(CommandBase):
    def __init__(
        self,
        cmds: Sequence[str],
        working_path: StrOrBytesPath | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        if working_path is not None:
            if kwargs.get("cwd") is not None:
                raise ValueError("cwd and working_path arguments may not both be used.")
            kwargs["cwd"] = working_path
        self.cmd = "\n".join(cmds)
        self.kwargs = gen_default_kwargs(kwargs)
        super().__init__(timeout)

    def run(self) -> Status:
        popen = Popen(self.cmd, shell=True, **self.kwargs)
        status = Status(popen=popen)
        wait_popen(popen, status, self.timeout)
        self.statuses.append(status)
        return status

    def get_code(self) -> int | None:
        return self.statuses[0].returncode

    def get_output(self) -> str | None:
        return self.statuses[0].stdout


class SingleCommand(CommandBase):
    def __init__(
        self,
        cmd: CMD,
        working_path: StrOrBytesPath | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        if isinstance(cmd, str):
            self.cmd = shlex.split(cmd)
        else:
            self.cmd = cmd
        if working_path is not None:
            if kwargs.get("cwd") is not None:
                raise ValueError("cwd and working_path arguments may not both be used.")
            kwargs["cwd"] = working_path
        kwargs = gen_default_kwargs(kwargs)
        self.kwargs = kwargs
        super().__init__(timeout)

    def run(self) -> Status:
        popen = Popen(self.cmd, **self.kwargs)
        status = Status(popen=popen)
        wait_popen(popen, status, self.timeout)
        self.statuses.append(status)
        return status

    def get_code(self) -> int | None:
        return self.statuses[0].returncode

    def get_output(self) -> str | None:
        return self.statuses[0].stdout


class MultiCommand(CommandBase):
    def __init__(
        self,
        cmds: Sequence[CMD],
        working_path: StrOrBytesPath | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        self.cmds = cmds
        if working_path is not None:
            if kwargs.get("cwd") is not None:
                raise ValueError("cwd and working_path arguments may not both be used.")
            kwargs["cwd"] = working_path
        kwargs = gen_default_kwargs(kwargs)
        self.kwargs = kwargs
        super().__init__(timeout)

    def run(self) -> list[Status]:
        for cmd in self.cmds:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            popen = Popen(cmd, **self.kwargs)
            status = Status(popen=popen)
            self.statuses.append(status)
        for status in self.statuses:
            popen = status.popen
            wait_popen(popen, status, self.timeout)
        return self.statuses


class SequenceCommand(MultiCommand):
    def run(self) -> list[Status]:
        for cmd in self.cmds:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            popen = Popen(cmd, **self.kwargs)
            status = Status(popen=popen)
            self.statuses.append(status)
            popen = status.popen
            wait_popen(popen, status, self.timeout)
        return self.statuses


class ParallelCommand(MultiCommand):
    pass
