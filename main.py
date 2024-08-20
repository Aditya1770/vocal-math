import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
from word2number import w2n
import random

pathModel = "enter vosk model path"
model = Model(pathModel)
recognizer = KaldiRecognizer(model, 16000)

def word2num(text):
    try:
        return w2n.word_to_num(text)
    except ValueError:
        return None

def ifMinus(expression):
    words = expression.split()
    if words[0] == "minus" and len(words) > 1:
        try:
            number = word2num(" ".join(words[1:]))
            if number is not None:
                return -number
        except ValueError:
            return None
    return word2num(expression)

def recognizeSpeech():
    with sd.InputStream(samplerate=16000, channels=1, dtype='int16') as stream:
        while True:
            data, _ = stream.read(2048)
            if recognizer.AcceptWaveform(data.tobytes()):
                result = recognizer.Result()
                spoken_text = json.loads(result).get('text', '')
                print(f"Recognized Text: {spoken_text}")
                if spoken_text:
                    return spoken_text
            else:
                result = recognizer.PartialResult()
                spoken_text = json.loads(result).get('partial', '')
                if spoken_text:
                    print(f"Partial Recognized Text: {spoken_text}")

def nextPuzzle():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    operator = random.choice(['+', '-'])
    
    if operator == '+':
        return num1, num2, num1 + num2, f"What is {num1} + {num2}?"
    elif operator == '-':
        return num1, num2, num1 - num2, f"What is {num1} - {num2}?"

def main():
    while True:
        num1, num2, current_answer, puzzle = nextPuzzle()
        print(puzzle)
        
        while True:
            recognized_text = recognizeSpeech()
            if not recognized_text:
                print("No speech recognized. Please try again.")
                continue

            processed_number = ifMinus(recognized_text)
            if processed_number is not None:
                print(f"Processed Expression: {processed_number}")
                if processed_number == current_answer:
                    print("Correct! Showing next puzzle.")
                    break
                else:
                    print(f"Incorrect. The expected answer was {current_answer}. Please try again.")
            else:
                print("Could not recognize or process the expression. Please try again.")

if __name__ == "__main__":
    main()
