import cv2
import time
from stream_capture import StreamCapture
from coin_processing import CoinProcessor

# VDO.Ninja stream ID
VIEW_ID = "Tk89sNbS"

def main():
    print("VDO.Ninja Coin Detector")
    print("=" * 50)
    
    # Initialize stream capture
    stream = StreamCapture(VIEW_ID)
    
    # Initialize coin processor
    processor = CoinProcessor(
        min_dist=80,
        min_radius=15,
        max_radius=80
    )
    
    try:
        # Start the stream
        stream.start(wait_time=5)
        
        print("\nStream loaded! Press 'q' to quit, 's' to save snapshot")
        print("Detecting coins...\n")
                
        while True:
            # Get frame from stream
            frame = stream.get_frame()
            
            if frame is None:
                print("Failed to get frame")
                break
                        
            # Process frame to detect coins
            coins, processed_frame = processor.detect_coins(frame)
            
            # Add info overlay
            processor.add_info_overlay(processed_frame, len(coins))
            
            # Display the processed frame
            cv2.imshow('Coin Detector', processed_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('s'):
                filename = f'coin_snapshot.jpg'
                cv2.imwrite(filename, processed_frame)
                print(f"Snapshot saved: {filename}")
            
            # Small delay to control frame rate
            time.sleep(0.033)  # ~30 fps
        
    except Exception as e:
        print(f"\nError: {e}")
        
    finally:
        # Cleanup
        stream.stop()
        cv2.destroyAllWindows()
        print("Coin detector closed")

if __name__ == "__main__":
    main()
