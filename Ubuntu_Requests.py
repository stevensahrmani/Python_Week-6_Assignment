import requests
import os
import hashlib
from urllib.parse import urlparse

def calculate_checksum(content):
    """Calculate the SHA-256 checksum of the given content."""
    return hashlib.sha256(content).hexdigest()

def fetch_image(url, directory, checksums):
    """Fetch an image from a URL and save it to the specified directory if the checksum matches."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # check the content-type header
        if not response.headers.get('Content-Type', '').startswith('image/'):
            print(f"Skipping {url}: Not an image")
            return
        
        # Calculate the checksum
        checksum = calculate_checksum(response.content)
        if checksum not in checksums:
            print(f"Skipping {url}: Duplicate image")
            return
        
        # Extract the filename from the URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        # Save the image
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f" Successfully fetched: {filename}")
        print(f" image saved to: {filepath}")

        # Add the checksum to the set
        checksums.add(checksum)
    
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An error occurred while processing: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher!")
    print("A tool for mindfully collecting images from the web\n")

    # Get URLs from the user
    urls = input("Please enter the image URLs (separated by sspaces): ").split()

    # Create a directory if it doesn't exist
    directory = "fetched_images"
    os.makedirs(directory, exist_ok=True)

    # Initialize the set of checksums
    checksums = set()

    # Fetch each image
    for url in urls:
        fetch_image(url, directory, checksums)

if __name__ == "__main__":
    main()