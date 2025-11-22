# Coin Counter

A real-time coin detection system that works with both static images and live video streams.

## Features

- **Real-time coin detection** from VDO.Ninja video streams
- **Static image analysis** with contour-based circular detection
- **Multiple detection methods**: HoughCircles and contour circularity
- **Visual feedback** with bounding boxes and coin count overlay
- **Snapshot capture** during live streaming

## Project Structure

```
coinCount/
├── main.py                 # Main application for stream-based detection
├── stream_capture.py       # VDO.Ninja stream capture using Selenium
├── coin_processing.py      # HoughCircles-based coin detection
├── coin_count_test.py      # Static image testing with contour detection
└── coin_test/              # Test images directory
```

## Requirements

```bash
pip install opencv-python numpy selenium webdriver-manager pillow
```

## Usage

### Live Stream Detection

Run the main application to detect coins from a live VDO.Ninja stream:

```bash
python main.py
```

**Controls:**
- Press `q` to quit
- Press `s` to save a snapshot

### Static Image Testing

Test coin detection on static images:

```bash
python coin_count_test.py
```

## Detection Methods

### 1. HoughCircles Method (`coin_processing.py`)
- Uses OpenCV's HoughCircles algorithm
- Best for clean, well-separated coins
- Adjustable parameters: `min_dist`, `min_radius`, `max_radius`

### 2. Contour Circularity Method (`coin_count_test.py`)
- Detects contours and filters by circularity formula: **4πA/P²**
- More flexible for various lighting conditions
- Circularity threshold: 0.7 (adjustable)

## Configuration

### Stream Settings
Edit `main.py` to change the VDO.Ninja stream ID:
```python
VIEW_ID = "your_stream_id"
```

### Detection Parameters

**HoughCircles (coin_processing.py):**
```python
processor = CoinProcessor(
    min_dist=80,      # Minimum distance between coins
    min_radius=15,    # Minimum coin radius
    max_radius=80     # Maximum coin radius
)
```

**Contour Method (coin_count_test.py):**
```python
circularity_threshold = 0.7  # 0.0-1.0 (1.0 = perfect circle)
min_area = 100               # Minimum contour area
```

## How It Works

1. **Image Preprocessing**: Grayscale conversion → Gaussian blur → Thresholding
2. **Feature Detection**: Circle/contour detection with filtering
3. **Visualization**: Bounding boxes, circles, and coin count overlay
4. **Real-time Processing**: ~30 FPS for live streams

## Troubleshooting

- **Stream not loading**: Check VDO.Ninja VIEW_ID and internet connection
- **False detections**: Adjust circularity threshold or HoughCircles parameters
- **Missing coins**: Increase blur kernel size or adjust threshold values
- **Performance issues**: Reduce frame processing rate in `main.py`

## License

MIT
