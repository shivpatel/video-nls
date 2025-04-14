from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import cv2
import os

def extract_keyframes_with_pyscenedetect(video_path, output_folder, threshold=30.0):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Step 1: Set up video manager and scene manager
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    video_manager.set_downscale_factor()  # Automatically downscale for speed
    video_manager.start()

    # Step 2: Detect scenes
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    print(f"{len(scene_list)} scenes detected!")

    # Step 3: Save a frame from the middle of each scene
    cap = cv2.VideoCapture(video_path)
    for i, (start, end) in enumerate(scene_list):
        middle_frame_num = (start.get_frames() + end.get_frames()) // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_num)
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(output_folder, f"scene_{i+1}_{start}_{end}.jpg")
            cv2.imwrite(filename, frame)

    cap.release()
    video_manager.release()

# Example usage
extract_keyframes_with_pyscenedetect("/Users/shiv/Desktop/sample.mov", "scene_keyframes", threshold=30.0)