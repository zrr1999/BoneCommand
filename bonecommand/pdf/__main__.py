#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/5 22:02
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from utils import merge_pdfs, split_pdf
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def merge(input_paths: list[Path], output_path: Path):
    merge_pdfs(input_paths, output_path)


@app.command()
def split(file_name, start_page, end_page, output_pdf):
    split_pdf(file_name, start_page, end_page, output_pdf)


if __name__ == "__main__":
    app()
