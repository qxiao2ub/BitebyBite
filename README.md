# Bite by Bite

<p align="center">
  <img src="assets/bitebybite_light_logo.png" alt="Bite by Bite logo" width="170">
</p>

**Pediatric Meal Tracker**  
**Author: Sidra Almoghrabi**

Bite by Bite is a dual-platform prototype for recording a child's meals, reviewing weekly nutrition progress, coordinating caregivers, and managing food-substitution requests. This repository preserves the original Android/Kotlin project and adds a complete Streamlit web application that can be launched directly on Streamlit Community Cloud.

> This project is an educational prototype. It is not a medical device, does not diagnose health conditions, and does not replace advice from a licensed clinician.

## Streamlit application

The Streamlit version includes:

- Demo sign-in and account-creation flows
- Child profile setup and editing
- Daily meal logging with completion tracking
- Weekly nutrition targets and downloadable CSV report
- Care-team access management
- Caregiver invitation and professional connection forms
- Food-substitution requests and approval workflow
- Privacy and permission explanations
- Responsive styling based on the supplied mobile UI design
- Visible author credit for **Sidra Almoghrabi** in the app header/footer, sidebar, About page, source files, and repository documentation

### Run locally

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. On the sign-in screen, select **Use demo account** to explore the pre-populated prototype immediately.

### Deploy on Streamlit Community Cloud

1. Upload the contents of this repository to a GitHub repository.
2. In Streamlit Community Cloud, create a new app and select that repository and branch.
3. Set the main file path to:

```text
app.py
```

4. In **Advanced settings**, select Python **3.12**.
5. Deploy the app. Streamlit Cloud will install the Python dependencies from `requirements.txt`.

No secrets or external API keys are required for the included prototype.

## Android application

The original Android project remains available in the same repository:

- Kotlin + Jetpack Compose source: `app/src/main/java/`
- Android resources: `app/src/main/res/`
- Gradle configuration: `build.gradle.kts`, `settings.gradle.kts`, and `gradle/`

To open the Android prototype, import the repository root into Android Studio and allow Gradle to synchronize. Local Android build artifacts, IDE state, and machine-specific SDK paths have been removed from version control.

## Repository structure

```text
.
├── app.py                         # Streamlit Cloud entry point
├── bitebybite/                    # Streamlit application package
│   ├── constants.py
│   ├── state.py
│   ├── ui.py
│   └── views.py
├── assets/
│   └── bitebybite_light_logo.png
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── .python-version               # Local/deployment Python target: 3.12
├── app/                           # Original Android application module
├── gradle/                        # Android Gradle wrapper/configuration
├── docs/
│   └── Parent UI - Phone.pdf      # Original mobile UI reference
├── AUTHORS.md
├── RELEASE_NOTES.md
├── LICENSE
└── README.md
```

## Prototype data and security

The Streamlit app uses `st.session_state` for interactive demonstration data. A browser refresh or server restart can reset the session. The prototype does not implement production authentication, a database, email delivery, encrypted health records, or clinical compliance controls.

A production release handling child or health information should include, at minimum, secure identity management, role-based authorization, encrypted storage and transport, audit logging, consent management, retention policies, backup/recovery, professional verification, and legal/privacy review appropriate to the deployment jurisdiction.

## License

MIT License. See [`LICENSE`](LICENSE).

## Author

**Sidra Almoghrabi**
