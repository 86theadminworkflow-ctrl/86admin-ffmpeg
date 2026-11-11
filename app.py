from flask import Flask, request, jsonify, send_file
import subprocess, os, uuid

app = Flask(__name__)

PLATFORM_SPECS = {
    "instagram":     {"w": 1080, "h": 1920},
    "linkedin":      {"w": 1080, "h": 1080},
    "youtube_long":  {"w": 1920, "h": 1080},
    "youtube_short": {"w": 1080, "h": 1920},
}

@app.route("/health")
def health():
    return "ok"

@app.route("/cut", methods=["POST"])
def cut():
    data = request.json
    video_url   = data["video_url"]
    start       = float(data["start_seconds"])
    end         = float(data["end_seconds"])
    platform    = data["platform"]
    output_name = data.get("output_name", str(uuid.uuid4()))

    spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["youtube_long"])
    duration = end - start
    out_path = f"/tmp/{output_name}.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", video_url,
        "-t", str(duration),
        "-vf", (
            f"scale={spec['w']}:{spec['h']}:force_original_aspect_ratio=decrease,"
            f"pad={spec['w']}:{spec['h']}:(ow-iw)/2:(oh-ih)/2:color=black"
        ),
        "-c:v", "libx264", "-crf", "23", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        out_path
    ]

    result = subprocess.run(cmd, capture_output=True, timeout=300)
    if result.returncode != 0:
        return jsonify({"error": result.stderr.decode()}), 500

    return send_file(out_path, mimetype="video/mp4",
                     download_name=f"{output_name}.mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
