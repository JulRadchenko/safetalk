import os
import requests
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDRoundFlatIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp, sp
from threading import Thread
from kivy.clock import Clock
from android.permissions import request_permissions, Permission
from plyer import audio
from plyer import filechooser
from android.storage import app_storage_path

Window.minimum_width = dp(360)
Window.minimum_height = dp(700)

API_URL = "https://voice-analyzer-api-tvaj.onrender.com"


class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__()
        self.current_audio = None
        self.is_recording = False
        self.is_playing = False
        self.audio = None
        self.temp_file = None

    def build(self):
        request_permissions([
            Permission.RECORD_AUDIO,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.INTERNET
        ])

        main_layout = BoxLayout(orientation='vertical', padding=dp(10))

        info_button_container = BoxLayout(orientation='horizontal', size_hint=(0.95, 0.05))

        info_button = MDRoundFlatIconButton(
            icon='help-circle',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(0.3, 0.6, 0.9, 1),
            text='Как использовать приложение?',
            text_color='white',
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1))
        info_button.bind(on_release=self.show_instructions)

        title = Label(
            text='[b]РЕЗУЛЬТАТ АНАЛИЗА[/b]',
            size_hint=(1, 0.1),
            font_size=sp(20),
            color='black',
            markup=True,
            padding=[dp(10), 0, dp(10), dp(10)],
            halign='center',
            valign='middle')

        result_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            size_hint=(0.95, 0.5),
            pos_hint={'center_x': 0.5}
        )

        self.progress = ProgressBar(max=100, value=0, size_hint=(0.95, 0.05), pos_hint={'center_x': 0.5})
        self.progress.opacity = 0

        text_container = FloatLayout(size_hint=(1, 0.5))

        self.result_text = Label(
            text='Ещё не было проанализировано ни одного аудиофайла.',
            font_size=sp(16),
            color='gray',
            halign='left',
            valign='top',
            size_hint=(1, None),
            text_size=(None, None),
            pos_hint={'x': 0, 'top': 1})

        clean_button_container = BoxLayout(orientation='vertical', size_hint=(0.95, 0.05))

        self.clean_button = MDRoundFlatIconButton(
            icon='delete',
            size_hint=(0.8, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(0.3, 0.6, 0.9, 1),
            line_color=(1, 1, 1, 0),
            text='Очистить',
            text_color='white',
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            disabled=True)
        self.clean_button.bind(on_press=self.clean_result)

        space = BoxLayout(orientation='vertical', size_hint=(0.95, 0.015), pos_hint={'center_x': 0.5})

        file_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            size_hint=(0.95, 0.1),
            pos_hint={'center_x': 0.5}
        )

        file_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )

        file_text = Label(text='Имя файла:', font_size=sp(16), color='black', size_hint=(0.3, 1))  # ИЗМЕНЕНО на sp

        self.file_name = Label(text='файл не выбран', font_size=sp(16), color='gray',
                               size_hint=(0.7, 1))  # ИЗМЕНЕНО на sp

        self.button_play = MDIconButton(
            icon='play',
            size_hint=(0.18, 1),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size=sp(30),
            pos_hint={'center_y': 0.4},
            disabled=True)
        self.button_play.bind(on_press=self.play_file)

        buttons_container = BoxLayout(
            orientation='horizontal',
            size_hint=(0.95, 0.3),
            spacing=dp(20)
        )

        button_attach = MDIconButton(
            icon='attachment',
            size_hint=(0.2, 0.33),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size=sp(40),
            pos_hint={'center_y': 0.5})
        button_attach.bind(on_release=self.attach_file)

        self.button_start = MDIconButton(
            icon='rocket-launch',
            size_hint=(0.4, 0.64),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size=sp(90),
            pos_hint={'center_y': 0.5},
            disabled=True)
        self.button_start.bind(on_release=self.start_analysis)

        button_mic = MDIconButton(
            icon='microphone',
            size_hint=(0.2, 0.33),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size=sp(40),
            pos_hint={'center_y': 0.5})
        button_mic.bind(on_release=self.record_audio)

        buttons_layout = BoxLayout(orientation='vertical', size_hint=(0.95, 0.3), pos_hint={'center_x': 0.5})

        with main_layout.canvas.before:
            Color(0.875, 0.918, 0.957, 1)
            self.main_bg = RoundedRectangle(size=main_layout.size, pos=main_layout.pos, radius=[0])
            Color(1, 1, 1, 1)
            self.result_bg = RoundedRectangle(size=result_layout.size, pos=result_layout.pos,
                                              radius=[dp(50)])  # ИЗМЕНЕНО на dp
            Color(0.875, 0.918, 0.957, 1)
            self.space_bg = RoundedRectangle(size=space.size, pos=space.pos, radius=[dp(50)])  # ИЗМЕНЕНО на dp
            Color(1, 1, 1, 1)
            self.file_bg = RoundedRectangle(size=file_layout.size, pos=file_layout.pos,
                                            radius=[dp(40)])  # ИЗМЕНЕНО на dp

        main_layout.bind(size=self.adapt_main, pos=self.adapt_main)
        result_layout.bind(size=self.adapt_result, pos=self.adapt_result)
        file_layout.bind(size=self.adapt_file, pos=self.adapt_file)
        space.bind(size=self.adapt_space, pos=self.adapt_space)
        self.result_text.bind(
            size=self.adapt_result_text,
            texture_size=lambda inst, val: setattr(inst, 'height', val[1] + dp(50))  # ИЗМЕНЕНО на dp
        )

        info_button_container.add_widget(info_button)
        text_container.add_widget(self.result_text)
        result_layout.add_widget(text_container)
        result_layout.add_widget(clean_button_container)

        file_row.add_widget(file_text)
        file_row.add_widget(self.file_name)
        file_row.add_widget(self.button_play)
        file_layout.add_widget(file_row)

        clean_button_container.add_widget(self.clean_button)

        buttons_container.add_widget(button_attach)
        buttons_container.add_widget(self.button_start)
        buttons_container.add_widget(button_mic)
        buttons_layout.add_widget(buttons_container)

        main_layout.add_widget(info_button_container)
        main_layout.add_widget(title)
        main_layout.add_widget(result_layout)
        main_layout.add_widget(space)
        main_layout.add_widget(file_layout)
        main_layout.add_widget(self.progress)
        main_layout.add_widget(buttons_layout)

        return main_layout

    def show_instructions(self, instance):
        self.result_text.text = """[size=16][b]КАК ИСПОЛЬЗОВАТЬ ПРИЛОЖЕНИЕ[/b][/size]
[size=14][b]1. Выбор аудиофайла[/b][/size]
Нажмите кнопку 📎 (скрепка), чтобы выбрать аудиофайл в формате WAV из памяти телефона.
[size=14][b]2. Запись с микрофона[/b][/size]
Нажмите кнопку 🎤 (микрофон) для начала записи. Для остановки записи нажмите кнопку ещё раз.
[size=14][b]3. Прослушивание[/b][/size]
После выбора или записи файла станет активна кнопка ▶ (play). Используйте её для предварительного прослушивания.
[size=14][b]4. Запуск анализа[/b][/size]
Нажмите большую кнопку 🚀 (ракета) для отправки аудио на анализ. Подождите 15-30 секунд.
[size=14][b]5. Результаты[/b][/size]"""
        self.clean_button.disabled = False
        self.result_text.markup = True

    def adapt_main(self, instance, value):
        self.main_bg.size = instance.size
        self.main_bg.pos = instance.pos

    def adapt_result(self, instance, value):
        self.result_bg.size = instance.size
        self.result_bg.pos = instance.pos

    def adapt_result_text(self, instance, value):
        instance.text_size = (instance.width, None)

    def adapt_file(self, instance, value):
        self.file_bg.size = instance.size
        self.file_bg.pos = instance.pos

    def adapt_space(self, instance, value):
        self.space_bg.size = instance.size
        self.space_bg.pos = instance.pos

    def clean_result(self, instance):
        self.result_text.text = 'Ещё не было проанализировано ни одного аудиофайла.'
        self.clean_button.disabled = True

    def attach_file(self, instance):
        filechooser.open_file(on_selection=self.show_file_name, filters=["*.wav"])

    def show_file_name(self, selection):
        if selection:
            self.current_audio = selection[0]
            self.audio = None
            self.is_playing = False
            file_basename = os.path.basename(selection[0])

            if Window.size < (420, 920) and len(file_basename) > 10:
                name_without_ext = os.path.splitext(file_basename)[0]
                extension = os.path.splitext(file_basename)[1]
                short_name = name_without_ext[:15] + '...' + extension
                file_basename = short_name

            self.file_name.text = file_basename
            self.file_name.color = 'blue'
            self.button_start.disabled = False
            self.button_play.disabled = False

    def play_file(self, instance):
        if not self.current_audio:
            return
        if not hasattr(self, 'audio') or self.audio is None:
            self.audio = SoundLoader.load(self.current_audio)
            if self.audio:
                self.audio.play()
                self.is_playing = True
                instance.icon = 'pause'
        else:
            if self.is_playing:
                self.audio.stop()
                self.is_playing = False
                instance.icon = 'play'
            else:
                self.audio.play()
                self.is_playing = True
                instance.icon = 'pause'

    def record_audio(self, instance):
        if not hasattr(self, 'is_recording') or not self.is_recording:
            self.is_recording = True
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.temp_file = os.path.join(
                app_storage_path(),
                f'recording_{timestamp}.wav'
            )
            audio.start_recording(self.temp_file)
            instance.icon = 'stop'
        else:
            audio.stop_recording()
            self.is_recording = False
            self.current_audio = self.temp_file.name
            self.file_name.text = os.path.basename(self.temp_file.name)
            self.file_name.color = 'blue'
            instance.icon = 'microphone'
            self.button_start.disabled = False
            self.button_play.disabled = False

    def start_analysis(self, instance):
        if not self.current_audio:
            return
        self.button_start.disabled = True
        self.progress.opacity = 1
        self.progress.value = 10
        self.result_text.text = "Анализ аудиофайла...\n\nПодождите, это может занять до 30 секунд."

        def analyze_async():
            try:
                with open(self.current_audio, 'rb') as f:
                    Clock.schedule_once(lambda dt: setattr(self.progress, 'value', 30))
                    response = requests.post(
                        f'{API_URL}/analyze',
                        files={'file': (os.path.basename(self.current_audio), f, 'audio/wav')},
                        timeout=60
                    )
                    Clock.schedule_once(lambda dt: setattr(self.progress, 'value', 80))
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            Clock.schedule_once(lambda dt: self.analysis_complete(data['result_content'], True))
                        else:
                            Clock.schedule_once(
                                lambda dt: self.analysis_complete(f"Ошибка: {data.get('error', 'Неизвестная ошибка')}",
                                                                  False))
                    else:
                        Clock.schedule_once(
                            lambda dt: self.analysis_complete(f"Ошибка сервера: {response.status_code}", False))
            except requests.exceptions.Timeout:
                Clock.schedule_once(
                    lambda dt: self.analysis_complete("Ошибка: Превышено время ожидания ответа от сервера", False))
            except requests.exceptions.ConnectionError:
                Clock.schedule_once(
                    lambda dt: self.analysis_complete("Ошибка: Не удалось подключиться к серверу. Проверьте интернет.",
                                                      False))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.analysis_complete(f"Ошибка: {str(e)}", False))

        Thread(target=analyze_async).start()

    def analysis_complete(self, result_content, success):
        self.result_text.text = result_content
        self.result_text.markup = True
        self.clean_button.disabled = False
        self.button_start.disabled = False
        self.progress.opacity = 0
        self.progress.value = 0


if __name__ == '__main__':
    Main().run()
    
