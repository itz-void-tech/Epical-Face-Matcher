import cv2
import mediapipe as mp
import numpy as np
import time
import random
from flask import Flask, Response, jsonify, render_template_string

# ======================================================
# APP INIT
# ======================================================
app = Flask(__name__)

# ======================================================
# MEDIAPIPE FACE MESH
# ======================================================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ======================================================
# CAMERA
# ======================================================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

# ======================================================
# GLOBAL STATE
# ======================================================
face_present = False
fps = 0

# ======================================================
# MYTHOLOGICAL CHARACTERS (RANDOM POOL)
# ======================================================
DIVINE_CHARACTERS = [
    "Shiva", "Vishnu", "Krishna", "Rama", "Ganesha", "Hanuman",
    "Durga", "Kali", "Lakshmi", "Saraswati", "Parvati",
    "Arjuna", "Karna", "Bhishma", "Ravana", "Sita",
    "Narada", "Surya", "Yama", "Indra"
]

DIVINE_TEXT = {
    "Shiva": "Transformation through stillness.",
    "Vishnu": "Balance sustains the cosmos.",
    "Krishna": "Wisdom hides behind playfulness.",
    "Rama": "Dharma is your backbone.",
    "Ganesha": "Obstacles yield to intelligence.",
    "Hanuman": "Strength through devotion.",
    "Durga": "Fearless protector of truth.",
    "Kali": "Liberation through destruction.",
    "Lakshmi": "Abundance flows where gratitude lives.",
    "Saraswati": "Knowledge is the highest power.",
    "Parvati": "Gentleness with inner fire.",
    "Arjuna": "Focus is your greatest weapon.",
    "Karna": "Loyalty beyond circumstance.",
    "Bhishma": "Sacrifice defines destiny.",
    "Ravana": "Power without restraint destroys itself.",
    "Sita": "Unshaken purity and resilience.",
    "Narada": "Truth travels faster than silence.",
    "Surya": "Radiance fuels all action.",
    "Yama": "Discipline defines balance.",
    "Indra": "Leadership is tested by chaos."
}

# ======================================================
# VIDEO STREAM (CONTINUOUS)
# ======================================================
def gen_frames():
    global fps, face_present
    prev = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = face_mesh.process(rgb)

        face_present = False

        if res.multi_face_landmarks:
            face_present = True
            face = res.multi_face_landmarks[0]

            for lm in face.landmark:
                cv2.circle(
                    frame,
                    (int(lm.x * w), int(lm.y * h)),
                    1,
                    (0, 215, 255),
                    -1
                )

        now = time.time()
        fps = int(1 / (now - prev)) if now != prev else fps
        prev = now

        cv2.putText(
            frame, f"FPS: {fps}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 215, 0), 2
        )

        _, buffer = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )

# ======================================================
# ROUTES
# ======================================================
@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Every Person Has A god Within</title>
    <!-- Fonts: Cinzel Decorative for Legend, Space Grotesk for Data -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --godly-gold: #f5c76b;
            --bronze-artifact: #c89b3c;
            --electric-essence: #00f2ff;
            --void: #020205;
            --energy-violet: #8a2be2;
        }

        /* 1. RESET & SCREEN CONSTRAINTS */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body, html {
            height: 100vh;
            width: 100vw;
            overflow: hidden; /* Zero Scrolling */
            background: var(--void);
            font-family: 'Space Grotesk', sans-serif;
            color: white;
        }

        /* 2. CINEMATIC BACKGROUND */
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: 
                radial-gradient(circle at 20% 30%, rgba(200, 155, 60, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0, 242, 255, 0.05) 0%, transparent 40%);
            z-index: -1;
        }

        /* Subtle Sacred Geometry Watermark */
        .mythic-grid {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://www.transparenttextures.com/patterns/sacred-geometry.png');
            opacity: 0.05;
            pointer-events: none;
            z-index: -1;
        }

        /* 3. LAYOUT STRUCTURE */
        .app-container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            padding: 2vh 2vw;
        }

        header {
            text-align: center;
            height: 8vh;
            margin-bottom: 2vh;
        }

        h1 {
            font-family: 'Cinzel Decorative', cursive;
            font-size: clamp(1rem, 4vh, 2.5rem);
            letter-spacing: 0.4rem;
            text-transform: uppercase;
            background: linear-gradient(to bottom, #fff, var(--godly-gold), var(--bronze-artifact));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 10px rgba(245, 199, 107, 0.3));
        }

        main {
            display: flex;
            flex: 1;
            gap: 2vw;
            height: 85vh;
        }

        /* 4. LEFT: VISUAL FEED (CAMERA) */
        .camera-vault {
            flex: 1.4;
            background: rgba(0,0,0,0.6);
            border: 2px solid rgba(200, 155, 60, 0.3);
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 50px rgba(0,0,0,0.5), inset 0 0 100px rgba(200, 155, 60, 0.05);
        }

        #cam {
            height: 90%;
            width: 90%;
            object-fit: cover;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* CONTINUOUS LIGHTNING / SCAN BAR */
        .scanner-bar {
            position: absolute;
            left: 5%;
            width: 90%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--electric-essence), #fff, var(--electric-essence), transparent);
            box-shadow: 0 0 15px var(--electric-essence), 0 0 30px var(--electric-essence);
            z-index: 5;
            animation: moveScan 4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
            opacity: 0.6;
        }

        @keyframes moveScan {
            0% { top: 5%; }
            50% { top: 95%; }
            100% { top: 5%; }
        }

        /* 5. RIGHT: MENU & COMMANDS */
        .command-center {
            flex: 1;
            background: rgba(10, 10, 15, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(200, 155, 60, 0.2);
            border-radius: 20px;
            padding: 4vh;
            display: flex;
            flex-direction: column;
            border-left: 4px solid var(--bronze-artifact);
        }

        .label {
            font-size: 0.7rem;
            letter-spacing: 0.3rem;
            color: var(--bronze-artifact);
            text-transform: uppercase;
            margin-bottom: 2vh;
        }

        /* 6. BUTTON STATES */
        #findBtn {
            padding: 20px;
            background: transparent;
            border: 2px solid var(--bronze-artifact);
            font-family: 'Cinzel Decorative', cursive;
            font-size: 1.2rem;
            color: var(--godly-gold);
            cursor: pointer;
            transition: 0.5s all ease;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }

        #findBtn:hover {
            background: rgba(200, 155, 60, 0.1);
            letter-spacing: 3px;
            box-shadow: 0 0 20px rgba(200, 155, 60, 0.3);
        }

        /* Status colors */
        .btn-searching { border-color: var(--energy-violet) !important; color: white !important; box-shadow: 0 0 25px var(--energy-violet) !important; animation: pulse 1s infinite alternate; }
        .btn-detected { border-color: var(--electric-essence) !important; color: var(--electric-essence) !important; text-shadow: 0 0 10px var(--electric-essence); }
        .btn-idle { border-color: var(--bronze-artifact); color: var(--godly-gold); }

        @keyframes pulse { 0% { opacity: 0.6; } 100% { opacity: 1; } }

        /* 7. RESULT INTERFACE */
        #result {
            margin-top: 4vh;
            flex: 1;
            opacity: 0;
            transition: 1s ease-out;
            transform: translateY(10px);
        }

        #resName {
            font-family: 'Cinzel Decorative', cursive;
            font-size: 2.2rem;
            margin-bottom: 10px;
            color: #fff;
            text-shadow: 0 0 15px rgba(255,255,255,0.4);
        }

        #resConf {
            color: var(--electric-essence);
            font-family: monospace;
            font-size: 0.8rem;
            margin-bottom: 2vh;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: inline-block;
        }

        #resText {
            line-height: 1.6;
            color: #ccc;
            font-size: 1rem;
            font-weight: 300;
        }
    </style>
</head>
<body>

    <div class="mythic-grid"></div>

    <div class="app-container">
        <header>
            <h1>Every Person Has A god Within</h1>
        </header>

        <main>
            <!-- Left Focal Area -->
            <div class="camera-vault">
                <div class="scanner-bar" id="scanEffect"></div>
                <img id="cam" src="/video">
            </div>

            <!-- Right Navigation Area -->
            <div class="command-center">
                <p class="label">Soul Extraction Protocol</p>
                <button id="findBtn" onclick="analyzeSoul()" class="btn-idle">
                    🔍 Initiate Seek
                </button>

                <div id="result">
                    <p class="label">Essence Identified</p>
                    <div id="resData">
                        <h2 id="resName">--</h2>
                        <span id="resConf">WAITING...</span>
                        <p id="resText"></p>
                    </div>
                </div>

                <div style="margin-top: auto; font-size: 10px; color: #555; letter-spacing: 1px;">
                    ESTABLISHED SYNC: HEAVENLY-LINK-009<br>
                    FREQUENCY: OPTIMIZED
                </div>
            </div>
        </main>
    </div>

    <script>
        const btn = document.getElementById("findBtn");
        const resContainer = document.getElementById("result");
        const scanner = document.getElementById("scanEffect");

        function analyzeSoul() {
            // UI Visual Shift to "Work" mode
            btn.innerHTML = "🌀 SEEKING WITHIN...";
            btn.className = "btn-searching";
            resContainer.style.opacity = 0;
            
            // Intensify scanner for search
            scanner.style.animationDuration = "1s"; 
            scanner.style.background = "var(--energy-violet)";

            fetch("/find")
                .then(r => r.json())
                .then(d => {
                    scanner.style.animationDuration = "4s"; 
                    scanner.style.background = "linear-gradient(90deg, transparent, var(--electric-essence), #fff, var(--electric-essence), transparent)";

                    if(d.name) {
                        btn.className = "btn-detected";
                        btn.innerHTML = "✨ ESSENCE CAPTURED";

                        document.getElementById("resName").innerText = d.name;
                        document.getElementById("resConf").innerText = "Match Confirmed: " + d.confidence;
                        document.getElementById("resText").innerText = d.text;

                        setTimeout(() => {
                            resContainer.style.opacity = 1;
                            resContainer.style.transform = "translateY(0)";
                        }, 200);
                    } else {
                        btn.className = "btn-idle";
                        btn.innerHTML = "✖ NO DEITY FOUND";
                        setTimeout(() => { btn.innerHTML = "🔍 RE-INITIATE"; }, 2000);
                    }
                })
                .catch(() => {
                    btn.className = "btn-idle";
                    btn.innerHTML = "⚠️ SYSTEM DISCORD";
                    scanner.style.animationDuration = "4s";
                });
        }
    </script>
</body>
</html>
""")

@app.route("/video")
def video():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/find")
def find():
    if not face_present:
        return jsonify({
            "name": "No Face Detected",
            "confidence": "—",
            "text": "Look into the divine mirror to reveal your form."
        })

    god = random.choice(DIVINE_CHARACTERS)
    return jsonify({
        "name": god,
        "confidence": f"{random.randint(75, 99)}%",
        "text": DIVINE_TEXT.get(god, "")
    })

# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    app.run(debug=False)
