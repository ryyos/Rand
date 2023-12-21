import json

class Writer:
    def __init__(self) -> None:
        pass

    def ex(self, path: str, content: any) -> None:
        with open(path, 'w', encoding= "utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=2, default=str)

    def exstr(self, path: str, content: any) -> None:
        with open(path, 'w', encoding="utf-8") as file:
            file.writelines(content)

    def eby(self, path: str, media: any) -> None:
        with open(path, 'wb') as file:
            file.write(media.content)