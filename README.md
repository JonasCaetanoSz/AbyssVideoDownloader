# Abyss Video Downloader

AbyssVideoDownloader is a Python library and command-line interface (CLI) that allows users to download Abyss.to videos, extract video metadata and thumbnails, and decrypt protected media data.

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
  - [Commands](#commands)
  - [Examples](#cli-examples)
- [Library Usage](#library-usage)
  - [Decryption](#decryption)
  - [Video Extraction](#video-extraction)
  - [Video Download](#video-download)
- [API Reference](#api-reference)
- [Exception Handling](#exception-handling)
- [Advanced Usage](#advanced-usage)

## 🚀 Installation

### From Source

```bash
git clone https://github.com/JonasCaetanoSz/AbyssVideoDownloader.git
cd AbyssVideoDownloader
pip install -e .
```

### From pip

```bash
 pip install git+https://github.com/JonasCaetanoSz/AbyssVideoDownloader.git
```

### Requirements

- Python 3.10+
- Dependencies listed in `pyproject.toml`

## ⚡ Quick Start

### CLI Quick Start

```bash
# Extract video slug
abyss get-video-slug -u "https://abysscdn.com/?v=K8R6OOjS7"

# Get video metadata
abyss get-video-metadata -u "https://abysscdn.com/?v=K8R6OOjS7"

# Download video
abyss download-video -u "https://abysscdn.com/?v=K8R6OOjS7" -r 720p -o my_video.mp4
```

### Library Quick Start

```python
from abyss_video_downloader import (
    metadata_extractor,
    download_video,
    Resolution
)

# Extract metadata
metadata = metadata_extractor("https://abysscdn.com/?v=K8R6OOjS7")

# Download video
success, output_path = download_video(
    video_metadata=metadata,
    resolution=Resolution("720p"),
    output="my_video.mp4"
)
```

## 🎯 CLI Usage

### Commands

#### 1. `get-video-slug` (Alias: `gs`)

Extracts the video slug from a video URL.

**Usage:**
```bash
abyss get-video-slug -u <VIDEO_URL>
abyss gs -u <VIDEO_URL>
```

**Arguments:**
- `-u, --url` (required): Video URL

**Example:**
```bash
abyss get-video-slug -u "https://abysscdn.com/?v=K8R6OOjS7"
# Output: K8R6OOjS7
```

---

#### 2. `get-video-thumbnail` (Alias: `gt`)

Extracts video thumbnail and sprite URLs.

**Usage:**
```bash
abyss get-video-thumbnail -u <VIDEO_URL> [-m MAX_SPRITES]
abyss gt -u <VIDEO_URL> [-m MAX_SPRITES]
```

**Arguments:**
- `-u, --url` (required): Video URL
- `-m, --max-sprites` (optional): Maximum number of sprites to retrieve

**Example:**
```bash
abyss get-video-thumbnail -u "https://abysscdn.com/?v=K8R6OOjS7" -m 5
# Output:
# thumbnail: https://cdn.example.com/thumbnail.jpg
# sprite [1]: https://cdn.example.com/sprite_1.jpg
# sprite [2]: https://cdn.example.com/sprite_2.jpg
# ...
```

**Note:** When accessing thumbnail URLs, include proper headers:
```bash
curl -H "User-Agent: Mozilla/5.0" -H "Referer: https://abysscdn.com/" "https://cdn.example.com/thumbnail.jpg"
```

---

#### 3. `get-video-metadata` (Alias: `gm`)

Extracts complete video metadata.

**Usage:**
```bash
abyss get-video-metadata -u <VIDEO_URL> [--json]
abyss gm -u <VIDEO_URL> [--json]
```

**Arguments:**
- `-u, --url` (required): Video URL
- `--json` (optional): Output metadata as formatted JSON

**Example:**
```bash
# Standard output
abyss get-video-metadata -u "https://abysscdn.com/?v=K8R6OOjS7"

# JSON output
abyss get-video-metadata -u "https://abysscdn.com/?v=K8R6OOjS7" --json
```

**Output (sample JSON):**
```json
{
  "user_id": 12345,
  "slug": "K8R6OOjS7",
  "md5_id": "abc123def456",
  "title": "Video Title",
  "duration": 3600,
  "media": {
    "mp4": {
      "sources": [
        {
          "label": "360p",
          "res_id": "360_res_id",
          "size": 52428800,
          "partSize": 2097152
        },
        {
          "label": "720p",
          "res_id": "720_res_id",
          "size": 209715200,
          "partSize": 2097152
        }
      ]
    }
  }
}
```

---

#### 4. `list-resolutions` (Alias: `lr`)

Lists all available resolutions for a video.

**Usage:**
```bash
abyss list-resolutions -u <VIDEO_URL>
abyss lr -u <VIDEO_URL>
```

**Arguments:**
- `-u, --url` (required): Video URL

**Example:**
```bash
abyss list-resolutions -u "https://abysscdn.com/?v=K8R6OOjS7"
# Output:
# Available resolutions:
# 
# mp4:
#   - 360p
#   - 720p
#   - 1080p
```

---

#### 5. `download-video` (Alias: `dl`)

Downloads a single video.

**Usage:**
```bash
abyss download-video -u <VIDEO_URL> [OPTIONS]
abyss dl -u <VIDEO_URL> [OPTIONS]
```

**Arguments:**
- `-u, --url` (required): Video URL
- `-o, --output` (optional): Output file name or directory
- `-r, --resolution` (optional, default: `360p`): Resolution to download (e.g., `360p`, `720p`, `1080p`)
- `-mw, --max-workers` (optional, default: `8`): Number of concurrent download threads
- `-hp, --hide-progress` (optional): Suppress progress bar
- `-mr, --max-retries` (optional, default: `3`): Maximum retry attempts per segment

**Examples:**
```bash
# Basic download with default resolution (360p)
abyss download-video -u "https://abysscdn.com/?v=K8R6OOjS7"

# Download with specific resolution
abyss download-video -u "https://abysscdn.com/?v=K8R6OOjS7" -r 720p

# Download with custom output name
abyss download-video -u "https://abysscdn.com/?v=K8R6OOjS7" -o ./videos/my_video.mp4

# Download to directory
abyss download-video -u "https://abysscdn.com/?v=K8R6OOjS7" -o ./videos/

# Advanced download with custom workers and retries
abyss download-video \
  -u "https://abysscdn.com/?v=K8R6OOjS7" \
  -r 1080p \
  -o my_video.mp4 \
  -mw 16 \
  -mr 5 \
  -hp
```

---

#### 6. `download-list` (Alias: `dlm`)

Downloads multiple videos from a file containing URLs (one URL per line).

**Usage:**
```bash
abyss download-list -f <FILE> [OPTIONS]
abyss dlm -f <FILE> [OPTIONS]
```

**Arguments:**
- `-f, --file` (required): File containing video URLs (one per line)
- `-o, --output` (optional): Output directory for all videos
- `-r, --resolution` (optional, default: `360p`): Resolution to download
- `-mw, --max-workers` (optional, default: `8`): Number of concurrent threads per video
- `-hp, --hide-progress` (optional): Suppress progress bar
- `-mr, --max-retries` (optional, default: `3`): Maximum retry attempts per segment

**Example:**

Create a file `urls.txt`:
```
https://abysscdn.com/?v=XXXXXX
https://abysscdn.com/?v=XXXXXX
https://abysscdn.com/?v=XXXXXX
```

Then run:
```bash
abyss download-list -f urls.txt -o ./videos/ -r 720p
```

This will download all videos to the `./videos/` directory with 720p resolution.

---

### CLI Examples

#### Example 1: Complete Workflow

```bash
# 1. Check available resolutions
abyss list-resolutions -u "https://abysscdn.com/?v=K8R6OOjS7"

# 2. Download video
abyss download-video -u "https://abysscdn.com/?v=K8R6OOjS7" -r 720p -o downloaded_video.mp4

# 3. Verify completion
ls -lh downloaded_video.mp4
```

#### Example 2: Batch Download with Retries

```bash
# Create a file with URLs
cat > videos.txt << EOF
https://abysscdn.com/?v=XXXXXX
https://abysscdn.com/?v=XXXXXX
https://abysscdn.com/?v=XXXXXX
EOF

# Download all with high retry count
abyss download-list -f videos.txt -o ./downloads -r 1080p -mw 16 -mr 10
```

#### Example 3: Get Metadata as JSON

```bash
# Save metadata to file
abyss get-video-metadata -u "https://abysscdn.com/?v=K8R6OOjS7" --json > metadata.json

# Use with jq for processing
cat metadata.json | jq '.title, .duration, .media | keys'
```

---

## 📚 Library Usage

### Basic Imports

```python
from abyss_video_downloader import (
    # Core functions
    slug_extractor,
    thumbnail_extractor,
    metadata_extractor,
    resolution_extractor,
    download_video,
    
    # Models
    VideoMetadata,
    VideoThumbnails,
    Resolution,
    ExpandedKey,
    EncryptedMedia,
    
    # Crypto
    Decryptor,
    
    # Utilities
    UrlValidator,
    build_base_url,
    get_version,
    print_banner,
    
    # Exceptions
    InvalidUrlException,
    VideoSourceNotFoundException,
    ResolutionNotAvailableException,
)
```

### Decryption

#### Decrypt Video Data

```python
from abyss_video_downloader import Decryptor, EncryptedMedia

# Create encrypted media object
encrypted_media = EncryptedMedia(
    user_id=12345,
    slug="video-slug",
    md5_id="abc123def456",
    title="Video Title",
    duration=3600,
    media="{encrypted_media_json_string}"  # Encrypted JSON string
)

# Decrypt the video data
video_metadata = Decryptor.decrypt_video_data(encrypted_media)

print(f"Title: {video_metadata.title}")
print(f"Duration: {video_metadata.duration}")
```

#### Generate Size Key

```python
from abyss_video_downloader import Decryptor

# Generate key for file size (used in segment download)
size_key = Decryptor.generate_size_key(209715200)
print(f"Size key: {size_key}")
```

#### Encrypt Path

```python
from abyss_video_downloader import Decryptor

# Encrypt download path for CDN access
path = "/mp4/video-id/resolution-id/209715200/2097152/0"
key = Decryptor.generate_size_key(209715200)
encrypted_token = Decryptor.encrypt_path(path, key)
print(f"Encrypted token: {encrypted_token}")
```

### Video Extraction

#### Extract Video Slug

```python
from abyss_video_downloader import slug_extractor

# Extract video identifier from URL
slug = slug_extractor(video_url="https://abysscdn.com/?v=K8R6OOjS7")
print(f"Video slug: {slug.value}")  # Output: K8R6OOjS7
```

#### Extract Video Thumbnail

```python
from abyss_video_downloader import thumbnail_extractor

# Get thumbnail and sprite URLs
thumbnails = thumbnail_extractor(
    video_url="https://abysscdn.com/?v=K8R6OOjS7",
    max_sprites=5  # Optional: limit number of sprites
)

print(f"Main thumbnail: {thumbnails.thumbnail}")
print(f"Number of sprites: {len(thumbnails.sprites)}")
for i, sprite_url in enumerate(thumbnails.sprites, 1):
    print(f"  Sprite {i}: {sprite_url}")

# Note: When requesting these URLs, include proper headers
import requests
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://abysscdn.com/"
}
response = requests.get(thumbnails.thumbnail, headers=headers)
```

#### Extract Video Metadata

```python
from abyss_video_downloader import metadata_extractor

# Get complete video metadata
metadata = metadata_extractor(video_url="https://abysscdn.com/?v=K8R6OOjS7")

print(f"Title: {metadata.title}")
print(f"Duration: {metadata.duration} seconds")
print(f"User ID: {metadata.user_id}")
print(f"MD5 ID: {metadata.md5_id}")

# Get available media formats
for format_type, media in metadata.media.items():
    print(f"\nFormat: {format_type}")
    for source in media.sources:
        print(f"  {source.label}: {source.size} bytes")
```

#### Extract Available Resolutions

```python
from abyss_video_downloader import metadata_extractor, resolution_extractor

# First get metadata
metadata = metadata_extractor(video_url="https://abysscdn.com/?v=K8R6OOjS7")

# Then extract available resolutions
resolutions = resolution_extractor(video_metadata=metadata)

for format_type, res_list in resolutions.items():
    print(f"{format_type}: {', '.join(res_list)}")
    # Output: mp4: 360p, 720p, 1080p
```

### Video Download

#### Basic Download

```python
from abyss_video_downloader import (
    metadata_extractor,
    download_video,
    Resolution
)

# Get video metadata
metadata = metadata_extractor(video_url="https://abysscdn.com/?v=K8R6OOjS7")

# Download video
success, output_path = download_video(
    video_metadata=metadata,
    resolution=Resolution("720p"),
    output="my_video.mp4"
)

if success:
    print(f"Download completed: {output_path}")
else:
    print("Download failed")
```

#### Advanced Download Configuration

```python
from abyss_video_downloader import (
    metadata_extractor,
    download_video,
    Resolution
)

metadata = metadata_extractor(video_url="https://abysscdn.com/?v=K8R6OOjS7")

success, output_path = download_video(
    video_metadata=metadata,
    resolution=Resolution("1080p"),
    output="./downloads/",  # Directory instead of filename
    max_workers=16,         # Increase concurrent downloads
    hide_progress=False,    # Show progress bar
    max_retries=5           # Retry failed segments more times
)

print(f"Downloaded to: {output_path}")
```

#### Download with Error Handling

```python
from abyss_video_downloader import (
    metadata_extractor,
    download_video,
    Resolution,
    ResolutionNotAvailableException,
    VideoSourceNotFoundException
)

url = "https://abysscdn.com/?v=K8R6OOjS7"

try:
    metadata = metadata_extractor(video_url=url)
    
    # Check available resolutions first
    if not metadata.has_resolution(video_ext="mp4", resolution=Resolution("1080p")):
        print("1080p not available, downloading 720p instead")
        target_resolution = Resolution("720p")
    else:
        target_resolution = Resolution("1080p")
    
    success, output_path = download_video(
        video_metadata=metadata,
        resolution=target_resolution,
        output="video.mp4"
    )
    
    if success:
        print(f"Success! Video saved to: {output_path}")
    
except ResolutionNotAvailableException as e:
    print(f"Resolution not available: {e}")
    
except VideoSourceNotFoundException as e:
    print(f"No video sources found: {e}")
    
except Exception as e:
    print(f"Error: {e}")
```

#### Batch Download

```python
from abyss_video_downloader import (
    metadata_extractor,
    download_video,
    Resolution
)
import os

video_urls = [
    "https://abysscdn.com/?v=XXXXXX",
    "https://abysscdn.com/?v=XXXXXX",
    "https://abysscdn.com/?v=XXXXXX",
]

output_dir = "./downloads"
os.makedirs(output_dir, exist_ok=True)

for idx, url in enumerate(video_urls, 1):
    try:
        print(f"\n[{idx}/{len(video_urls)}] Downloading: {url}")
        
        metadata = metadata_extractor(video_url=url)
        
        success, output_path = download_video(
            video_metadata=metadata,
            resolution=Resolution("720p"),
            output=output_dir,
            max_workers=8
        )
        
        if success:
            print(f"✓ Completed: {output_path}")
        else:
            print(f"✗ Failed: {url}")
            
    except Exception as e:
        print(f"✗ Error processing {url}: {e}")

print("\nBatch download completed!")
```

---

## 📖 API Reference

### Core Functions

#### `slug_extractor(video_url: str) -> Slug`

Extracts the video slug from a URL.

**Parameters:**
- `video_url` (str): The video URL

**Returns:**
- `Slug`: Object with `.value` property containing the slug

**Raises:**
- `InvalidUrlException`: If URL is invalid
- `InvalidSlugException`: If slug cannot be extracted

---

#### `thumbnail_extractor(video_url: str, max_sprites: int | None = None) -> VideoThumbnails`

Extracts thumbnail and sprite URLs.

**Parameters:**
- `video_url` (str): The video URL
- `max_sprites` (int, optional): Maximum number of sprites to retrieve

**Returns:**
- `VideoThumbnails`: Object with:
  - `.thumbnail`: Main thumbnail URL
  - `.sprites`: List of sprite URLs

**Raises:**
- `InvalidUrlException`: If URL is invalid
- `ThumbnailNotFoundException`: If thumbnails cannot be found

---

#### `metadata_extractor(video_url: str) -> VideoMetadata`

Extracts complete video metadata.

**Parameters:**
- `video_url` (str): The video URL

**Returns:**
- `VideoMetadata`: Object containing:
  - `user_id` (int): User ID
  - `slug` (str): Video slug
  - `md5_id` (str): MD5 identifier
  - `title` (str): Video title
  - `duration` (int): Duration in seconds
  - `media` (dict): Media sources for each format
  - `to_dict()`: Method to convert to dictionary
  - `has_resolution()`: Method to check resolution availability

**Raises:**
- `InvalidUrlException`: If URL is invalid
- `MetadataNotFoundException`: If metadata cannot be extracted

---

#### `resolution_extractor(video_metadata: VideoMetadata) -> dict[str, list[str]]`

Extracts available resolutions from metadata.

**Parameters:**
- `video_metadata` (VideoMetadata): Video metadata object

**Returns:**
- `dict`: Format -> List of available resolutions

---

#### `download_video(video_metadata: VideoMetadata, resolution: Resolution, output: str | None = None, max_workers: int = 8, hide_progress: bool = False, max_retries: int = 3) -> tuple[bool, str]`

Downloads a video with specified resolution.

**Parameters:**
- `video_metadata` (VideoMetadata): Video metadata
- `resolution` (Resolution): Target resolution
- `output` (str, optional): Output file path or directory
- `max_workers` (int, default: 8): Concurrent download threads
- `hide_progress` (bool, default: False): Hide progress bar
- `max_retries` (int, default: 3): Retry attempts per segment

**Returns:**
- `tuple[bool, str]`: (success, output_path)

**Raises:**
- `VideoSourceNotFoundException`: If no video sources available
- `ResolutionNotAvailableException`: If resolution not available
- `MissingSegmentException`: If segment download fails after retries

---

### Models

#### `VideoMetadata`

```python
@dataclass
class VideoMetadata:
    user_id: int
    slug: str
    md5_id: str
    title: str
    duration: int
    media: dict[str, VideoMedia]
    
    def to_dict(self) -> dict: ...
    def has_resolution(self, video_ext: str, resolution: 'Resolution') -> bool: ...
```

#### `Resolution`

```python
@dataclass
class Resolution:
    value: str  # e.g., "720p", "1080p"
```

#### `VideoThumbnails`

```python
@dataclass
class VideoThumbnails:
    thumbnail: str        # Main thumbnail URL
    sprites: list[str]    # Sprite URLs
```

#### `Decryptor`

Static methods for encryption/decryption:
- `decrypt_video_data(encrypted_video_data: EncryptedMedia) -> VideoMetadata`
- `expandKey(video_data: EncryptedMedia) -> ExpandedKey`
- `decrypt_string_media(media: str, expanded_key: ExpandedKey) -> str`
- `generate_size_key(size: int) -> str`
- `encrypt_path(path_str: str, key_hex: str) -> str`

---

## ⚠️ Exception Handling

All exceptions inherit from a base exception class and can be caught accordingly:

```python
from abyss_video_downloader import (
    InvalidSlugException,
    InvalidUrlException,
    ThumbnailNotFoundException,
    MetadataNotFoundException,
    VideoSourceNotFoundException,
    ResolutionNotAvailableException,
    DomainNotFoundException,
    MissingSegmentException
)

try:
    metadata = metadata_extractor(video_url=url)
    success, path = download_video(metadata=metadata, resolution=Resolution("720p"))
    
except InvalidUrlException as e:
    print(f"URL is invalid: {e}")
except MetadataNotFoundException as e:
    print(f"Could not extract metadata: {e}")
except ResolutionNotAvailableException as e:
    print(f"Resolution not available: {e}")
except VideoSourceNotFoundException as e:
    print(f"No video sources found: {e}")
except MissingSegmentException as e:
    print(f"Download failed - missing segment: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 🔧 Advanced Usage

### Custom Download with Progress Tracking

```python
from abyss_video_downloader import metadata_extractor, download_video, Resolution
import sys

def download_with_custom_tracking(url, resolution, output=None):
    """Download with custom progress tracking"""
    try:
        print(f"Fetching metadata for: {url}")
        metadata = metadata_extractor(video_url=url)
        print(f"✓ Got metadata: {metadata.title}")
        
        print(f"Starting download at {resolution.value}...")
        success, output_path = download_video(
            video_metadata=metadata,
            resolution=resolution,
            output=output,
            max_workers=12,
            hide_progress=False,
            max_retries=5
        )
        
        if success:
            print(f"✓ Download completed: {output_path}")
            return output_path
        else:
            print("✗ Download failed")
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return None

# Usage
download_with_custom_tracking(
    "https://abysscdn.com/?v=K8R6OOjS7",
    Resolution("1080p"),
    "./videos/my_video.mp4"
)
```

### Using the Library in a Web Application

```python
from abyss_video_downloader import metadata_extractor, Resolution
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/video/info/<url>')
def get_video_info(url):
    """API endpoint to get video information"""
    try:
        metadata = metadata_extractor(video_url=url)
        return jsonify({
            'status': 'success',
            'title': metadata.title,
            'duration': metadata.duration,
            'formats': {
                fmt: [s.label for s in sources.sources]
                for fmt, sources in metadata.media.items()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/video/resolutions/<url>')
def get_resolutions(url):
    """API endpoint to get available resolutions"""
    try:
        from abyss_video_downloader import resolution_extractor
        metadata = metadata_extractor(video_url=url)
        resolutions = resolution_extractor(video_metadata=metadata)
        return jsonify({
            'status': 'success',
            'resolutions': resolutions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
```

---

## 📝 Notes

- **Headers Required:** When requesting thumbnail or sprite URLs, always include:
  ```python
  headers = {
      "User-Agent": "Mozilla/5.0",
      "Referer": "https://abysscdn.com/"
  }
  ```

- **Rate Limiting:** Be respectful of server resources when batch downloading

- **Segment Size:** Default segment size is 2MB (2097152 bytes). This can vary per video.

- **Temporary Files:** Download segments are stored in temporary directories and cleaned up automatically after completion

- **Encryption:** Video metadata is encrypted using AES-CTR mode. The library handles decryption automatically.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Made with ❤️ by JonasCaetanoSz**
