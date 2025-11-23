# Coin Counter

Real-time coin detection using OpenCV. Works with webcams, USB cameras, or VDO.Ninja streams.

## What it does

Detects circular coins in a video feed and counts them in real-time. Uses contour detection with circularity filtering to identify coins and draws bounding boxes around them.

## How I built it

The basic coin detection approach was inspired by [this YouTube tutorial](https://www.youtube.com/watch?v=XZ3PNnA9NbU), though I adapted the code for my specific use case with streaming support and different detection parameters.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

You'll be prompted to choose between:
- Local camera (webcam/USB camera)
- VDO.Ninja remote stream


### Keyboard controls
- `q` - quit
- `s` - save snapshot
- `c` - toggle contour visualization

### Preset configuration

Skip the prompts by editing `main.py`:
```python
# For camera
mode, source = get_stream_source(mode='camera', source=0)

# For VDO.Ninja
mode, source = get_stream_source(mode='vdo_ninja', source='your_stream_id')
```

## Project structure

```
main.py              - Main application
stream_picker.py     - Interactive source selection
camera_capture.py    - Webcam/USB camera handler
stream_capture.py    - VDO.Ninja stream handler (auto-play, hidden browser)
coin_processing.py   - Coin detection algorithm
coin_count_test.py   - Static image testing
```

## How it works

1. **Preprocessing**: Convert to grayscale → Gaussian blur → Otsu's threshold
2. **Detection**: Find contours and filter by circularity (4πA/P²)
3. **Filtering**: Only keep shapes with circularity > 0.7 and area > 100px
4. **Display**: Draw bounding boxes and show coin count

### Detection parameters

Edit `coin_processing.py` or pass to the processor:
```python
processor = CoinProcessor(
    blur=15,              # Gaussian blur strength
    show_contours=False   # Show all detected contours
)
```

Circularity threshold: `0.7` (adjust in `coin_processing.py`)  
Minimum area: `100` pixels

## VDO.Ninja features

The stream capture automatically:
- Opens Chrome in hidden mode (off-screen window)
- Clicks the play button
- Captures frames at ~30fps

## Troubleshooting

**VDO.Ninja not playing**: Increase wait time in `stream_capture.py`

**False detections**: Increase circularity threshold or minimum area

**Missing coins**: Decrease thresholds, increase blur, or improve lighting

**Slow performance**: Lower frame rate (increase sleep time in main loop)

