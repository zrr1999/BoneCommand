#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/5 22:02
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from bonecommand.pdf.utils import merge_pdfs, split_pdf
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def merge(input_paths: list[Path], output_folder: Path):
    merge_pdfs(input_paths, output_folder)


@app.command()
def split(input_path: Path, first_page: int, last_page: int, output_path: Path):
    split_pdf(input_path, first_page, last_page, output_path)


@app.command()
def convert(
    input_path: Path,
    dpi: int = 200,
    output_folder: Path = None,
    output_list: list[str] = None,
    first_page: int = None,
    last_page: int = None,
    fmt: str = "ppm",
):
    raise NotImplementedError


if __name__ == "__main__":
    app()
