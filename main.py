import customtkinter

from modules.colours import Mocha
from modules.vocal_math import VocalMath

FONT = "Source Code Pro"


class App(customtkinter.CTk):
    def __init__(self, vocal_math: VocalMath, **kwargs) -> None:
        super().__init__(**kwargs)
        self.difficulty = 1
        self.geometry("1000x900")
        self.vocal_math = vocal_math
        self.configure(fg_color=Mocha.MANTLE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=4)

        NameFrame(self).grid(
            row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=2
        )

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(
            row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=2
        )

        StartGameButton(self).grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        DifficultyFrame(self).grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

    def start_game(self) -> None:
        expression = self.vocal_math.new_expression(self.difficulty)
        self.image_frame.label.configure(text=expression)

    def set_difficulty(self, difficulty: int) -> None:
        self.difficulty = difficulty


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
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=Mocha.BASE)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self, text="", font=("Gloria Hallelujah", 128), text_color=Mocha.GREEN
        )
        self.label.grid(row=0, column=0, sticky="nsew")


class StartGameButton(customtkinter.CTkButton):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            text="Start Game",
            font=(FONT, 48),
            command=master.start_game,
            fg_color=Mocha.BASE,
            text_color=Mocha.LAVENDER,
            border_color=Mocha.LAVENDER,
            border_width=3,
            hover_color=Mocha.MANTLE,
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
            font=(FONT, 36),
            text_color=Mocha.LAVENDER,
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

        self.difficulty = customtkinter.IntVar(value=0)
        easy = customtkinter.CTkRadioButton(
            self,
            text="Easy",
            variable=self.difficulty,
            value=1,
            command=self.radio_button_event,
        )
        medium = customtkinter.CTkRadioButton(
            self,
            text="Medium",
            variable=self.difficulty,
            value=2,
            command=self.radio_button_event,
        )
        hard = customtkinter.CTkRadioButton(
            self,
            text="Hard",
            variable=self.difficulty,
            value=3,
            command=self.radio_button_event,
        )

        easy.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        medium.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        hard.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

    def radio_button_event(self) -> None:
        self.master.set_difficulty(self.difficulty.get())


if __name__ == "__main__":
    app = App(VocalMath(r"assets/vosk-model-en-in-0.5"))
    app.mainloop()
