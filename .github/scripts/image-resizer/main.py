#!/usr/bin/env python

from PIL import Image
from pathlib import Path
import logging
import argparse

logging.basicConfig(level=logging.INFO)


def crop_and_resize(img: Image.Image, width: int, height: int) -> Image.Image:
    img_ratio = img.size[0] / float(img.size[1])
    ratio = width / height
    if ratio > img_ratio:
        img = img.resize(
            (width, int(img.size[1] * width / img.size[0])),
            Image.ANTIALIAS,
        )
        img = img.crop(
            box=(
                0,  # left
                (img.size[1] - height) // 2,  # upper
                width,  # right
                (img.size[1] + height) // 2,  # lower
            )
        )
    elif ratio < img_ratio:
        img = img.resize(
            (int(img.size[0] * height / img.size[1]), height),
            Image.ANTIALIAS,
        )
        img = img.crop(
            box=(
                (img.size[0] - width) // 2,  # left
                0,  # upper
                (img.size[0] + width) // 2,  # right
                height,  # lower
            )
        )
    else:
        img = img.resize((width, height), Image.ANTIALIAS)
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_file", help="image file path")
    parser.add_argument("width", help="generated image width", type=int)
    parser.add_argument("height", help="generated image height", type=int)
    args = parser.parse_args()
    try:
        img = Image.open(Path(args.image_file))
        img = crop_and_resize(img, args.width, args.height)
        store_path = Path(args.image_file).resolve().parents[0] / "{}x{}.png".format(
            args.width, args.height
        )
        img.save(store_path, bitmap_format="png")
        print("successed {}".format(args.image_file))
    except:
        logging.warn("invalid file name: {}".format(args.image_file))


if __name__ == "__main__":
    main()

# CI の最初の行のコミットログの出し方
# export $ACTION_MESSAGE="[IMAGE RESIZER CI]"
# git log --oneline | grep $ACTION_MESSAGE | head -n 1 | tr -s " " | cut -d " " -f 1
# コミットがあれば、それ用のブランチを作る
# プルリクのリストを取ってくる
# 同一のタイトルのPRとブランチを閉じる
# git diff -AM <- 更新と変更のファイルのみ検知
