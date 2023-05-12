#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/5 22:18
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from pypdf import PdfReader, PdfWriter, PdfMerger
from typing import TYPE_CHECKING
from pdf2image import convert_from_path, convert_from_bytes
from io import BytesIO
import base64

if TYPE_CHECKING:
    from typing import Sequence
    from pathlib import Path


def merge_pdfs(input_paths: Sequence[Path | str], output_path: Path | str):
    pdf_merger = PdfMerger()
    current_num_pages = 0
    for path in input_paths:
        pdf_reader = PdfReader(path)
        pdf_merger.merge(current_num_pages, pdf_reader)
        current_num_pages += len(pdf_reader.pages)
    # 把这个已合并了的PDF文档存储起来
    with open(output_path, "wb") as out:
        pdf_merger.write(out)


def split_pdf(
    input_path: Path | str, first_page: int, last_page: int, output_path: Path | str
):
    input_file = PdfReader(open(input_path, "rb"))
    output_file = PdfWriter()
    for i in range(first_page, last_page):
        output_file.add_page(input_file.pages[i])
    with open(output_path, "wb") as f:
        output_file.write(f)


def convert_pdf(
    input_path: Path | str,
    dpi: int = 200,
    output_folder: Path | str = None,
    output_list: list[str] = None,
    first_page: int = None,
    last_page: int = None,
    fmt: str = "ppm",
):
    outputs = convert_from_path(
        input_path, dpi, output_folder, first_page, last_page, fmt
    )
    if output_list is not None:
        buff = BytesIO()
        output_list.extend(
            [
                output.save(buff, format="PNG")
                or base64.b64encode(buff.getvalue()).decode()
                for output in outputs
            ]
        )
