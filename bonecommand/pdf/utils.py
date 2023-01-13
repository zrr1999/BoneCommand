#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/5 22:18
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from pypdf import PdfReader, PdfWriter, PdfMerger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath
    from typing import Sequence


def merge_pdfs(input_paths: Sequence[StrOrBytesPath], output_path: StrOrBytesPath):
    pdf_merger = PdfMerger()
    current_num_pages = 0
    for path in input_paths:
        pdf_reader = PdfReader(path)
        pdf_merger.merge(current_num_pages, pdf_reader)
        current_num_pages += len(pdf_reader.pages)
    # 把这个已合并了的PDF文档存储起来
    with open(output_path, "wb") as out:
        pdf_merger.write(out)


def split_pdf(file_name, start_page, end_page, output_pdf):
    input_file = PdfReader(open(file_name, "rb"))
    output_file = PdfWriter()
    for i in range(start_page, end_page):
        output_file.add_page(input_file.pages[i])
    with open(output_pdf, "wb") as f:
        output_file.write(f)
