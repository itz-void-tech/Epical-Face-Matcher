# 🔱 Divine Mirror: Every Person Has A God Within

An AI-powered "Soul Extraction" experience that utilizes real-time Computer Vision to map human facial geometry and reveal the mythological essence residing within.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-white?style=for-the-badge&logo=flask)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face_Mesh-teal?style=for-the-badge&logo=google)

## 🌌 The Concept
The **Divine Mirror** bridges the gap between ancient mythology and modern technology. Using a high-fidelity Face Mesh, the system "scans" the user's presence and identifies a corresponding deity or mythological character from Indian heritage (e.g., Shiva, Durga, Arjuna) based on the "Soul Extraction Protocol."

## ✨ Key Features
* **Real-time Face Mesh:** Utilizes `mediapipe` to track 468+ facial landmarks in real-time.
* **Cinematic UI:** A dark-themed, "Godly Gold" interface featuring **Cinzel Decorative** typography and sacred geometry overlays.
* **Dynamic Essence Mapping:** A randomized algorithm that pair's the user's detected presence with deep philosophical insights (Dharma, Wisdom, Strength).
* **Continuous Scanning:** Visual "Lightning/Scan" bar effect to simulate a high-tech spiritual sync.

---

## 🛠️ Technical Architecture

### Backend
* **Flask:** Handles the web server and video streaming routes.
* **OpenCV:** Manages camera input and frame preprocessing.
* **MediaPipe Face Mesh:** Processes RGB frames to detect facial presence and apply a "Divine" landmark overlay.

### Frontend
* **HTML5/CSS3:** Custom styles with CSS variables for a "Void & Gold" aesthetic.
* **JavaScript (Fetch API):** Communicates with the `/find` endpoint to trigger the soul analysis without reloading the page.

---

## 🚀 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/divine-mirror.git](https://github.com/your-username/divine-mirror.git)
    cd divine-mirror
    ```

2.  **Install Dependencies:**
    ```bash
    pip install flask opencv-python mediapipe numpy
    ```

3.  **Run the Application:**
    ```bash
    python app.py
    ```

4.  **Access the Mirror:**
    Open your browser and navigate to `http://127.0.0.1:5000`

---

## 📜 Soul Extraction Logic
When the **Initiate Seek** button is pressed, the system checks the `face_present` global state:
* **If Detected:** It selects a character from the `DIVINE_CHARACTERS` pool and fetches their corresponding philosophical text.
* **If Not Detected:** It prompts the user to "Look into the divine mirror."

---

## 👤 Author
**Swarnendu Kundu**
* *Embedded Systems & Robotics Enthusiast*

---
*Created with a blend of modern code and ancient wisdom.*
