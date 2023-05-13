import speech_recognition
import pyttsx3
import openai
import tkinter as tk
import tkinter.font as font


class VoiceChat:
    """
    Класс для создания объектов голосового чата
    """

    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.ttsEngine = pyttsx3.init()

        # Устанавливаем параметры голоса
        voices = self.ttsEngine.getProperty("voices")
        self.ttsEngine.setProperty("voice", voices[0].id)

    def play_voice_assistant_speech(self, text_to_speech):
        # Воспроизводим текст
        self.ttsEngine.say(str(text_to_speech))
        self.ttsEngine.runAndWait()

    def record_and_recognize_audio(self):
        with self.microphone:

            recognized_data = ''

            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

            try:
                # Получаем звуковую дорожку
                self.play_voice_assistant_speech("Слушаю ваш вопрос")
                audio = self.recognizer.listen(self.microphone, 5, 5)

            except speech_recognition.WaitTimeoutError:
                self.play_voice_assistant_speech("Вас не слышно, проверьте свой микрофон")
                raise SystemExit

            try:
                # Переводим ее в текст
                recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                pass

            except speech_recognition.RequestError:
                self.play_voice_assistant_speech("Проверьте ваш доступ в интернет")

            return recognized_data


def generate_text(text, voice):
    """
    Функция работы с ChatGPT
    """

    # Ключ АПИ
    openai.api_key = "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"

    # Проверка списка на пустоту
    if not text:
        return

    # Объединяем текст
    search_term = ' '.join(text)

    # Задаем параметры запроса
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=search_term,
        max_tokens=1024,
    )

    # Отправляем и получаем ответ
    message = response.choices[0].text.strip()

    # Воспроизводим ответ
    voice.play_voice_assistant_speech(message)

    # Вставляем ответ в текстовое поле
    text_field.insert(tk.END, message)


def init_program():
    """
    Функция запуска основного алгоритма
    """

    # Очистка текстового поля
    text_field.delete(1.0, tk.END)

    # Создание объекта голосового чата
    voice = VoiceChat()

    # Получение текста от пользователя
    voice_input = voice.record_and_recognize_audio()

    # Передача текста в ChatGPT
    generate_text(voice_input, voice)


if __name__ == '__main__':
    # Создаем окно
    window = tk.Tk()

    # Устанавливаем заголовок окна
    window.title("Голосовой ChatGPT")

    # Устанавливаем размер окна
    window.geometry("600x300")

    # Настраиваем стиль кнопки
    button_font = font.Font(family='Helvetica', size=12, weight='bold')

    # Создаем объект текстового поля
    text_field = tk.Text(window)

    # Размещаем кнопку
    button = tk.Button(window, text="Задать вопрос", bg="green", command=init_program, width=20, height=2,
                       fg="white", font=button_font)

    # Настраиваем текстовое поле
    text_field.grid(padx=10, pady=10)
    text_field.configure(height=12, width=300)

    # Размещаем элементы управления на форме
    button.grid(row=1, column=0, columnspan=2)

    # Размещаем кнопку по центру
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Запускаем главный цикл обработки событий
    window.mainloop()
