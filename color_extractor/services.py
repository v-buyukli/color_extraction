import os

import extcolors
import matplotlib.pyplot as plt
import requests
from colormap import rgb2hex


def extract_colors(img_url, img_name, tolerance=25, limit=7):
    img_data = requests.get(img_url).content
    with open(img_name, "wb") as handler:
        handler.write(img_data)

    colors_x = extcolors.extract_from_path(img_name, tolerance=tolerance, limit=limit)
    rgb_list = [el[0] for el in colors_x[0]]
    hex_colors = [rgb2hex(el[0], el[1], el[2]) for el in rgb_list]
    color_occurrence = [el[1] for el in colors_x[0]]
    color_occurrence_sum = sum(color_occurrence)
    color_percents = [
        str(round(el[1] / color_occurrence_sum * 100, 2)) + "%" for el in colors_x[0]
    ]

    print("Colors:")
    colors = zip(hex_colors, color_percents)
    for color in colors:
        print(color[0], "=", color[1])

    my_circle = plt.Circle((0, 0), 0.75,
                            edgecolor="black", linewidth=0.5, facecolor="white")
    plt.pie(
        color_occurrence,
        labels=color_percents,
        colors=hex_colors,
        wedgeprops={"edgecolor": "black",
                     'linewidth': 0.5},
    )
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.legend(hex_colors, loc="center", title="Colors")
    name_result = img_name.replace(".jpg", "_result.png")
    plt.savefig(f"color_extractor/static/color_extractor/{name_result}")

    if os.path.exists("test_image.jpg"):
        os.remove("test_image.jpg")
    else:
        print("The file does not exist")
