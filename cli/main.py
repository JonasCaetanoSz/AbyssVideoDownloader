from core.slug_extractor import SlugExtractor
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



    args = parser.parse_args()


    if args.command in ["get-video-slug", "gs"]:

        try:
            slug_video = SlugExtractor( video_url=args.url )

            if slug_video:
                print( slug_video.value )

        except InvalidSlugException as e:
            print("error: " + str(e) )
        
        quit()


if __name__ == "__main__":
    main()