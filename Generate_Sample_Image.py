import cv2
import numpy as np

def create_sample_image():
    """Create a sample image for steganography testing"""
    
    # Create a 512x512 image with 3 channels (BGR)
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Create a gradient background
    for i in range(512):
        for j in range(512):
            img[i, j] = [
                int(255 * (i / 512)),  # Blue gradient
                int(255 * (j / 512)),  # Green gradient
                int(255 * ((i + j) / 1024))  # Red gradient
            ]
    
    # Add some geometric shapes for visual interest
    # Rectangle
    cv2.rectangle(img, (50, 50), (200, 150), (255, 255, 255), -1)
    cv2.rectangle(img, (55, 55), (195, 145), (0, 0, 0), 2)
    
    # Circle
    cv2.circle(img, (350, 100), 50, (0, 255, 255), -1)
    cv2.circle(img, (350, 100), 45, (255, 0, 0), 3)
    
    # Triangle
    triangle_points = np.array([[100, 300], [200, 300], [150, 250]], np.int32)
    cv2.fillPoly(img, [triangle_points], (255, 0, 255))
    
    # Add text
    cv2.putText(img, 'Sample Image', (250, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, 'For Steganography', (220, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    
    # Add noise for better steganography capacity
    noise = np.random.randint(0, 50, (512, 512, 3), dtype=np.uint8)
    img = cv2.addWeighted(img, 0.9, noise, 0.1, 0)
    
    # Save the image
    cv2.imwrite('sample.png', img)
    print("Sample image 'sample.png' created successfully!")
    print("Image size: 512x512 pixels")
    print("This image can be used for steganography testing.")

if __name__ == "__main__":
    create_sample_image()
