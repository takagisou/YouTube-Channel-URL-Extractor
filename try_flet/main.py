from faulthandler import disable
from turtle import onclick
import flet as ft
from yt_dlp import YoutubeDL
import time, pyperclip

def extract_channel_url(url: str) -> str:
    opts = {
        'playlist_items': '0',
        'quiet': True
    }

    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url = info['channel_url']
        return url


def main(page: ft.Page):

    def btn_cilck(e):
        txt_result.error_text = ""
        if not txt_url.value:
            txt_url.error_text = "Please enter youtube url"
            page.update()
        else:
            url = txt_url.value
            pr.visible = True
            page.update()
            try:
                channel_url = extract_channel_url(url)
                txt_result.value = channel_url
            except:
                txt_result.error_text = "extract failed"
            finally:
                pr.visible = False
                page.update()

    def paste_click(e):
        txt = pyperclip.paste()
        txt_url.value = txt
        page.update()

    def copy_click(e):
        txt = txt_result.value
        pyperclip.copy(txt)
        page.snack_bar = ft.SnackBar(ft.Text(f"Copied! {txt}"))
        page.snack_bar.open = True
        page.update()

    def clear_click(e):
        txt_url.value = ""
        txt_result.value = ""
        page.update()

    page.title = "YouTube Channel URL Extractor"

    btn_extract = ft.ElevatedButton("Extract Channel URL!", on_click=btn_cilck)
    btn_paste = ft.ElevatedButton("Paste", on_click=paste_click)
    btn_copy = ft.ElevatedButton("Copy", on_click=copy_click)
    btn_clear = ft.ElevatedButton("Clear", on_click=clear_click, color="red")
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
    txt_url = ft.TextField(label="URL", hint_text="https://www.youtube.com/@xxxxxxxx", width=600)
    txt_result = ft.TextField(label="Result", hint_text="https://www.youtube.com/channel/xxxxxxxx", width=600)


    page.add(
        ft.Row([txt_url, btn_paste], width=page.window_width),
        ft.Row([txt_result, btn_copy], width=page.window_width),
        ft.Divider(),
        ft.Row(
            [
                ft.Row([btn_extract, pr]),
                btn_clear
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

ft.app(target=main)