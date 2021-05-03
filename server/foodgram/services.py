from django.utils.text import slugify


RUS_TRANS = """абвгдеёжзийклмнопрстуфхцчшщъыьэюя
               АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"""
ENG_TRANS = """abvgdeejzijklmnoprstufhzcss_y_eua
               ABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"""


def user_directory_path(instance, filename):
    return f'recipies/{instance.author.username}/{filename}'


def pretty_slugify(title: str):
    slug = title.translate(str.maketrans(RUS_TRANS,ENG_TRANS))
    return slugify(slug)
