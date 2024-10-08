import tempfile
import uuid
from io import BytesIO

import extcolors
import matplotlib.pyplot as plt
from colormap import rgb2hex


def upload_user_image(instance, filename):   # noqa
    return f"color_extraction/{uuid.uuid4()}/{filename}"


def extract_colors(image_data, tolerance=25, limit=7):
    with tempfile.NamedTemporaryFile(delete=False) as temp_img:
        temp_img.write(image_data)

        colors_x = extcolors.extract_from_path(
            temp_img.name, tolerance=tolerance, limit=limit
        )

        rgb_list = [el[0] for el in colors_x[0][:limit]]
        hex_colors = [rgb2hex(el[0], el[1], el[2]) for el in rgb_list]
        color_occurrence = [el[1] for el in colors_x[0][:limit]]
        color_occurrence_sum = sum(color_occurrence)
        color_percents = [
            str(round(el[1] / color_occurrence_sum * 100, 2)) + "%"
            for el in colors_x[0][:limit]
        ]

        fig, ax = plt.subplots(figsize=(10, 10))
        fig.patch.set_facecolor("black")

        my_circle = plt.Circle(
            (0, 0), 0.7, edgecolor="white", linewidth=2, facecolor="black"
        )

        ax.pie(
            color_occurrence,
            labels=color_percents,
            colors=hex_colors,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"fontsize": 13, "color": "white", "weight": "bold"},
        )
        ax.add_artist(my_circle)

        legend = ax.legend(
            hex_colors,
            loc="center",
            title="$\\bf{Colors}$",
            fontsize=14,
            title_fontsize=15,
            labelcolor="white",
        )
        legend.get_title().set_color("white")
        legend.get_frame().set_facecolor("gray")

        with BytesIO() as result_image_buffer:
            plt.savefig(result_image_buffer, format="png")
            result_image_data = result_image_buffer.getvalue()

        plt.close(fig)
        return result_image_data
