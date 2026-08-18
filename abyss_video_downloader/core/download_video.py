import math
import requests
import tempfile
import shutil

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from ..exceptions import (
    VideoSourceNotFoundException,
    ResolutionNotAvailableException,
    MissingSegmentException

)
from ..models import VideoMetadata, Resolution

from ..utils import build_base_url

from ..crypto import Decryptor


FRAGMENT_SIZE = 2097152
TIMEOUT = 30
YELLOW = "\033[93m"
RESET = "\033[0m"

HEADERS = {"Referer": "https://abysscdn.com/", "User-Agent": "Mozilla/5.0"}


def download_video(video_metadata: VideoMetadata, resolution: Resolution, output: str | None = None, max_workers: int = 8, hide_progress: bool = False, max_retries: int = 3) -> tuple[bool, str]:
    source_ext = "mp4"
    media = video_metadata.media.get(source_ext)

    if not media:
        source_ext = list(video_metadata.media.keys())[0]
        media = video_metadata.media.get(source_ext)

    if not media:
        raise VideoSourceNotFoundException()

    if not video_metadata.has_resolution(video_ext=source_ext, resolution=resolution):
        raise ResolutionNotAvailableException(resolution=resolution)

    source = next((item for item in media.sources if item.label == resolution.value), None)

    if not source:
        raise ResolutionNotAvailableException(resolution=resolution)

    output_path = Path(output or video_metadata.title)

    if output_path.exists() and output_path.is_dir():
        output_path = output_path / video_metadata.title

    if not output_path.suffix:
        output_path = output_path.with_suffix(f".{source_ext}")

    elif output_path.suffix.lower().replace(".", "") != source_ext.lower():
        print(f"{YELLOW}Warning: the output format '{output_path.suffix}' does not match the video format '{source_ext}'.{RESET}")

    base_url = build_base_url(video_format=media, video_source=source)

    fragment_size = source.partSize if source.partSize > 0 else FRAGMENT_SIZE
    total_segments = math.ceil(source.size / fragment_size)

    temp_dir = Path(tempfile.mkdtemp(prefix="abyss_download_"))

    key = Decryptor.generate_size_key(source.size)
    urls = []

    for index in range(total_segments):
        path = f"/{source_ext}/{video_metadata.md5_id}/{source.res_id}/{source.size}/{fragment_size}/{index}"
        token = Decryptor.encrypt_path(path, key)
        urls.append(f"{base_url}/sora/{source.size}/{token}")

    def download_segment(data):
        index, url = data
        file = temp_dir / f"segment_{index}"

        if file.exists():
            return True, index

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

                if response.status_code == 200:
                    file.write_bytes(response.content)
                    return True, index

                print(f"{YELLOW}Warning: segment {index} failed (HTTP {response.status_code}), retry {attempt}/{max_retries}{RESET}")

            except Exception as e:
                if attempt == max_retries:
                    return False, f"Segment {index}: {str(e)}"

                print(f"{YELLOW}Warning: segment {index} error, retry {attempt}/{max_retries}{RESET}")

        return False, index

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            tasks = [executor.submit(download_segment, item) for item in enumerate(urls)]
            iterator = as_completed(tasks)

            if not hide_progress:
                iterator = tqdm(iterator, total=len(tasks), desc="Downloading")

            for task in iterator:
                result = task.result()

                if not result[0]:
                    print("Failed task:", result)

        with open(output_path, "wb") as final:
            for index in range(total_segments):
                part = temp_dir / f"segment_{index}"

                if not part.exists():
                    raise MissingSegmentException(segment=index)

                with open(part, "rb") as file:
                    final.write(file.read())


        return True, str(output_path)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)