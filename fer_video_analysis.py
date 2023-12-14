import matplotlib.pyplot as plt
from fer import Video
from fer import FER

def video_Analysis_(video):
    face_detector = FER(mtcnn=True)
    input_video = Video(video)
    processing_data = input_video.analyze(face_detector, display = False, save_frames = False, save_video = False, annotate_frames = False, zip_images = False)
    vid_df = input_video.to_pandas(processing_data)
    vid_df = input_video.get_first_face(vid_df)
    vid_df = input_video.get_emotions(vid_df)
    pltfig = vid_df.plot(figsize=(12, 6), fontsize=12).get_figure()
    plt.legend(fontsize = 'large' , loc = 1)
    pltfig.savefig(r'static/image/fer_output.png')
    return "success"

