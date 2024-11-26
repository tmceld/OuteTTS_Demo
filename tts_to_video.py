import ffmpeg
import argparse



def audio_to_video(audio_file, video_file):
    """
    Generate a video from the audio file with a spectrum visualization.

    Args:
        audio_file (str): Path to the input audio file.
        video_file (str): Path to the output video file.
    """
    try:
        # Create the audio input
        audio_input = ffmpeg.input(audio_file)

        # Apply the showspectrum filter to the audio input to generate video
        video_stream = audio_input.filter(
            'showspectrum', mode='separate', color='intensity', slide=1, scale='cbrt'
        )

        # Combine audio and video in the output
        ffmpeg.output(
            video_stream,  # Video stream from the filter
            audio_input.audio,  # Original audio stream
            video_file,
            pix_fmt="yuv420p",
            vcodec="libx264",  # Video codec
            acodec="aac",  # Audio codec
            audio_bitrate="192k",  # Audio bitrate
            preset="veryfast",
            crf=18  # Quality setting
        ).run(overwrite_output=True)

    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf-8") if e.stderr else "Unknown error"
        raise RuntimeError(f"FFmpeg error: {error_message}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert WAV audio to a spectrum visualization video.")
    parser.add_argument("audio_file", type=str, help="Path to the input WAV file.")
    parser.add_argument("video_file", type=str, help="Path to the output MP4 file.")
    args = parser.parse_args()

    try:
        audio_to_video(args.audio_file, args.video_file)
        print(f"Video successfully created: {args.video_file}")
    except RuntimeError as e:
        print(f"Error: {e}")

