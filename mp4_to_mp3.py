from moviepy.editor import VideoFileClip

def extract_audio(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)

# 设置输入文件路径和输出文件路径
input_file = "a.mp4"
output_file = "output.mp3"

# 调用函数提取音频
extract_audio(input_file, output_file)
