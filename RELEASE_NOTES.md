# Release Notes - Streamlit-Ready Repository

## Version 1.0.0

This release converts the supplied Android-only source archive into a clean dual-platform GitHub repository.

### Added

- Root-level `app.py` entry point for Streamlit Community Cloud
- Responsive Streamlit implementation of the Bite by Bite workflow
- Account creation, child onboarding, meal logging, nutrition progress, care-team management, substitutions, privacy, and About views
- Demo session data and CSV/JSON exports
- `.streamlit/config.toml`, `requirements.txt`, and Python version declaration
- `AUTHORS.md` and visible author attribution for **Sidra Almoghrabi**
- Detailed local-run and Streamlit Cloud deployment instructions

### Preserved

- Original Kotlin/Jetpack Compose Android source
- Original logo and visual design language
- Original mobile UI reference PDF
- MIT licensing

### Removed from the repository package

- Generated APK and Android build outputs
- Gradle caches
- Android Studio workspace files
- Machine-specific `local.properties`
- Python cache files
