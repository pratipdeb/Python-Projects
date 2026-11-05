import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def match_images_orb(drone_img_path, satellite_map_path):
    # Loading Images in grayscale 
    img_drone = cv.imread(drone_img_path, cv.IMREAD_GRAYSCALE)
    img_sat = cv.imread(satellite_map_path, cv.IMREAD_GRAYSCALE)
    
    if img_drone is None or img_sat is None:
        print("Error loading images.")
        return

    # Initializing ORB detector 
    orb = cv.ORB_create(nfeatures=1000)
    
    # Keypoints and descriptors 
    kp1, des1 = orb.detectAndCompute(img_drone, None)
    kp2, des2 = orb.detectAndCompute(img_sat, None)
    
    # Brute-Force Matcher
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    
    if des1 is not None and des2 is not None:
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Filtering Top 15% good matches 
        good_matches = matches[:int(len(matches) * 0.15)]
        
        # --- NUMPY LOGIC (Coordinates calculation) ---
        if len(good_matches) > 0:
            pts_drone = np.float32([kp1[m.queryIdx].pt for m in good_matches])
            pts_sat = np.float32([kp2[m.trainIdx].pt for m in good_matches])
            
            # Finding out approximate matching features' center (mean) on the satellite Map 
            center_x = np.mean(pts_sat[:, 0])
            center_y = np.mean(pts_sat[:, 1])
            
            print(f"Match Successful! Approximate Drone Center on Map: X={center_x:.2f}, Y={center_y:.2f}")
        # ---------------------------------------------
        
        # Drawing the Matches 
        img_matches = cv.drawMatches(
            img_drone, kp1, img_sat, kp2, good_matches, None, 
            flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        plt.figure(figsize=(15, 8))
        plt.imshow(img_matches)
        plt.title(f"Found {len(good_matches)} Confident Feature Matches")
        plt.axis('off')
        plt.show()
    else:
        print("Not enough features found to compute matches.")


if __name__ == "__main__":
    match_images_orb('drone_photo.jpg', 'satellite_map.jpg')