"""
Script to download a Ganesh image for the sidebar
Run this script to get a default Ganesh image if you don't have one
"""
import requests
from pathlib import Path

def download_ganesh_image():
    """Download a public domain Ganesh image"""
    # Using a public domain Ganesh image URL
    image_urls = [
        "https://images.unsplash.com/photo-1599639957043-d2394395f7e3?w=400",  # Ganesh statue
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Ganesha_Basohli_miniature_circa_1730_Dubost_p64.jpg/400px-Ganesha_Basohli_miniature_circa_1730_Dubost_p64.jpg",
    ]
    
    output_path = Path(__file__).parent / "ganesh.jpg"
    
    for url in image_urls:
        try:
            print(f"Downloading Ganesh image from {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Ganesh image saved successfully at: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to download from {url}: {e}")
            continue
    
    print("⚠️ Could not download any image. Please manually save your Ganesh image as 'ganesh.jpg' in the assets folder.")
    return False

if __name__ == "__main__":
    download_ganesh_image()
