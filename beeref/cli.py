import argparse
import sys
import base64
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice

from beeref.view import BeeGraphicsView
from beeref.scene import BeeGraphicsScene  
from beeref.items import BeePixmapItem

class BeeRefCLI:
    def __init__(self):
        self.app = None
        self.main_window = None
    
    def ensure_app(self):
        """Initialize Qt application if needed"""
        if not self.app:
            self.app = QApplication(sys.argv if sys.argv else ['beeref-cli'])
            self.main_window = BeeGraphicsView()
            self.scene = BeeGraphicsScene()
            self.main_window.setScene(self.scene)
            
    def add_image_from_stdin(self):
        """Read base64 image data from stdin and add to BeeRef"""
        try:
            # Read all stdin data
            input_data = sys.stdin.buffer.read()
            
            # Try to decode as base64 first
            try:
                if input_data.startswith(b'data:image'):
                    # Remove data URL prefix
                    input_data = input_data.split(b',')[1]
                image_bytes = base64.b64decode(input_data)
            except:
                # If not base64, treat as raw image data
                image_bytes = input_data
            
            self.ensure_app()
            
            # Create QPixmap from bytes
            pixmap = QPixmap()
            if not pixmap.loadFromData(image_bytes):
                raise ValueError("Invalid image data")
            
            # Add to scene
            item = BeePixmapItem(pixmap)
            self.scene.addItem(item)
            self.scene.arrange_items()
            
            # Show window
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
            
            return True
            
        except Exception as e:
            print(f"Error adding image from stdin: {e}", file=sys.stderr)
            return False
    
    def add_image_from_file(self, filepath):
        """Add image file to BeeRef"""
        try:
            path = Path(filepath)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
                
            self.ensure_app()
            
            # Load image
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                raise ValueError(f"Cannot load image: {filepath}")
            
            # Add to scene
            item = BeePixmapItem(pixmap)
            self.scene.addItem(item)
            self.scene.arrange_items()
            
            # Show window
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
            
            return True
            
        except Exception as e:
            print(f"Error adding image from file: {e}", file=sys.stderr)
            return False

def cli_main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='BeeRef CLI Interface')
    parser.add_argument('--add-from-stdin', action='store_true',
                       help='Add image from stdin (base64 or raw bytes)')
    parser.add_argument('--add-file', type=str, metavar='PATH',
                       help='Add image from file path')
    parser.add_argument('--show', action='store_true',
                       help='Show BeeRef window')
    
    args = parser.parse_args()
    
    if not any([args.add_from_stdin, args.add_file, args.show]):
        parser.print_help()
        return 1
    
    cli = BeeRefCLI()
    success = True
    
    if args.add_from_stdin:
        success = cli.add_image_from_stdin()
    
    if args.add_file and success:
        success = cli.add_image_from_file(args.add_file)
    
    if args.show and success:
        cli.ensure_app()
        cli.main_window.show()
    
    # Start Qt event loop if window is shown
    if cli.app and cli.main_window and cli.main_window.isVisible():
        return cli.app.exec()
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(cli_main())
