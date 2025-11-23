import cv2
import time
from camera_capture import CameraCapture
from stream_capture import StreamCapture
from coin_processing import CoinProcessor
from stream_picker import get_stream_source

def main():
    print("Coin Detector")
    print("=" * 50)
    
    # Get stream source (set mode"camera/vdo_ninja",source"index/id" to bypass prompt)
    mode, source = get_stream_source()
    
    if not mode or source is None:
        print("No stream source selected.")
        return
    
    # Setup capture
    if mode == 'camera':
        stream = CameraCapture(camera_index=source)
    elif mode == 'vdo_ninja':
        stream = StreamCapture(view_id=source)
    else:
        print(f"Unknown mode: {mode}")
        return
    
    processor = CoinProcessor(blur=15, show_contours=False)
    
    try:
        stream.start()
        print("\nPress 'q' to quit, 's' to save snapshot, 'c' to toggle contours\n")
                
        while True:
            frame = stream.get_frame()
            if frame is None:
                break
            
            # Process frame to detect coins
            coins, processed = processor.detect_coins(frame)
            # Add overlay with coin count
            processor.add_info_overlay(processed, len(coins))
            
            cv2.imshow('Coin Detector', processed)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                processor.show_contours = not processor.show_contours
            elif key == ord('s'):
                cv2.imwrite('coin_snapshot.jpg', processed)
                print("Snapshot saved")
            
            time.sleep(0.033)
        
    except Exception as e:
        print(f"\nError: {e}")
        
    finally:
        # Cleanup
        stream.stop()
        cv2.destroyAllWindows()
        print("Coin detector closed")

if __name__ == "__main__":
    main()
