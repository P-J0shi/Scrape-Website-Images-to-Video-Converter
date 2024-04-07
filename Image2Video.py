import requests
from bs4 import BeautifulSoup
import os
import urllib
import cv2

def scrape_and_download_images(url, save_folder):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Send a GET request to the URL with custom headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all image tags
        img_tags = soup.find_all('img')
        
        # Create a folder to save the images if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        # Download each image
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                # Construct the absolute URL
                if not img_url.startswith('http'):
                    img_url = url + img_url
                
                # Get the image filename
                img_filename = img_url.split('/')[-1]
                
                # Download the image
                img_path = os.path.join(save_folder, img_filename)
                urllib.request.urlretrieve(img_url, img_path)
                print(f"Downloaded: {img_url}")
    else:
        print("Failed to fetch the URL. Response Status Code:", response.status_code)
                



def scrape_images_from_multiple_pages(base_url, num_pages, save_folder):
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}{page_number}"
        print(f"Scraping images from page {page_number}")
        scrape_and_download_images(url, save_folder)

# Example usage

url = ''  # Replace with the URL you want to scrape
save_folder = '' # Replace with the path where you want to store the images
num_pages = 5 # Replace with the number of pages that you want to scrape
scrape_images_from_multiple_pages(url, num_pages, save_folder)

import cv2
import os

def images_to_video(image_folder, output_video, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    if not images:
        print("No images found in the folder.")
        return

    images.sort(key=lambda x: os.path.getmtime(os.path.join(image_folder, x)))
    # Read the first image to get frame size
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Create video writer with the correct frame size and FPS
    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        img = cv2.imread(img_path)
        if img is not None:
            # Resize image if necessary to match frame size
            if img.shape[0] != height or img.shape[1] != width:
                img = cv2.resize(img, (width, height))
            video.write(img)
            print(f"Processed image: {img_path}")
        else:
            print(f"Failed to read image: {img_path}")

    cv2.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    image_folder = "" # Image folder path
    output_video = "" # Output video path/name
    fps = 0.25
    images_to_video(image_folder, output_video, fps)
