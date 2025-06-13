"""
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""


def draw_xmas_tree(levels=7):
    for i in range(levels):
        spaces = " " * (levels - i - 1)
        stars = "*" * (2 * i + 1)
        print(spaces + stars)
    print(" " * (levels - 1) + "|")


if __name__ == "__main__":
    draw_xmas_tree(7)
