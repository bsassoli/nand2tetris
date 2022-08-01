class CodeWriter():
    def __init__(self, fileName) -> None:
        self.fileName = fileName
    
    def writeArithmetic(self, command: str) -> str:
        pass

    def writePushPop(self, command: str, segment: str, index: int) -> str:
        pass

    def close(self) -> None:
        pass
