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


class Status(BaseModel):
    finished: bool = False
    returncode: Optional[int] = None
    stdout: Optional[str] = None


class CommandBase:
    def __init__(self, popens: Sequence[Popen], timeout: float | None = None):
        self.popens = popens
        self.timeout = timeout
        self.popens_status: list[Status] = [Status() for _ in popens]

    def run(self) -> list[Status]:
        for p, s in zip(self.popens, self.popens_status):
            if not s.finished:
                s.finished = True
                with p:
                    s.returncode = p.wait(timeout=self.timeout)
                    s.stdout = p.stdout.read().decode()
        return self.popens_status


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
        super().__init__([Popen(self.cmd, **self.kwargs)], timeout)

    def get_code(self) -> int:
        return self.run()[0].returncode

    def get_output(self) -> str:
        return self.run()[0].stdout


class MultiCommand(CommandBase):
    def __init__(
        self,
        cmds: Sequence[CMD],
        working_path: StrOrBytesPath | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        if working_path is not None:
            if kwargs.get("cwd") is not None:
                raise ValueError("cwd and working_path arguments may not both be used.")
            kwargs["cwd"] = working_path
        kwargs = gen_default_kwargs(kwargs)
        popens = []
        for cmd in cmds:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            popens.append(Popen(cmd, **kwargs))
        super().__init__(popens, timeout)

    def get_codes(self) -> list[int]:
        codes = []
        for s in self.popens_status:
            codes.append(s.returncode)
        return codes

    def get_outputs(self) -> list[str]:
        outputs = []
        for s in self.popens_status:
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
        kwargs = gen_default_kwargs(kwargs)
        super().__init__([Popen("\n".join(cmds), shell=True, **kwargs)], timeout)

    def get_code(self) -> int:
        return self.run()[0].returncode

    def get_output(self) -> str:
        return self.run()[0].stdout
