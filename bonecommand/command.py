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
    from typing import Sequence, Union, Any, Optional

    CMD = Union[StrOrBytesPath, Sequence[StrOrBytesPath]]


def gen_default_kwargs(kwargs: dict[str, Any]):
    if kwargs.get("stdin") is None:
        kwargs["stdin"] = PIPE
    if kwargs.get("stderr") is None:
        kwargs["stderr"] = PIPE
    if kwargs.get("stdout") is None:
        kwargs["stdout"] = PIPE
    return kwargs


class SubprocessError(Exception):
    def __init__(self, return_code):
        self.return_code = return_code
        super().__init__(f"Subprocess returned non-zero exit status {return_code}")


class Status(BaseModel):
    finished: bool = False
    returncode: Optional[int] = None
    stdout: Optional[str] = None


class CommandBase:
    def __init__(self, timeout: float | None = None):
        self.timeout = timeout
        self.popens: list[Popen] = []
        self.status: list[Status] = []

    def create_popens(self):
        raise NotImplementedError

    def run(self) -> list[Status]:
        self.create_popens()
        for p, s in zip(self.popens, self.status):
            if not s.finished:
                s.finished = True
                with p:
                    s.returncode = p.wait(timeout=self.timeout)
                    if p.stdout is not None:
                        s.stdout = p.stdout.read().decode()
        return self.status

    def finished(self) -> bool:
        for s in self.status:
            if not s.finished:
                return False
        return True

    def get_code(self) -> int | None:
        for code in self.get_codes():
            if code != 0:
                return code
        return 0

    def get_output(self) -> str | None:
        raise NotImplementedError

    def get_codes(self) -> list[int | None]:
        codes = []
        for s in self.status:
            codes.append(s.returncode)
        return codes

    def get_outputs(self) -> list[str | None]:
        outputs = []
        for s in self.status:
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

    def create_popens(self):
        self.popens = [Popen(self.cmd, shell=True, **self.kwargs)]
        self.status = [Status()]

    def get_code(self) -> int | None:
        return self.status[0].returncode

    def get_output(self) -> str | None:
        return self.status[0].stdout


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

    def create_popens(self):
        self.popens = [Popen(self.cmd, **self.kwargs)]
        self.status = [Status()]

    def get_code(self) -> int | None:
        return self.status[0].returncode

    def get_output(self) -> str | None:
        return self.status[0].stdout


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

    def create_popens(self) -> Sequence[Popen]:
        popens = []
        for cmd in self.cmds:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            popens.append(Popen(cmd, **self.kwargs))
        return popens


class SequenceCommand(CommandBase):
    def __init__(
        self,
        cmds: Sequence[CMD],
        working_path: StrOrBytesPath | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        pass


class PipelineCommand(CommandBase):
    def __init__(
        self,
        cmds: Sequence[CMD],
        working_path: StrOrBytesPath | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        pass
