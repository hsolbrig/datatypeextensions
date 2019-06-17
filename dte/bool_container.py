

class BOOL:
    """  Boolean container -- supports global boolean variables """
    def __init__(self, v: bool) -> None:
        self.v = v

    def __bool__(self):
        return self.v

    def __str__(self):
        return str(self.v)

