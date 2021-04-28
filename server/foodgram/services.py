from django.utils.text import slugify


def user_directory_path(instance, filename):
    return f'recipies/{instance.author.username}/{filename}'


def pretty_slugify(title: str):
    slug = title.translate(
            str.maketrans(
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
        )
    return slugify(slug)
