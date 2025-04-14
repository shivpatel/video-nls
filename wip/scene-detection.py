from scenedetect import detect, SceneManager, AdaptiveDetector, open_video

# scene_list = detect('/Users/shiv/Desktop/sample.mov', AdaptiveDetector())

scene_manager = SceneManager()

scene_manager.add_detector(AdaptiveDetector())

video = open_video('/Users/shiv/Desktop/sample.mov')

scene_manager.detect_scenes(video=video)

scene_list = scene_manager.get_scene_list()

scene_manager.save_images(scene_list, video, num_images=3, image_extension='jpg', output_dir='./images')

# for scene in scene_list:
#     print(scene)

video.close()