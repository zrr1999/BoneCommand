#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/1 12:09
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from typing import TYPE_CHECKING
from subprocess import Popen, PIPE, run
import shlex

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath
    from typing import Sequence, Union

    CMD = Union[StrOrBytesPath, Sequence[StrOrBytesPath]]


class CommandBase:
    def __init__(self, popens: Sequence[Popen], timeout: float | None = None):
        self.popens = popens
        self.timeout = timeout

    def run(self):
        for p in self.popens:
            with p:
                try:
                    return p.wait(timeout=self.timeout)
                except:  # Including KeyboardInterrupt, wait handled that.
                    p.kill()
                    # We don't call p.wait() again as p.__exit__ does that for us.
                    raise


class SingleCommand(CommandBase):
    def __init__(self, cmd: CMD, working_path: StrOrBytesPath | None = None,
                 timeout: float | None = None, **kwargs):
        if isinstance(cmd, str):
            self.cmd = shlex.split(cmd)
        else:
            self.cmd = cmd
        if kwargs.get('stdin') is None:
            kwargs['stdin'] = PIPE
        if working_path is not None:
            if kwargs.get('cwd') is not None:
                raise ValueError('cwd and working_path arguments may not both be used.')
            kwargs['cwd'] = working_path
        self.kwargs = kwargs
        super().__init__([
            Popen(self.cmd, **self.kwargs)
        ], timeout)


class MultiCommand(CommandBase):
    def __init__(self, cmds: Sequence[CMD], working_path: StrOrBytesPath | None = None,
                 timeout: float | None = None, **kwargs):
        if kwargs.get('stdin') is None:
            kwargs['stdin'] = PIPE
        if working_path is not None:
            if kwargs.get('cwd') is not None:
                raise ValueError('cwd and working_path arguments may not both be used.')
            kwargs['cwd'] = working_path
        popens = []
        for cmd in cmds:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            popens.append(Popen(cmd, **kwargs))
        super().__init__(popens, timeout)


class ShellCommand(CommandBase):
    def __init__(self, cmds: Sequence[str], working_path: StrOrBytesPath | None = None,
                 timeout: float | None = None, **kwargs):
        if kwargs.get('stdin') is None:
            kwargs['stdin'] = PIPE
        if working_path is not None:
            if kwargs.get('cwd') is not None:
                raise ValueError('cwd and working_path arguments may not both be used.')
            kwargs['cwd'] = working_path
        super().__init__([Popen("\n".join(cmds), shell=True, **kwargs)], timeout)

