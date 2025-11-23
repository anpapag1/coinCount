from pyusbcameraindex import enumerate_usb_video_devices_windows

def pick_camera():
    """Pick a camera from the list of connected USB cameras"""
    devices = enumerate_usb_video_devices_windows()
    if not devices:
        print("No USB video devices found.")
        return None

    print("Available USB Video Devices:")
    for device in devices:
        print(f"{device.index}: {device.name}")

    while True:
        try:
            choice = int(input("Select a camera by index (or -1 to exit): "))
            if choice == -1:
                return None
            for device in devices:
                if device.index == choice:
                    return choice
            print("Invalid index. Please try again.")
        except ValueError:
            print("Please enter a valid integer.")
            
def start(preset=False, mode=None, cam_index=None):
    """Start the camera picker"""
    if preset:
        if mode == 'camera':
            return cam_index
        if mode == 'vdo ninja':
            return cam_index
    else:
        print("Streaming sources: \n1. camera\n2. vdo ninja")
        choice = input("Select a streaming source (or -1 to exit): ")
        if choice == '1':
            return pick_camera()
        elif choice == '2':
            view_id = input("Enter VDO.Ninja vi1ew ID: ")
            return view_id
        else:
            print("Invalid choice.")
            return None
    
if __name__ == "__main__":
    camera_index = start()
    if camera_index is not None:
        print(f"Selected camera index: {camera_index}")
    else:
        print("No camera selected.")