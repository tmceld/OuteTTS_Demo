import argparse
import os
import datetime
import outetts
import tts_to_video  # Import the new script for video generation

# Configure the model
model_config = outetts.HFModelConfig_v1(
    model_path="OuteAI/OuteTTS-0.2-500M",
    language="en",  # Supported languages in v0.2: en, zh, ja, ko
)

# Initialize the interface
interface = outetts.InterfaceHF(model_version="0.2", cfg=model_config)

# Load a default speaker
interface.print_default_speakers()
speaker = interface.load_default_speaker(name="female_1")


def get_input_text(input_text=None, input_file=None):
    """Retrieve the input text from a string, file, or user prompt."""
    if input_file:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        with open(input_file, "r") as f:
            return f.read()
    elif input_text:
        return input_text
    else:
        return input("Enter the text to synthesize: ")


def generate_output_filename(input_file=None, output_arg=None, extension="wav"):
    """Determine the output filename based on the input or argument."""
    if output_arg:
        return output_arg
    elif input_file:
        base, _ = os.path.splitext(input_file)
        return f"{base}_output.{extension}"
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"output_{timestamp}.{extension}"


def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech Synthesizer")
    parser.add_argument("--text", "-T", type=str, help="Input text string")
    parser.add_argument("--file", "-F", type=str, help="Input text file")
    parser.add_argument("--output", "-O", type=str, help="Output file name")
    parser.add_argument("--video", "-V", action="store_true", help="Generate video from audio")
    args = parser.parse_args()

    try:
        input_text = get_input_text(args.text, args.file)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Generate speech
    output = interface.generate(
        text=input_text,
        temperature=0.1,
        repetition_penalty=1.1,
        max_length=4096,
        speaker=speaker,
    )

    # Determine output file name
    output_filename = generate_output_filename(input_file=args.file, output_arg=args.output, extension="wav")

    # Save the synthesized speech to a file
    output.save(output_filename)
    print(f"Synthesized speech saved to '{output_filename}'.")

    # If the --video flag is True, generate a video
    if args.video:
        video_filename = generate_output_filename(input_file=args.file, output_arg=args.output, extension="mp4")
        print(f"Generating video: {video_filename}...")
        try:
            tts_to_video.audio_to_video(audio_file=output_filename, video_file=video_filename)
            print(f"Video saved to '{video_filename}'.")
        except Exception as e:
            print(f"Error generating video: {e}")


if __name__ == "__main__":
    main()

