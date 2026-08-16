from core.thumbnail_extractor import thumbnail_extractor
from core.slug_extractor import slug_extractor

from exceptions import InvalidSlugException

import argparse


def main():

    parser = argparse.ArgumentParser(
        prog="AbyssVideoDownloader",
        allow_abbrev=False
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True
    )


    # command: get-video-slug

    slug = sub.add_parser(
        "get-video-slug",
        aliases=["gs"],
        help="Gets the video slug"
    )

    slug.add_argument(
        "-u",
        "--url",
        required=True,
        help="Video URL"
    )


    # command: get-video-thumbnail

    thumbnail = sub.add_parser(
        "get-video-thumbnail",
        aliases=["gt"],
        help="Gets the video thumbnail"
    )

    thumbnail.add_argument(
        "-u",
        "--url",
        required=True,
        help="Video URL"
    )

    thumbnail.add_argument(
        "-m",
        "--max-sprites",
        required=False,
        type=int,
        help="Maximum sprites"
    )

    args = parser.parse_args()


    if args.command in ["get-video-slug", "gs"]:

        try:
            slug_video = slug_extractor(
                video_url=args.url
            )

            if slug_video:
                print(slug_video.value)

        except InvalidSlugException as e:
            print("error: " + str(e))


    elif args.command in ["get-video-thumbnail", "gt"]:

        try:
            thumbnail = thumbnail_extractor(video_url=args.url, max_sprites=args.max_sprites)
            print("thumbnail: " + thumbnail.thumbnail + "\n" )

            for n, sprite_url in enumerate( thumbnail.sprites, start=1):
                print(f"sprite [{n}]: {sprite_url}\n")

            print("\033[33mwarning: Don't forget to add the request headers with User-Agent and Referer pointing to https://abysscdn.com/\033[0m")

        except Exception as e:
            print("error: " + str(e))


if __name__ == "__main__":
    main()