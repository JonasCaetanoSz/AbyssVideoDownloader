from core import thumbnail_extractor
from core import slug_extractor
from core import metadata_extractor
from core import download_video

from models import Resolution

import argparse
import json


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


    # command: get-video-metadata

    metadata = sub.add_parser(
        "get-video-metadata",
        aliases=["gm"],
        help="Gets the video metadata"
    )

    metadata.add_argument(
        "-u",
        "--url",
        required=True,
        help="Video URL"
    )

    metadata.add_argument(
        "--json",
        action="store_true",
        help="Output metadata as JSON object"
    )


    # command: download-video

    download = sub.add_parser(
        "download-video",
        aliases=["dl"],
        help="Downloads the video"
    )

    download.add_argument(
        "-u",
        "--url",
        required=True,
        help="Video URL"
    )

    download.add_argument(
        "-o",
        "--output",
        required=False,
        help="Output file name"
    )

    download.add_argument(
        "-r",
        "--resolution",
        required=False,
        default="360p",
        help="Download resolution"
    )

    download.add_argument(
        "-mw",
        "--max-workers",
        required=False,
        type=int,
        default=8,
        help="Maximum download workers"
    )

    download.add_argument(
        "-hp",
        "--hide-progress",
        action="store_true",
        help="Hide download progress"
    )

    download.add_argument(
        "-mr",
        "--max-retries",
        required=False,
        type=int,
        default=3,
        help="Maximum segment download retries"
    )


    # command: download-list

    download_list = sub.add_parser(
        "download-list",
        aliases=["dlm"],
        help="Downloads multiple videos"
    )

    download_list.add_argument(
        "-f",
        "--file",
        required=True,
        help="File containing video URLs"
    )

    download_list.add_argument(
        "-o",
        "--output",
        required=False,
        help="Output directory"
    )

    download_list.add_argument(
        "-r",
        "--resolution",
        required=False,
        default="360p",
        help="Download resolution"
    )

    download_list.add_argument(
        "-mw",
        "--max-workers",
        required=False,
        type=int,
        default=8,
        help="Maximum download workers"
    )

    download_list.add_argument(
        "-hp",
        "--hide-progress",
        action="store_true",
        help="Hide download progress"
    )

    download_list.add_argument(
        "-mr",
        "--max-retries",
        required=False,
        type=int,
        default=3,
        help="Maximum segment download retries"
    )


    args = parser.parse_args()


    # execute: get-video-slug

    if args.command in ["get-video-slug", "gs"]:

        try:

            slug_video = slug_extractor(
                video_url=args.url
            )

            if slug_video:
                print(
                    slug_video.value
                )

        except Exception as e:
            print(
                "error: " + str(e)
            )


    # execute: get-video-thumbnail

    elif args.command in ["get-video-thumbnail", "gt"]:

        try:

            thumbnail = thumbnail_extractor(
                video_url=args.url,
                max_sprites=args.max_sprites
            )

            print(
                "thumbnail: " + thumbnail.thumbnail + "\n"
            )

            for n, sprite_url in enumerate(
                thumbnail.sprites,
                start=1
            ):
                print(
                    f"sprite [{n}]: {sprite_url}\n"
                )

            print(
                "\033[33mwarning: Don't forget to add the request headers "
                "with User-Agent and Referer pointing to https://abysscdn.com/\033[0m"
            )

        except Exception as e:
            print(
                "error: " + str(e)
            )


    # execute: get-video-metadata

    elif args.command in ["get-video-metadata", "gm"]:

        try:

            metadata = metadata_extractor(
                video_url=args.url
            )

            if args.json:

                print(
                    json.dumps(
                        metadata.to_dict(),
                        indent=2
                    )
                )

            else:

                print(
                    metadata.to_dict()
                )

        except Exception as e:
            print(
                "error: " + str(e)
            )


    # execute: download-video

    elif args.command in ["download-video", "dl"]:

        try:

            metadata = metadata_extractor(
                video_url=args.url
            )

            resolution = Resolution(
                args.resolution
            )

            result, output_path = download_video(
                video_metadata=metadata,
                resolution=resolution,
                output=args.output,
                max_workers=args.max_workers,
                hide_progress=args.hide_progress,
                max_retries=args.max_retries
            )

            print(
                f"Download completed: {output_path}"
            )

        except Exception as e:
            print(
                "error: " + str(e)
            )


    # execute: download-list

    elif args.command in ["download-list", "dlm"]:

        try:

            resolution = Resolution(
                args.resolution
            )

            with open(
                args.file,
                "r",
                encoding="utf-8"
            ) as file:

                urls = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]


            for index, url in enumerate(
                urls,
                start=1
            ):

                try:

                    print(
                        f"\n[{index}/{len(urls)}] Processing: {url}"
                    )

                    metadata = metadata_extractor(
                        video_url=url
                    )

                    result, output_path = download_video(
                        video_metadata=metadata,
                        resolution=resolution,
                        output=args.output,
                        max_workers=args.max_workers,
                        hide_progress=args.hide_progress,
                        max_retries=args.max_retries
                    )

                    print(
                        f"Download completed: {output_path}"
                    )


                except Exception as e:

                    print(
                        f"Failed: {url}"
                    )

                    print(
                        "error: " + str(e)
                    )


        except Exception as e:

            print(
                "error: " + str(e)
            )


if __name__ == "__main__":
    main()