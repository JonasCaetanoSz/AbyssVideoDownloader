from models import VideoMetadata


def resolution_extractor(video_metadata: VideoMetadata) -> dict[str, list[str]]:

    resolutions = {}

    for video_ext, media in video_metadata.media.items():

        resolutions[video_ext] = []

        for source in media.sources:

            if source.label not in resolutions[video_ext]:

                resolutions[video_ext].append(
                    source.label
                )

    return resolutions