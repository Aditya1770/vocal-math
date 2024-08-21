import json
import random
from math import sqrt
from random import randint
from typing import Union

import sounddevice as sound_device
import vlc
from gtts import gTTS
from vosk import Model, KaldiRecognizer
from word2number import w2n


def check_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


class VocalMath:
    def __init__(
        self,
        model_path: str,
        sample_rate: int = 16000,
        channels: int = 1,
    ) -> None:
        self.channels: int = channels
        self.sample_rate: int = sample_rate
        self.answer: Union[None, float] = None
        self.expression: Union[None, str] = None

        model = Model(model_path)
        self.recognizer = KaldiRecognizer(model, 16000)

    def new_expression(self, difficulty: int) -> str:
        operator = random.choice(["+", "-", "*", "/"][0 : difficulty + 1])

        if operator == "/":
            num1 = random.choice(
                [
                    i
                    for i in range(10 ** (difficulty - 1), 10**difficulty + 1)
                    if not check_prime(i)
                ]
            )

            divisors = set()
            for i in range(2, int(sqrt(num1)) + 1):
                if num1 % i == 0:
                    divisors.add(i)
                    divisors.add(num1 // i)

            num2 = random.choice(list(divisors))

        elif operator == "-":
            num1 = randint(10 ** (difficulty - 1), 10**difficulty)
            num2 = randint(1, num1)

        else:
            num1, num2 = randint(10 ** (difficulty - 1), 10**difficulty), randint(
                10 ** (difficulty - 1), 10**difficulty
            )

        self.expression = f"{num1} {operator} {num2}"
        return self.expression.replace("*", "×").replace("/", "÷")

    def recognize_speech(self, duration: float) -> Union[None, str]:
        frames = int(duration * self.sample_rate)
        with sound_device.InputStream(
            samplerate=self.sample_rate, channels=self.channels, dtype="int16"
        ) as stream:
            data, _ = stream.read(frames)

            if self.recognizer.AcceptWaveform(data.tobytes()):
                result = self.recognizer.Result()
                return json.loads(result).get("text", "")

            else:
                result = self.recognizer.PartialResult()
                return json.loads(result).get("text", "")

    def check_answer(self, answer: int) -> bool:
        return eval(self.expression) == answer

    @staticmethod
    def word_to_number(word: str) -> Union[None, int]:
        try:
            return w2n.word_to_num(word)
        except ValueError:
            return None

    @staticmethod
    def tts(text):
        file = r"sound.mp3"
        gTTS(text=text.replace("-", "minus"), lang="en").save(file)
        vlc.MediaPlayer(file).play()
