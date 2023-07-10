class WrongId(Exception):
    """Класс исключения при несуществующем id"""

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Видео с таким id не существует'

