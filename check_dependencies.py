import sys
import importlib.util
import warnings

def check_tgcrypto():
    """Check if TgCrypto is installed and warn Windows users if it's missing."""
    tgcrypto_installed = importlib.util.find_spec("tgcrypto") is not None
    
    if not tgcrypto_installed and sys.platform == "win32":
        warnings.warn(
            "\n"
            "TgCrypto is not installed. Your application will work but may be slower.\n"
            "For better performance, install TgCrypto using a pre-compiled wheel:\n"
            "1. Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#tgcrypto\n"
            "2. Install with: pip install path\\to\\downloaded\\wheel\\file.whl\n",
            UserWarning
        )
    
    return tgcrypto_installed

if __name__ == "__main__":
    # This can be run directly to check dependencies
    is_installed = check_tgcrypto()
    print(f"TgCrypto installed: {is_installed}")
