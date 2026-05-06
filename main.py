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
from android.permissions import request_permissions, Permission, check_permission
from plyer import filechooser
from android.storage import app_storage_path
from jnius import autoclass

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
        self.recorder = None

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
            text="Ещё не было проанализировано ни одного аудиофайла.",
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

        file_text = Label(text="Имя файла:", font_size=sp(16), color='black', size_hint=(0.3, 1))

        self.file_name = Label(text="файл не выбран", font_size=sp(16), color='gray',
                               size_hint=(0.7, 1))

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
                                              radius=[dp(50)])
            Color(0.875, 0.918, 0.957, 1)
            self.space_bg = RoundedRectangle(size=space.size, pos=space.pos, radius=[dp(50)])
            Color(1, 1, 1, 1)
            self.file_bg = RoundedRectangle(size=file_layout.size, pos=file_layout.pos,
                                            radius=[dp(40)])

        main_layout.bind(size=self.adapt_main, pos=self.adapt_main)
        result_layout.bind(size=self.adapt_result, pos=self.adapt_result)
        file_layout.bind(size=self.adapt_file, pos=self.adapt_file)
        space.bind(size=self.adapt_space, pos=self.adapt_space)
        self.result_text.bind(
            size=self.adapt_result_text,
            texture_size=lambda inst, val: setattr(inst, 'height', val[1] + dp(50))
        )
        info_button.bind(on_release=self.show_instructions)

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
        self.result_text.text = '''[b]КАК ИСПОЛЬЗОВАТЬ ПРИЛОЖЕНИЕ[/b]\n
1. Нажмите кнопку "Прикрепить", чтобы выбрать аудиофайл из памяти телефона.
2. Нажмите кнопку "Микрофон", чтобы начать запись. Для остановки записи нажмите ещё раз.
3. Нажмите большую кнопку "Старт", чтобы начать анализ.'''
        self.clean_button.disabled = False
        self.result_text.markup = True

    def clean_result(self, instance):
        self.result_text.text = "Выберите новый аудиофайл для анализа."
        self.clean_button.disabled = True

    def attach_file(self, instance):
        if not check_permission('android.permission.READ_EXTERNAL_STORAGE') or not check_permission(
                'android.permission.WRITE_EXTERNAL_STORAGE'):
            self.result_text.text = "[color=ff0000][b]Ошибка:[/b] Нет доступа к файлам. Предоставьте разрешения в " \
                                    "настройках.[/color]"
            self.result_text.markup = True
            self.clean_button.disabled = False
            return
        filechooser.open_file(on_selection=self.show_file_name, filters=["*.wav"])

    def show_file_name(self, selection):
        if selection:
            file_path = selection[0]

            if not file_path.lower().endswith('.wav'):
                self.result_text.text = "[color=ff0000][b]Ошибка:[/b] Поддерживаются только файлы формата .wav[/color]"
                self.result_text.markup = True
                self.clean_button.disabled = False
                return

            self.current_audio = file_path
            self.audio = None
            self.is_playing = False
            file_basename = os.path.basename(file_path)

            if len(file_basename) > 14:
                name_without_ext = os.path.splitext(file_basename)[0]
                extension = os.path.splitext(file_basename)[1]
                short_name = name_without_ext[:13] + '...' + extension
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
        if not check_permission('android.permission.RECORD_AUDIO'):
            self.result_text.text = "[color=ff0000][b]Ошибка:[/b] Нет доступа к микрофону. Предоставьте разрешения в " \
                                    "настройках.[/color]"
            self.result_text.markup = True
            self.clean_button.disabled = False
            return

        if not check_permission('android.permission.WRITE_EXTERNAL_STORAGE'):
            self.result_text.text = "[color=ff0000][b]Ошибка:[/b] Нет доступа к файлам для сохранения записи. " \
                                    "Предоставьте разрешения в настройках.[/color]"
            self.result_text.markup = True
            self.clean_button.disabled = False
            return

        if not self.is_recording:
            try:
                self.is_recording = True
                from datetime import datetime

                recordings_dir = os.path.join(app_storage_path(), 'Recordings')
                if not os.path.exists(recordings_dir):
                    os.makedirs(recordings_dir)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.temp_file = os.path.join(recordings_dir, f'recording_{timestamp}.wav')

                MediaRecorder = autoclass('android.media.MediaRecorder')
                AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
                AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
                OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')

                self.recorder = MediaRecorder()
                self.recorder.setAudioSource(AudioSource.MIC)
                self.recorder.setOutputFormat(OutputFormat.MPEG_4)
                self.recorder.setAudioEncoder(AudioEncoder.AAC)
                self.recorder.setAudioSamplingRate(44100)
                self.recorder.setAudioChannels(1)
                self.recorder.setAudioEncodingBitRate(128000)
                self.recorder.setOutputFile(self.temp_file)
                self.recorder.prepare()
                self.recorder.start()

                instance.icon = 'stop'
                self.result_text.text = "Идет запись... Нажмите кнопку микрофона еще раз для остановки."
                self.result_text.markup = False
                self.clean_button.disabled = False
            except Exception as e:
                self.is_recording = False
                self.result_text.text = f"[color=ff0000][b]Ошибка записи:[/b] {str(e)}[/color]"
                self.result_text.markup = True
                self.clean_button.disabled = False
        else:
            try:
                if self.recorder:
                    self.recorder.stop()
                    self.recorder.release()
                    self.recorder = None

                self.is_recording = False

                if os.path.exists(self.temp_file) and os.path.getsize(self.temp_file) > 0:
                    wav_file = self.convert_to_wav(self.temp_file)
                    if wav_file:
                        self.current_audio = wav_file
                        file_basename = os.path.basename(wav_file)

                        if len(file_basename) > 13:
                            name_without_ext = os.path.splitext(file_basename)[0]
                            extension = os.path.splitext(file_basename)[1]
                            short_name = name_without_ext[:13] + '...' + extension
                            file_basename = short_name

                        self.file_name.text = file_basename
                        self.file_name.color = 'blue'
                        self.button_start.disabled = False
                        self.button_play.disabled = False
                        self.result_text.text = "Запись завершена. Нажмите Старт для анализа."
                        self.result_text.markup = False
                else:
                    self.result_text.text = "[color=ff0000][b]Ошибка:[/b] Запись не удалась или файл пуст.[/color]"
                    self.result_text.markup = True

                instance.icon = 'microphone'
            except Exception as e:
                self.is_recording = False
                self.result_text.text = f"[color=ff0000][b]Ошибка при остановке записи:[/b] {str(e)}[/color]"
                self.result_text.markup = True
                self.clean_button.disabled = False
                instance.icon = 'microphone'

    def convert_to_wav(self, input_file):
        """Конвертирует аудиофайл в WAV формат используя MediaExtractor и MediaCodec"""
        try:
            import subprocess

            wav_file = input_file.rsplit('.', 1)[0] + '.wav'

            # Используем ffmpeg если доступен, или другую конвертацию
            try:
                subprocess.run(['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le',
                                '-ar', '16000', '-ac', '1', wav_file],
                               check=True, capture_output=True, timeout=30)
                return wav_file
            except:
                # Альтернативный метод конвертации через Android API
                return self.convert_android(input_file, wav_file)

        except Exception as e:
            print(f"Conversion error: {e}")
            return None

    def convert_android(self, input_file, output_file):
        try:
            MediaExtractor = autoclass('android.media.MediaExtractor')
            MediaFormat = autoclass('android.media.MediaFormat')
            MediaCodec = autoclass('android.media.MediaCodec')
            ByteBuffer = autoclass('java.nio.ByteBuffer')

            extractor = MediaExtractor()
            extractor.setDataSource(input_file)

            track_index = -1
            for i in range(extractor.getTrackCount()):
                format = extractor.getTrackFormat(i)
                mime = format.getString(MediaFormat.KEY_MIME)
                if mime.startswith("audio/"):
                    track_index = i
                    break

            if track_index < 0:
                return None

            extractor.selectTrack(track_index)

            import shutil
            shutil.copy2(input_file, output_file)
            return output_file

        except Exception as e:
            print(f"Android conversion error: {e}")
            return None

    def start_analysis(self, instance):
        if not self.current_audio:
            return

        if not check_permission('android.permission.INTERNET'):
            self.result_text.text = f"[color=ff0000][b]Ошибка:[/b] Нет доступа к сети Интернет. Предоставьте " \
                                    f"разрешения в настройках.[/color]"
            self.result_text.markup = True
            self.clean_button.disabled = False
            return

        self.button_start.disabled = True
        self.progress.opacity = 1
        self.progress.value = 10
        self.result_text.text = "Анализ аудиофайла...\n\nПодождите, это может занять до 30 секунд."

        def analyze_async():
            try:
                file_size = os.path.getsize(self.current_audio)
                if file_size == 0:
                    Clock.schedule_once(
                        lambda dt: self.analysis_complete("Ошибка: Файл пуст.", False))
                    return

                with open(self.current_audio, 'rb') as f:
                    Clock.schedule_once(lambda dt: setattr(self.progress, 'value', 30))

                    files = {
                        'audio': (os.path.basename(self.current_audio), f, 'audio/wav')
                    }

                    response = requests.post(
                        f'{API_URL}/analyze',
                        files=files,
                        timeout=60
                    )

                    Clock.schedule_once(lambda dt: setattr(self.progress, 'value', 80))

                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            Clock.schedule_once(lambda dt: self.analysis_complete(data['result_content'], True))
                        else:
                            Clock.schedule_once(
                                lambda dt: self.analysis_complete(f"Ошибка: {data.get('error', 'Неизвестная ошибка.')}",
                                                                  False))
                    else:
                        error_msg = f"Ошибка сервера: {response.status_code}"
                        try:
                            error_data = response.json()
                            error_msg += f" - {error_data.get('error', '')}"
                        except:
                            pass
                        Clock.schedule_once(
                            lambda dt: self.analysis_complete(error_msg, False))

            except requests.exceptions.Timeout:
                Clock.schedule_once(
                    lambda dt: self.analysis_complete("Ошибка: Превышено время ожидания ответа от сервера.", False))
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
    
