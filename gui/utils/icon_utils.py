"""
Utility functions for handling Material Design icons.
"""
import os
import io
import base64
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Try to import cairosvg, but don't fail if it's not available
try:
    import cairosvg
    CAIROSVG_AVAILABLE = True
except (ImportError, OSError):
    CAIROSVG_AVAILABLE = False
    print("Warning: cairosvg is not available. Using fallback for icons.")

# Directory for storing icons
ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")

# Create the icons directory if it doesn't exist
os.makedirs(ICONS_DIR, exist_ok=True)

# Material Design Icons in SVG format
MATERIAL_ICONS = {
    # File operations
    "open": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h240l80 80h280q33 0 56.5 23.5T880-680v480q0 33-23.5 56.5T800-120H200Zm0-80h600v-480H200v480Zm0 0v-560 560Z"/></svg>""",
    "save": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M840-680v480q0 33-23.5 56.5T760-120H200q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h480l160 160Zm-80 34L646-760H200v560h560v-446ZM480-240q33 0 56.5-23.5T560-320v-120q0-33-23.5-56.5T480-520q-33 0-56.5 23.5T400-440v120q0 33 23.5 56.5T480-240ZM240-640h360v-80H240v80Zm-40-120v560-560Z"/></svg>""",
    "save_as": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M840-680v480q0 33-23.5 56.5T760-120H200q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h480l160 160Zm-80 34L646-760H200v560h560v-446ZM480-240q33 0 56.5-23.5T560-320v-120q0-33-23.5-56.5T480-520q-33 0-56.5 23.5T400-440v120q0 33 23.5 56.5T480-240ZM240-640h360v-80H240v80Zm-40-120v560-560Z"/></svg>""",
    "print": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M640-640v-120H320v120h-80v-200h480v200h-80Zm-480 80h640-640Zm560 100q17 0 28.5-11.5T760-500q0-17-11.5-28.5T720-540q-17 0-28.5 11.5T680-500q0 17 11.5 28.5T720-460ZM320-160h320v-200H320v200Zm400-80v120H240v-120h-80v-240q0-33 23.5-56.5T240-680h480q33 0 56.5 23.5T800-600v240h-80Zm80-240H160h640Z"/></svg>""",
    "exit": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z"/></svg>""",
    
    # Export operations
    "image": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm40-80h480L570-480 450-320l-90-120-120 160Zm-40 80v-560 560Z"/></svg>""",
    "text": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M320-240h320v-80H320v80Zm0-160h320v-80H320v80Zm0-160h320v-80H320v80ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0 0v-560 560Z"/></svg>""",
    
    # Edit operations
    "extract_text": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M320-240h320v-80H320v80Zm0-160h320v-80H320v80Zm0-160h320v-80H320v80ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0 0v-560 560Z"/></svg>""",
    "add_text": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-240q17 0 28.5-11.5T520-280v-160h160q17 0 28.5-11.5T720-480q0-17-11.5-28.5T680-520H520v-160q0-17-11.5-28.5T480-720q-17 0-28.5 11.5T440-680v160H280q-17 0-28.5 11.5T240-480q0 17 11.5 28.5T280-440h160v160q0 17 11.5 28.5T480-240ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0 0v-560 560Z"/></svg>""",
    "highlight": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M240-160h120v-120h-80v-80h-40v200Zm360 0h120v-200h-40v80h-80v120Zm-280-480h320v-160H320v160Zm-80 280h480v-200H240v200ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0 0v-560 560Z"/></svg>""",
    "note": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M240-400h360v-80H240v80Zm0-120h360v-80H240v80Zm0-120h360v-80H240v80ZM880-80 720-240H160q-33 0-56.5-23.5T80-320v-480q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v720ZM160-320h594l46 45v-525H160v480Zm0 0v-480 480Z"/></svg>""",
    "draw": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm40-80h480L570-480 450-320l-90-120-120 160Zm-40 80v-560 560Z"/></svg>""",
    "delete": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>""",
    
    # Navigation icons
    "navigate_before": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M560-240 320-480l240-240 56 56-184 184 184 184-56 56Z"/></svg>""",
    "navigate_next": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M504-480 320-664l56-56 240 240-240 240-56-56 184-184Z"/></svg>""",
    
    # Page operations
    "add_page": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-240q17 0 28.5-11.5T520-280v-160h160q17 0 28.5-11.5T720-480q0-17-11.5-28.5T680-520H520v-160q0-17-11.5-28.5T480-720q-17 0-28.5 11.5T440-680v160H280q-17 0-28.5 11.5T240-480q0 17 11.5 28.5T280-440h160v160q0 17 11.5 28.5T480-240ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0 0v-560 560Z"/></svg>""",
    "delete_page": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>""",
    "extract_page": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-320 280-520l56-58 104 104v-246h80v246l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-560q0-33 23.5-56.5T240-880h320l240 240v400q0 33-23.5 56.5T720-160H240Zm280-560v-160H240v560h480v-400H520ZM240-800v160-160 560-560Z"/></svg>""",
    "rotate": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-160q-133 0-226.5-93.5T160-480q0-133 93.5-226.5T480-800q85 0 149 34.5T740-671v-129h80v280H540v-80h168q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q77 0 139-44t87-116h84q-28 106-114 173t-196 67Z"/></svg>""",
    "split": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M120-240v-480h720v480H120Zm80-80h240v-320H200v320Zm320 0h240v-320H520v320Z"/></svg>""",
    "merge": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M120-120v-720h720v720H120Zm80-80h560v-560H200v560Zm280-40q50 0 85-35t35-85q0-50-35-80t-105-30q-36 0-68.5 13T354-699l40 40q17-12 37.5-21.5T480-690q40 0 60 18t20 42q0 20-9 36.5T526-560q-25 24-40.5 39T456-485q-6 11-11 25.5t-5 19.5Z"/></svg>""",
    
    # View operations
    "zoom_in": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M440-440H320q-17 0-28.5-11.5T280-480q0-17 11.5-28.5T320-520h120v-120q0-17 11.5-28.5T480-680q17 0 28.5 11.5T520-640v120h120q17 0 28.5 11.5T680-480q0 17-11.5 28.5T640-440H520v120q0 17-11.5 28.5T480-280q-17 0-28.5-11.5T440-320v-120Zm40 320q-117 0-198.5-81.5T200-400q0-117 81.5-198.5T480-680q117 0 198.5 81.5T760-400q0 117-81.5 198.5T480-120Zm0-80q83 0 141.5-58.5T680-400q0-83-58.5-141.5T480-600q-83 0-141.5 58.5T280-400q0 83 58.5 141.5T480-200Zm0-200Z"/></svg>""",
    "zoom_out": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M320-440q-17 0-28.5-11.5T280-480q0-17 11.5-28.5T320-520h320q17 0 28.5 11.5T680-480q0 17-11.5 28.5T640-440H320Zm160 320q-117 0-198.5-81.5T200-400q0-117 81.5-198.5T480-680q117 0 198.5 81.5T760-400q0 117-81.5 198.5T480-120Zm0-80q83 0 141.5-58.5T680-400q0-83-58.5-141.5T480-600q-83 0-141.5 58.5T280-400q0 83 58.5 141.5T480-200Zm0-200Z"/></svg>""",
    "reset": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-160q-133 0-226.5-93.5T160-480q0-133 93.5-226.5T480-800q85 0 149 34.5T740-671v-129h80v280H540v-80h168q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q77 0 139-44t87-116h84q-28 106-114 173t-196 67Z"/></svg>""",
    "fullscreen": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M120-120v-240h80v160h160v80H120Zm480 0v-80h160v-160h80v240H600ZM120-600v-240h240v80H200v160h-80Zm640 0v-160H600v-80h240v240h-80Z"/></svg>""",
    "fullscreen_exit": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M240-240v-160h80v80h80v160H240Zm320 0v-80h80v-80h80v160H560ZM240-560v-160h160v80h-80v80h-80Zm400 0v-80h-80v-80h160v160h-80Z"/></svg>""",
    
    # Help operations
    "help": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Zm0 160q17 0 28.5-11.5T520-360q0-17-11.5-28.5T480-400q-17 0-28.5 11.5T440-360q0 17 11.5 28.5T480-320ZM440-440h80q0-17 1.5-30t8.5-25q7-12 19.5-25.5T580-550q20-20 30-40t10-50q0-50-35-80t-105-30q-36 0-68.5 13T354-699l40 40q17-12 37.5-21.5T480-690q40 0 60 18t20 42q0 20-9 36.5T526-560q-25 24-40.5 39T456-485q-6 11-11 25.5t-5 19.5Z"/></svg>""",
    "info": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M440-280h80v-240h-80v240Zm40-320q17 0 28.5-11.5T520-640q0-17-11.5-28.5T480-680q-17 0-28.5 11.5T440-640q0 17 11.5 28.5T480-600Zm0 520q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>""",
    "contact": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm320-280L160-640v400h640v-400L480-440Zm0-80 320-200H160l320 200ZM160-640v-80 480-400Z"/></svg>""",
    "bug": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-80q-83 0-141.5-58.5T280-280q0-85 57.5-142.5T480-480q85 0 142.5 57.5T680-280q0 83-58.5 141.5T480-80Zm0-80q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35ZM240-720q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35Zm480 0q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35ZM480-440q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35Z"/></svg>""",
    "about": """<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Zm-40 120h80v-240h-80v240Zm40-280q17 0 28.5-11.5T520-680q0-17-11.5-28.5T480-720q-17 0-28.5 11.5T440-680q0 17 11.5 28.5T480-640Z"/></svg>"""
}

def load_svg_icon(icon_name, size=24, color="#000000"):
    """
    Load an SVG icon and convert it to a PhotoImage.
    
    Args:
        icon_name (str): Name of the icon to load
        size (int): Size of the icon in pixels
        color (str): Color of the icon in hex format
        
    Returns:
        PhotoImage: The icon as a PhotoImage
    """
    if icon_name not in MATERIAL_ICONS:
        raise ValueError(f"Icon {icon_name} not found")
    
    # Replace the color in the SVG
    svg_data = MATERIAL_ICONS[icon_name].replace('path d="', f'path fill="{color}" d="')
    
    # Check if we have cairosvg available
    if CAIROSVG_AVAILABLE:
        try:
            # Convert SVG to PNG using cairosvg
            png_data = cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), 
                                        output_width=size, 
                                        output_height=size)
            
            # Create a PIL image from the PNG data
            image = Image.open(io.BytesIO(png_data))
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error converting SVG to PNG: {e}")
            # Fall through to fallback
    
    # Fallback: Create a simple icon based on the icon name
    image = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple shape based on the icon name
    if "navigate_before" in icon_name:
        # Left arrow
        draw.polygon([(size*0.7, size*0.2), (size*0.3, size*0.5), (size*0.7, size*0.8)], fill=color)
    elif "navigate_next" in icon_name:
        # Right arrow
        draw.polygon([(size*0.3, size*0.2), (size*0.7, size*0.5), (size*0.3, size*0.8)], fill=color)
    elif "add" in icon_name:
        # Plus sign
        draw.rectangle([size*0.4, size*0.2, size*0.6, size*0.8], fill=color)
        draw.rectangle([size*0.2, size*0.4, size*0.8, size*0.6], fill=color)
    elif "delete" in icon_name:
        # X mark
        draw.line([(size*0.2, size*0.2), (size*0.8, size*0.8)], fill=color, width=int(size*0.1))
        draw.line([(size*0.2, size*0.8), (size*0.8, size*0.2)], fill=color, width=int(size*0.1))
    elif "zoom_in" in icon_name:
        # Magnifying glass with plus
        draw.ellipse([size*0.2, size*0.2, size*0.7, size*0.7], outline=color, width=int(size*0.1))
        draw.line([(size*0.6, size*0.6), (size*0.8, size*0.8)], fill=color, width=int(size*0.1))
        draw.line([(size*0.35, size*0.45), (size*0.55, size*0.45)], fill=color, width=int(size*0.1))
        draw.line([(size*0.45, size*0.35), (size*0.45, size*0.55)], fill=color, width=int(size*0.1))
    elif "zoom_out" in icon_name:
        # Magnifying glass with minus
        draw.ellipse([size*0.2, size*0.2, size*0.7, size*0.7], outline=color, width=int(size*0.1))
        draw.line([(size*0.6, size*0.6), (size*0.8, size*0.8)], fill=color, width=int(size*0.1))
        draw.line([(size*0.35, size*0.45), (size*0.55, size*0.45)], fill=color, width=int(size*0.1))
    elif "fullscreen" in icon_name:
        # Expand arrows
        draw.line([(size*0.2, size*0.2), (size*0.4, size*0.2)], fill=color, width=int(size*0.1))
        draw.line([(size*0.2, size*0.2), (size*0.2, size*0.4)], fill=color, width=int(size*0.1))
        draw.line([(size*0.8, size*0.2), (size*0.6, size*0.2)], fill=color, width=int(size*0.1))
        draw.line([(size*0.8, size*0.2), (size*0.8, size*0.4)], fill=color, width=int(size*0.1))
        draw.line([(size*0.2, size*0.8), (size*0.4, size*0.8)], fill=color, width=int(size*0.1))
        draw.line([(size*0.2, size*0.8), (size*0.2, size*0.6)], fill=color, width=int(size*0.1))
        draw.line([(size*0.8, size*0.8), (size*0.6, size*0.8)], fill=color, width=int(size*0.1))
        draw.line([(size*0.8, size*0.8), (size*0.8, size*0.6)], fill=color, width=int(size*0.1))
    elif "text" in icon_name or "extract_text" in icon_name:
        # Text lines
        draw.line([(size*0.2, size*0.3), (size*0.8, size*0.3)], fill=color, width=int(size*0.1))
        draw.line([(size*0.2, size*0.5), (size*0.8, size*0.5)], fill=color, width=int(size*0.1))
        draw.line([(size*0.2, size*0.7), (size*0.8, size*0.7)], fill=color, width=int(size*0.1))
    elif "rotate" in icon_name:
        # Rotate arrow
        draw.arc([size*0.2, size*0.2, size*0.8, size*0.8], 0, 270, fill=color, width=int(size*0.1))
        draw.polygon([(size*0.8, size*0.5), (size*0.7, size*0.3), (size*0.9, size*0.3)], fill=color)
    elif "image" in icon_name:
        # Image frame
        draw.rectangle([size*0.2, size*0.2, size*0.8, size*0.8], outline=color, width=int(size*0.1))
        draw.polygon([(size*0.3, size*0.7), (size*0.4, size*0.6), (size*0.5, size*0.7), (size*0.7, size*0.5), (size*0.7, size*0.7), (size*0.3, size*0.7)], fill=color)
    elif "help" in icon_name:
        # Question mark
        draw.ellipse([size*0.2, size*0.2, size*0.8, size*0.8], outline=color, width=int(size*0.1))
        # Use a default font for the question mark
        try:
            font = ImageFont.load_default()
            draw.text((size*0.45, size*0.3), "?", fill=color, font=font)
        except Exception:
            # If there's an issue with the font, just draw a circle
            draw.ellipse([size*0.45, size*0.45, size*0.55, size*0.55], fill=color)
    elif "info" in icon_name:
        # Info icon
        draw.ellipse([size*0.2, size*0.2, size*0.8, size*0.8], outline=color, width=int(size*0.1))
        draw.rectangle([size*0.45, size*0.35, size*0.55, size*0.45], fill=color)
        draw.rectangle([size*0.45, size*0.5, size*0.55, size*0.7], fill=color)
    else:
        # Default: just draw a square with the first letter of the icon name
        draw.rectangle([size*0.2, size*0.2, size*0.8, size*0.8], outline=color, width=int(size*0.1))
        if icon_name:
            # Use a default font for the first letter
            try:
                font = ImageFont.load_default()
                first_letter = icon_name[0].upper()
                # Center the text approximately
                draw.text((size*0.4, size*0.3), first_letter, fill=color, font=font)
            except Exception:
                # If there's an issue with the font, just draw a circle
                draw.ellipse([size*0.4, size*0.4, size*0.6, size*0.6], fill=color)
    
    # Save the SVG to a file for future use
    icon_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
    with open(icon_path, 'w') as f:
        f.write(svg_data)
    
    # Convert to PhotoImage
    return ImageTk.PhotoImage(image)

def create_icon_button(parent, icon_name, command, text=None, size=24, color="#000000", **kwargs):
    """
    Create a button with an icon.
    
    Args:
        parent: Parent widget
        icon_name (str): Name of the icon to use
        command: Button command
        text (str, optional): Button text
        size (int): Size of the icon in pixels
        color (str): Color of the icon in hex format
        **kwargs: Additional keyword arguments for the button
        
    Returns:
        ttk.Button: The created button
    """
    icon = load_svg_icon(icon_name, size, color)
    
    # Create the button
    button = ttk.Button(parent, image=icon, command=command, **kwargs)
    
    # Store the icon to prevent garbage collection
    button.icon = icon
    
    # Add text if provided
    if text:
        button.config(text=text, compound=tk.LEFT)
    
    return button

def save_svg_to_file(icon_name, file_path, size=24, color="#000000"):
    """
    Save an SVG icon to a file.
    
    Args:
        icon_name (str): Name of the icon to save
        file_path (str): Path to save the icon to
        size (int): Size of the icon in pixels
        color (str): Color of the icon in hex format
    """
    if icon_name not in MATERIAL_ICONS:
        raise ValueError(f"Icon {icon_name} not found")
    
    # Replace the color in the SVG
    svg_data = MATERIAL_ICONS[icon_name].replace('path d="', f'path fill="{color}" d="')
    
    # Convert SVG to PNG using cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), 
                               output_width=size, 
                               output_height=size)
    
    # Save the PNG data to a file
    with open(file_path, 'wb') as f:
        f.write(png_data)
