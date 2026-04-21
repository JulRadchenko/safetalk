import os
import tempfile
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
from threading import Thread
from kivy.clock import Clock
from android.permissions import request_permissions, Permission
from plyer import audio
from plyer import filechooser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout

API_URL = "https://voice-analyzer-api.onrender.com"

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

        main_layout = BoxLayout(orientation='vertical', padding=10)

        info_button_container = BoxLayout(orientation='horizontal', size_hint=(0.95, 0.05))

        info_button = MDRoundFlatIconButton(
            icon='help-circle',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(0.3, 0.6, 0.9, 1),
            text='Как использовать приложение?',
            text_color='white',
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1))

        title = Label(
            text='[b]РЕЗУЛЬТАТ АНАЛИЗА[/b]',
            size_hint=(1, 0.1),
            font_size='20sp',
            color='black',
            markup=True,
            padding=[10, 0, 10, 10],
            halign='center',
            valign='middle')

        result_layout = BoxLayout(orientation='vertical', padding=20, size_hint=(0.95, 0.5), pos_hint={'center_x': 0.5})

        self.progress = ProgressBar(max=100, value=0, size_hint=(0.95, 0.05), pos_hint={'center_x': 0.5})
        self.progress.opacity = 0

        text_container = FloatLayout(size_hint=(1, 0.5))

        self.result_text = Label(
            text='Ещё не было проанализировано ни одного аудиофайла.',
            font_size='16sp',
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

        space = BoxLayout(orientation='vertical', size_hint=(0.95, 0.015), pos_hint={'center_x': 0.5})

        file_layout = BoxLayout(orientation='vertical', padding=20, size_hint=(0.95, 0.1), pos_hint={'center_x': 0.5})

        file_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)

        file_text = Label(text='Имя файла:', font_size='16sp', color='black', size_hint=(0.3, 1))

        self.file_name = Label(text='файл не выбран', font_size='16sp', color='gray', size_hint=(0.7, 1))

        self.button_play = MDIconButton(
            icon='play',
            size_hint=(0.18, 1),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size='30sp',
            pos_hint={'center_y': 0.4},
            disabled=True)

        buttons_container = BoxLayout(orientation='horizontal', size_hint=(0.95, 0.3), spacing=20)

        button_attach = MDIconButton(
            icon='attachment',
            size_hint=(0.2, 0.33),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size='40sp',
            pos_hint={'center_y': 0.5})

        self.button_start = MDIconButton(
            icon='rocket-launch',
            size_hint=(0.4, 0.64),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size='90sp',
            pos_hint={'center_y': 0.5},
            disabled=True)

        button_mic = MDIconButton(
            icon='microphone',
            size_hint=(0.2, 0.33),
            md_bg_color=(0.3, 0.6, 0.9, 1),
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            icon_size='40sp',
            pos_hint={'center_y': 0.5})

        buttons_layout = BoxLayout(orientation='vertical', size_hint=(0.95, 0.3), pos_hint={'center_x': 0.5})

        with main_layout.canvas.before:
            Color(0.875, 0.918, 0.957, 1)
            self.main_bg = RoundedRectangle(size=main_layout.size, pos=main_layout.pos, radius=[0])
            Color(1, 1, 1, 1)
            self.result_bg = RoundedRectangle(size=result_layout.size, pos=result_layout.pos, radius=[50])
            Color(0.875, 0.918, 0.957, 1)
            self.space_bg = RoundedRectangle(size=space.size, pos=space.pos, radius=[50])
            Color(1, 1, 1, 1)
            self.file_bg = RoundedRectangle(size=file_layout.size, pos=file_layout.pos, radius=[40])

        main_layout.bind(size=self.adapt_main, pos=self.adapt_main)
        result_layout.bind(size=self.adapt_result, pos=self.adapt_result)
        file_layout.bind(size=self.adapt_file, pos=self.adapt_file)
        space.bind(size=self.adapt_space, pos=self.adapt_space)
        self.result_text.bind(size=self.adapt_result_text, texture_size=lambda inst, val: setattr(inst, 'height', val[1] + 50))
        info_button.bind(on_release=self.show_instructions)

        info_button_container.add_widget(info_button)
        text_container.add_widget(self.result_text)
        result_layout.add_widget(text_container)
        result_layout.add_widget(clean_button_container)

        file_row.add_widget(file_text)
        file_row.add_widget(self.file_name)
        file_row.add_widget(self.button_play)
        file_layout.add_widget(file_row)
        self.button_play.bind(on_press=self.play_file)

        clean_button_container.add_widget(self.clean_button)
        self.clean_button.bind(on_press=self.clean_result)

        buttons_container.add_widget(button_attach)
        buttons_container.add_widget(self.button_start)
        buttons_container.add_widget(button_mic)
        buttons_layout.add_widget(buttons_container)
        button_attach.bind(on_release=self.attach_file)
        button_mic.bind(on_release=self.record_audio)
        self.button_start.bind(on_release=self.start_analysis)

        main_layout.add_widget(info_button_container)
        main_layout.add_widget(title)
        main_layout.add_widget(result_layout)
        main_layout.add_widget(space)
        main_layout.add_widget(file_layout)
        main_layout.add_widget(self.progress)
        main_layout.add_widget(buttons_layout)

        return main_layout

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

    def show_instructions(self, instance):

        content = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint_y=None,
            height=500
        )

        title_label = Label(
            text='[b]КАК ИСПОЛЬЗОВАТЬ ПРИЛОЖЕНИЕ[/b]',
            font_size='20sp',
            color=(0.3, 0.6, 0.9, 1),
            markup=True,
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle'
        )
        content.add_widget(title_label)

        instruction_text = """
[size=16][b]1. Выбор аудиофайла[/b][/size]
[color=333333]Нажмите кнопку [b]📎[/b] (скрепка), чтобы выбрать готовый аудиофайл в формате WAV из памяти телефона.
[/color]
[size=16][b]2. Запись с микрофона[/b][/size]
[color=333333]Нажмите кнопку [b]🎤[/b] (микрофон) для начала записи. Для остановки записи нажмите кнопку [b]⏹[/b] (стоп).
[/color]
[size=16][b]3. Прослушивание[/b][/size]
[color=333333]После выбора или записи файла станет активна кнопка [b]▶[/b] (play). Используйте её для прослушивания.
[/color]
[size=16][b]4. Запуск анализа[/b][/size]
[color=333333]Нажмите большую кнопку [b]🚀[/b] (ракета) для отправки аудио на анализ. Подождите 15-30 секунд.[/color]
[size=16][b]5. Результаты[/b][/size]
[color=333333]Система покажет уровень риска (НИЗКИЙ/СРЕДНИЙ/ВЫСОКИЙ) и даст рекомендации. [/color]
[size=14][color=008000][b]Совет:[/b][/color] Для точного анализа записывайте фрагменты длительностью не менее 10 секунд в тихой обстановке.[/size]
    """

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=4,
            bar_color=(0.3, 0.6, 0.9, 1),
            bar_inactive_color=(0.7, 0.7, 0.7, 1)
        )

        text_label = Label(
            text=instruction_text,
            font_size='14sp',
            color=(0.2, 0.2, 0.2, 1),
            markup=True,
            size_hint_y=None,
            text_size=(350, None),
            halign='left',
            valign='top',
            padding=[5, 5]
        )

        text_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        scroll.add_widget(text_label)
        content.add_widget(scroll)

        self.dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.7),
            buttons=[
                MDFlatButton(
                    text="ПОНЯТНО",
                    theme_text_color="Custom",
                    text_color=(0.3, 0.6, 0.9, 1),
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
            md_bg_color=(1, 1, 1, 1),
            radius=[30, 30, 30, 30]
        )
        self.dialog.open()

    def clean_result(self, instance):
        self.result_text.text = 'Выберите или запишите новый аудиофайл для анализа.'
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
            self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio.start_recording(self.temp_file.name)
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
                        files={'audio': (os.path.basename(self.current_audio), f, 'audio/wav')},
                        timeout=60
                    )
                    Clock.schedule_once(lambda dt: setattr(self.progress, 'value', 80))
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            Clock.schedule_once(lambda dt: self.analysis_complete(data['result_content'], True))
                        else:
                            Clock.schedule_once(lambda dt: self.analysis_complete(f"Ошибка: {data.get('error', 'Неизвестная ошибка')}", False))
                    else:
                        Clock.schedule_once(lambda dt: self.analysis_complete(f"Ошибка сервера: {response.status_code}", False))
            except requests.exceptions.Timeout:
                Clock.schedule_once(lambda dt: self.analysis_complete("Ошибка: Превышено время ожидания ответа от сервера", False))
            except requests.exceptions.ConnectionError:
                Clock.schedule_once(lambda dt: self.analysis_complete("Ошибка: Не удалось подключиться к серверу. Проверьте интернет.", False))
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
