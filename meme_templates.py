from typing import List

class MemeTemplate():
    def __init__(
        self,
        id: str,
        name: str,
        text_areas: List[bool],
        filename: str
    ):
        self.id = id
        self.name = name
        self.text_areas = text_areas
        self.filename = filename


MEME_TEMPLATES = [
    MemeTemplate(
        'mealsome',
        'Me also me',
        [True, True],
        'mealsome.png'
    ),
    MemeTemplate(
        'itsretarded',
        "It's retarded",
        [True],
        'itsretarded.png'
    ),
    MemeTemplate(
        'headache',
        'Headache',
        [True],
        'headache.png'
    ),
    MemeTemplate(
        'itstime',
        "It's time",
        [True, True],
        'itstime.png'
    ),
    MemeTemplate(
        'classnote',
        'Class note',
        [True],
        'classnote.png'
    ),
    MemeTemplate(
        'nutbutton',
        'Button',
        [True],
        'nutbutton.jpg'
    ),
    MemeTemplate(
        'pills',
        'Pills',
        [True],
        'pills.jpg'
    ),
    MemeTemplate(
        'balloon',
        'Balloon',
        [True, True, True],
        'balloon.jpg'
    ),
    MemeTemplate(
        'classy',
        'Winnie the Pooh classy',
        [True, True],
        'classy.jpg'
    ),
    MemeTemplate(
        'cola',
        'Cola',
        [True, True],
        'cola.jpg'
    ),
    MemeTemplate(
        'loud',
        'Loud',
        [True, False],
        'loud.jpg'
    ),
    MemeTemplate(
        'milk',
        'Milking cow',
        [True, False],
        'milking.jpg'
    ),
    MemeTemplate(
        'finally',
        'Finally',
        [True, False],
        'finally.jpg'
    ),
    MemeTemplate(
        'cliff',
        'Push off cliff',
        [True, True],
        'cliff.jpg'
    ),
    MemeTemplate(
        'predatorhandshake',
        'Predator handshake',
        [True, True, True],
        'handshake.gif'
    ),
    MemeTemplate(
        'knight',
        'Knight with arrow in visor',
        [True, True],
        'knight.png'
    ),
    MemeTemplate(
        'vape',
        'Tom Scott vape',
        [True, True],
        'vape.png'
    ),
    MemeTemplate(
        'hate',
        'Winnie the Pooh hate',
        [True],
        'hate.png'
    )
]
