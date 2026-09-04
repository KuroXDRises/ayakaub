import edge_tts

class Speak:
    def __init__(self, text:str, voice:str="en-IN-NeerjaExpressiveNeural"):
        self.text = text
        self.voice = voice
        self.output_file = "ayaka.mp3"
        
    async def save(self) -> str:
        communicate = edge_tts.Communicate(text=self.text, voice=self.voice)
        await communicate.save(self.output_file)
        return self.output_file