import pyfiglet


def text_to_ascii_art(text):
    ascii_art = pyfiglet.figlet_format(text)
    return ascii_art


input_text = "Hello, World!"
ascii_art_text = text_to_ascii_art(input_text)
print(ascii_art_text)
