from pyusbcameraindex import enumerate_usb_video_devices_windows




def pick_camera():
    devices = enumerate_usb_video_devices_windows()
    if not devices:
        print("No cameras found")
        return None

    print("\nAvailable cameras:")
    for dev in devices:
        print(f"  {dev.index}: {dev.name}")

    while True:
        try:
            idx = int(input("\nSelect camera (-1 to cancel): "))
            if idx == -1:
                return None
            if any(d.index == idx for d in devices):
                return idx
            print("Invalid index")
        except ValueError:
            print("Enter a number")


def get_stream_source(mode=None, source=None):
    # Use preset if both provided
    if mode and source is not None:
        print(f"Using: {mode} - {source}")
        return mode, source
    
    # Prompt for source if only mode provided
    if mode:
        if mode == 'camera':
            return 'camera', pick_camera()
        elif mode == 'vdo_ninja':
            vid = input("VDO.Ninja ID: ").strip()
            return 'vdo_ninja', vid if vid else None
        return None, None
    
    # Full prompt
    print("SELECT SOURCE")
    print("="*50)
    print("1. Camera")
    print("2. VDO.Ninja\n")
    
    while True:
        choice = input("Choose (1/2, -1 to exit): ").strip()
        
        if choice == '-1':
            return None, None
        elif choice == '1':
            idx = pick_camera()
            return ('camera', idx) if idx is not None else (None, None)
        elif choice == '2':
            vid = input("\nVDO.Ninja ID: ").strip()
            return ('vdo_ninja', vid) if vid else (None, None)
        else:
            print("Enter 1 or 2")


if __name__ == "__main__":
    # Test the stream picker
    mode, source = get_stream_source()
    
    if mode and source is not None:
        print(f"\n Selected: {mode} - {source}")
    else:
        print("\n No source selected")
