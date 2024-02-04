
import flet as ft
import elevenlabs
import config
import os
import webbrowser
from uuid import uuid4
import requests


API_KEY : str = config.API_KEY


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
        self.info = self.get_subscription_info()
        self.tier = self.info['tier']
        self.character_count = self.info['character_count']
        self.character_limit = self.info['character_limit']


        self.powered_by = ft.Text(
            value = 'powered by Elevenlabs API'
        )

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

        self.label_1 = ft.Text(
            value = '',
            weight=900
        )

        
        

        self.use_info = ft.Text(
            value = f'{self.character_count} out of {self.character_limit} used'
        )

        self.upgrade_bt = ft.TextButton(
            text = 'Upgrade Plan',
            on_click = self.Upgrade_Plan
        )


        if self.tier == 'free':
            self.label_1.value = 'Free Characters'
        else:
            self.label_1.value = 'Subscriber'

    



    def Upgrade_Plan(self, e):
        webbrowser.open('https://elevenlabs.io/subscription')
    
    
  
    # Get user subscription info
    def get_subscription_info(self):
        url = "https://api.elevenlabs.io/v1/user/subscription"

        headers = {"xi-api-key": API_KEY}

        response = requests.request("GET", url, headers=headers)
        return response.json()
        



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

            self.audio = elevenlabs.generate(
                text, 
                voice = self.voices.value,
                model="eleven_multilingual_v2"
            )

            self.play_audio()


            self.info = self.get_subscription_info()
            self.character_count = self.info['character_count']
            self.character_limit = self.info['character_limit']


            self.use_info.value = f'{self.character_count} out of {self.character_limit} used'
            self.use_info.update()


            self.play_bt.icon = ft.icons.PLAY_CIRCLE
            self.play_bt.update()


            
                
            
        self.page.update()
        
    
    def build(self):
        return ft.Column([

            ft.Row([self.powered_by]),

            ft.Row([self.label_1, self.use_info, self.upgrade_bt], 
                alignment = ft.MainAxisAlignment.START
            ),

            ft.Row([self.text_box]),
            ft.Row([self.voices]),
            ft.Row([self.play_bt, self.save_bt])
        ])


def main(page : ft.Page):
    page.window_height = 540
    page.window_width = 700

    page.add(TtsAPP())
    page.update()



    
if (API_KEY.isalpha() or API_KEY.isalnum()):
    elevenlabs.set_api_key(API_KEY)
    ft.app(target = main)
else:
    webbrowser.open('http://elevenlabs.io/?from=partnersmith9278')
    exit(0)
