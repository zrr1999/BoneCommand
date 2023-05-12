#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/13 22:03
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import os.path

import flet
from pdf2image.exceptions import PDFPageCountError

from bonecommand import all_commands
from bonecommand.utils import user_path
from bonecommand.pdf.utils import convert_pdf, split_pdf, merge_pdfs


def main(page: flet.Page):
    page.title = "My First Flet App"
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    thumbnails = flet.Row(
        [],
        alignment=flet.MainAxisAlignment.CENTER,
    )

    os.makedirs(f"{user_path}/bonecommand/generated", exist_ok=True)
    pdf_path = flet.TextField(
        label="PDF Path",
        value="",
    )
    output_folder = flet.TextField(
        label="Output folder",
        value=f"{user_path}/bonecommand/generated",
    )

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.add(
        pdf_path,
        output_folder,
        thumbnails,
        flet.TextButton("Split PDF", on_click=split_pdf),
    )
    page.views.append(
        flet.View(
            "/store",
            [
                flet.AppBar(
                    title=flet.Text("Store"), bgcolor=flet.colors.SURFACE_VARIANT
                ),
                flet.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
            ],
        )
    )
    page.go("/store")
    print([v.route for v in page.views])
    page.on_view_pop = view_pop


flet.app(target=main, assets_dir=f"{user_path}/bonecommand/assets")
