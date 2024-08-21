from typing import Union

import customtkinter
from PIL import Image

from modules.colours import Mocha
from modules.vocal_math import VocalMath

FONT = "Satoshi Variable Bold"


class App(customtkinter.CTk):
    def __init__(self, vocal_math: VocalMath, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tts = False
        self.difficulty = 1
        self.geometry("1000x900")
        self.vocal_math = vocal_math
        self.answer: Union[None, int] = None
        self.configure(fg_color=Mocha.MANTLE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=8)

        self.name_frame = NameFrame(self)
        self.name_frame.grid(
            row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=3
        )

        self.image_frame = ImageFrame(self, True)
        self.image_frame.grid(
            row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=3
        )

        self.empty_frame = customtkinter.CTkFrame(self, height=0, fg_color=Mocha.BASE)
        self.empty_frame.grid(
            row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=3
        )
        self.empty_frame.input_answer_button = None
        self.empty_frame.check_answer_button = None

        self.button = StartGameButton(self)
        self.button.grid(row=3, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)

        self.difficulty_frame = DifficultyFrame(self)
        self.difficulty_frame.grid(row=3, column=2, padx=20, pady=20, sticky="nsew")

        # self.tts_switch = customtkinter.CTkSwitch(
        #     self,
        #     text="TTS",
        #     command=self.toggle_tts,
        # )
        # self.tts_switch.grid(row=3, column=2, padx=20, pady=20, sticky="nsew")

    def start_game(self) -> None:
        self.answer = None
        self.button.configure(text="Next Problem")
        self.name_frame.label.configure(
            text="Solve the problem below!", font=("Gloria Hallelujah", 56)
        )

        self.image_frame.destroy()
        self.image_frame = ImageFrame(self, False)
        self.image_frame.grid(
            row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=3
        )

        if not self.empty_frame.input_answer_button:
            self.empty_frame.input_answer_button = InputAnswer(
                self.empty_frame, self.input_answer
            )
            self.empty_frame.input_answer_button.grid(
                row=0, column=0, padx=20, pady=20, sticky="nsew"
            )
        else:
            self.empty_frame.input_answer_button.configure(
                state="normal", border_color=Mocha.LAVENDER
            )

        if not self.empty_frame.check_answer_button:
            self.empty_frame.check_answer_button = CheckAnswer(
                self.empty_frame, self.check_answer
            )
            self.empty_frame.check_answer_button.grid(
                row=0, column=1, padx=20, pady=20, sticky="nsew"
            )
        else:
            self.empty_frame.check_answer_button.configure(
                state="disabled", border_color=Mocha.SURFACE2
            )

        expression = self.vocal_math.new_expression(self.difficulty)
        self.image_frame.label.configure(
            text=f"{expression} = ?", text_color=Mocha.TEXT
        )

        if self.tts:
            self.update()
            self.vocal_math.tts(f"What does {expression} equal to ?")

    def input_answer(self) -> None:
        self.name_frame.label.configure(
            text="Please speak the answer!", font=("Gloria Hallelujah", 56)
        )
        self.update()

        duration = 5 if self.difficulty == 1 else 10
        word = self.vocal_math.recognize_speech(duration)
        print(word)
        self.answer = self.vocal_math.word_to_number(word)
        print(self.answer)

        if self.answer is None:
            self.name_frame.label.configure(
                text="Your voice wasn't clear can you please try again?",
                font=("Gloria Hallelujah", 36),
            )
            return

        self.name_frame.label.configure(
            text="Is your answer correct?", font=("Gloria Hallelujah", 56)
        )
        self.image_frame.label.configure(
            text=f"{self.image_frame.label.cget('text').replace('?', str(self.answer) + ' ?')}",
            text_color=Mocha.LAVENDER,
        )
        self.empty_frame.check_answer_button.configure(
            state="normal", border_color=Mocha.LAVENDER
        )

    def check_answer(self) -> None:
        if self.vocal_math.check_answer(self.answer):
            self.name_frame.label.configure(
                text="Your answer is correct!", font=("Gloria Hallelujah", 56)
            )
            self.image_frame.label.configure(
                text_color=Mocha.GREEN,
                text=self.image_frame.label.cget("text").replace(" ?", ""),
            )
            self.empty_frame.input_answer_button.configure(
                state="disabled", border_color=Mocha.SURFACE2
            )
        else:
            self.name_frame.label.configure(
                text="Your answer is wrong!", font=("Gloria Hallelujah", 56)
            )
            self.image_frame.label.configure(
                text_color=Mocha.RED,
                text=self.image_frame.label.cget("text")
                .replace(" ?", "")
                .replace("=", "≠"),
            )
            self.answer = None

        self.empty_frame.check_answer_button.configure(
            state="disabled", border_color=Mocha.SURFACE2
        )

    def set_difficulty(self, difficulty: int) -> None:
        self.difficulty = difficulty

    def toggle_tts(self) -> None:
        self.tts = not self.tts


class NameFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=Mocha.BASE)

        self.label = customtkinter.CTkLabel(
            self,
            font=("Gloria Hallelujah", 76),
            text="Math Echo Blitz",
            text_color=Mocha.LAVENDER,
        )
        self.label.pack()


class ImageFrame(customtkinter.CTkFrame):
    def __init__(self, master, image: bool, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=Mocha.BASE)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = (
            customtkinter.CTkLabel(
                self,
                text="",
                font=("Gloria Hallelujah", 128),
                text_color=Mocha.TEXT,
                image=customtkinter.CTkImage(
                    Image.open(r"assets/background.png"), size=(1000, 900)
                ),
            )
            if image
            else customtkinter.CTkLabel(
                self,
                text="",
                font=("Gloria Hallelujah", 128),
                text_color=Mocha.TEXT,
            )
        )

        self.label.grid(row=0, column=0, sticky="nsew")


class StartGameButton(customtkinter.CTkButton):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            text="Start Game",
            font=(FONT, 32),
            border_width=2,
            command=master.start_game,
            fg_color=Mocha.BASE,
            hover_color=Mocha.MANTLE,
            text_color=Mocha.LAVENDER,
            border_color=Mocha.LAVENDER,
        )


class DifficultyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.master: App = master
        self.configure(fg_color=Mocha.BASE)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.label = customtkinter.CTkLabel(
            self,
            text="Difficulty Level",
            font=(FONT, 32),
            text_color=Mocha.LAVENDER,
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

        self.difficulty = customtkinter.IntVar(value=0)
        easy = customtkinter.CTkRadioButton(
            self,
            value=1,
            text="Easy",
            font=(FONT, 16),
            fg_color=Mocha.GREEN,
            hover_color=Mocha.GREEN,
            border_color=Mocha.TEXT,
            variable=self.difficulty,
            command=self.radio_button_event,
        )
        medium = customtkinter.CTkRadioButton(
            self,
            value=2,
            text="Medium",
            font=(FONT, 16),
            fg_color=Mocha.PEACH,
            hover_color=Mocha.PEACH,
            border_color=Mocha.TEXT,
            variable=self.difficulty,
            command=self.radio_button_event,
        )
        hard = customtkinter.CTkRadioButton(
            self,
            value=3,
            text="Hard",
            font=(FONT, 16),
            fg_color=Mocha.RED,
            hover_color=Mocha.RED,
            border_color=Mocha.TEXT,
            variable=self.difficulty,
            command=self.radio_button_event,
        )

        easy.select()
        easy.grid(row=1, column=0, padx=20, pady=20, sticky="ns")
        medium.grid(row=1, column=1, padx=20, pady=20, sticky="ns")
        hard.grid(row=1, column=2, padx=20, pady=20, sticky="ns")

    def radio_button_event(self) -> None:
        self.master.set_difficulty(self.difficulty.get())


class InputAnswer(customtkinter.CTkButton):
    def __init__(self, master, command, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            text="Input Answer",
            font=(FONT, 36),
            border_width=2,
            command=command,
            border_spacing=20,
            fg_color=Mocha.BASE,
            hover_color=Mocha.MANTLE,
            text_color=Mocha.LAVENDER,
            border_color=Mocha.LAVENDER,
        )


class CheckAnswer(customtkinter.CTkButton):
    def __init__(self, master, command, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            state="disabled",
            text="Check Answer",
            border_width=2,
            font=(FONT, 36),
            border_spacing=20,
            command=command,
            fg_color=Mocha.BASE,
            hover_color=Mocha.MANTLE,
            text_color=Mocha.LAVENDER,
            border_color=Mocha.SURFACE2,
        )


if __name__ == "__main__":
    app = App(VocalMath(r"assets/vosk-model-en-in-0.5"))
    app.mainloop()
