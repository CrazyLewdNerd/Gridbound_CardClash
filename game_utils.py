import pygame
import urllib.request
import io

def get_image(image_path, dimensions):
    try:
        # Check if the image path is a URL
        if image_path.startswith("http://") or image_path.startswith("https://"):
            # Load the image from the URL
            response = urllib.request.urlopen(image_path)
            image_data = response.read()
            image = pygame.image.load_extended(io.BytesIO(image_data))
        else:
            # Load the image from the local file path
            image = pygame.image.load(image_path)

        return pygame.transform.scale(image, dimensions)

    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return f"Error loading image: {str(e)}"
    