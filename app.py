
import flet as ft
import elevenlabs
import config
import os
from uuid import uuid4


API_KEY = config.API_KEY
 
elevenlabs.set_api_key(API_KEY)



class TtsAPP(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.text_box = ft.TextField(
            multiline = True,
            min_lines = 20,
            expand = True,
            width = 700,
            height = 300
        )

        self.audio = None
        self.audio_task = None
        self.voices_list = elevenlabs.voices()


        self.play_bt = ft.IconButton(
            icon = ft.icons.PLAY_CIRCLE,
            on_click= self.play
        )

        self.save_bt = ft.IconButton(
            icon = ft.icons.SAVE,
            on_click = self.save_audio
        )

        self.voices = ft.Dropdown(
            width = 200,
            options = [ft.dropdown.Option(v.name) for v in self.voices_list]
        )

        # set default voice
        self.voices.value = self.voices_list[-1].name



    def save_audio(self, e):
        if self.audio:
            if not os.path.exists('out'):
                os.mkdir('out')

            file_id = str(uuid4())
            elevenlabs.save(self.audio, filename = f'out/{file_id}.mp3')
    

    def play_audio(self):
        elevenlabs.play(self.audio)
        

    def play(self, e):
        text = self.text_box.value
        if len(text) > 0 and not text.isspace():
            
            self.play_bt.icon = ft.icons.STOP_CIRCLE
            self.play_bt.update()

            self.audio = elevenlabs.generate(text, voice = self.voices.value)
            self.play_audio()
           


            self.play_bt.icon = ft.icons.PLAY_CIRCLE
            self.play_bt.update()

            
                
            
        self.page.update()
        
    
    def build(self):
        return ft.Column([
            ft.Row([self.text_box]),
            ft.Row([self.voices]),
            ft.Row([self.play_bt, self.save_bt])
        ])


def main(page : ft.Page):
    page.window_height = 500
    page.window_width = 700

    page.add(TtsAPP())
    page.update()


ft.app(target = main)