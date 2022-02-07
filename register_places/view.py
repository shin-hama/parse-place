from tracemalloc import start
from pywebio.input import input, TEXT, input_group, radio, textarea
from pywebio.session import go_app
from pywebio.output import put_text
from pywebio.platform.tornado import start_server


test: list[str] = []
with open("spots.txt", mode="r", encoding="utf-8") as f:
    test = f.readlines()


def index():
    # 数値入力
    result = input_group(
        "",
        [
            input(
                "観光スポット", name="spot", type=TEXT, placeholder="スポットを入力", required=True
            ),
            radio("inputted", options=test, name="op"),
        ],
    )
    spot = result["spot"]
    test.append(spot)

    with open("spots.txt", mode="a", encoding="utf-8") as f:
        f.write(f'"{spot}",\n')

    go_app("index", new_window=False)


start_server([index], port=8001)
