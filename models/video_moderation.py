import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
import os
from PIL import Image
from models.image_moderation import ImageModerator

class VideoModerator:
    def __init__(self):
        self.image_moderator = ImageModerator()
        self.frame_results = []
        self.lock = threading.Lock()
    
    def process_frame(self, frame, frame_number):
        try:
            # Convert frame to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Save frame temporarily
            temp_path = f"temp_frame_{frame_number}.jpg"
            pil_image.save(temp_path)
            
            # Analyze frame
            result = self.image_moderator.analyze(temp_path)
            
            # Add frame number to result
            result['frame_number'] = frame_number
            
            # Thread-safe append to results
            with self.lock:
                self.frame_results.append(result)
            
            # Clean up
            os.remove(temp_path)
            
        except Exception as e:
            print(f"Error processing frame {frame_number}: {str(e)}")
    
    def analyze(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            # Process every nth frame (e.g., every second)
            frame_interval = fps
            
            # Reset frame results
            self.frame_results = []
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                frame_number = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_number % frame_interval == 0:
                        executor.submit(self.process_frame, frame, frame_number)
                    
                    frame_number += 1
            
            cap.release()
            
            # Sort results by frame number
            self.frame_results.sort(key=lambda x: x['frame_number'])
            
            # Calculate overall video safety score
            unsafe_frames = sum(1 for result in self.frame_results if not result['safe'])
            safety_percentage = ((len(self.frame_results) - unsafe_frames) / len(self.frame_results)) * 100
            
            return {
                'safe': safety_percentage >= 80,  # Consider video safe if 80% or more frames are safe
                'safety_percentage': round(safety_percentage, 2),
                'total_frames_analyzed': len(self.frame_results),
                'unsafe_frames': unsafe_frames,
                'frame_results': self.frame_results
            }
        
        except Exception as e:
            raise Exception(f"Error processing video: {str(e)}")