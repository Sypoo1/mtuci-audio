import subprocess

INPUT_FILE = "lab56/sentences_az.txt"
VOICE = "az"

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File '{INPUT_FILE}' not found!")
        return

    print(f"Starting audio generation... Total sentences: {len(sentences)}")

    for i, sentence in enumerate(sentences, start=1):
        if i == 9001:
            break
        output_file = f"lab56/audio/{i}.wav"
        command = [
            "espeak-ng",
            f"-v{VOICE}",
            "-w", output_file,
            sentence
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Generated: {output_file}")
        except Exception as e:
            print(f"Error generating file {output_file}: {e}")


    print("\nAll audio files generated successfully!")


if __name__ == "__main__":
    main()
