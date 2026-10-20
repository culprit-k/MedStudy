# MedStudy Android test wrapper

This directory contains a lightweight Android WebView wrapper for the image-first MedStudy learning app (120 starter MCQs, sourced medical-image quizzes, revision tools, and a personalised AI teacher). It is a test package, not a native rewrite of the Streamlit application.

## Important: deploy the website first

The APK does not contain a Python/Streamlit server. It opens the HTTPS URL you enter on first launch. The repository has automated code validation, but the owner must deploy the website before the wrapper can be tested against the live app. Deploy the repository in Streamlit Community Cloud:

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Create an app from repository `culprit-k/MedStudy`, branch `main`, main file `app.py`.
3. Wait for the app to finish deploying and copy its actual `.streamlit.app` URL.
4. Open the APK on Android, paste that URL, and tap **Open MedStudy**.

Do not guess the deployment URL. The owner must authorize and deploy the web app before the APK can show it.

## Download a test APK

The workflow at [Build MedStudy Android APK](https://github.com/culprit-k/MedStudy/actions/workflows/android-apk.yml) runs when Android files change on `main`, and can also be started manually:

1. Open the workflow link above.
2. Select **Run workflow** if no run is already in progress.
3. Open the completed successful run.
4. Under **Artifacts**, download `MedStudy-Android-debug-APK`.
5. Extract the ZIP and install `app-debug.apk` on an Android device. You may need to allow installation from the browser or file manager used to open it.

Artifacts are retained for 14 days. This is a debug APK, not a Play Store release; it is not signed with a production release key.

## Build locally

Requires JDK 17, Android SDK Platform 35, and Gradle 8.7 or a compatible Gradle 8.x release.

```bash
cd android
gradle assembleDebug
```

Output: `android/app/build/outputs/apk/debug/app-debug.apk`.

## Scope and security

- The wrapper requires internet access and an HTTPS MedStudy deployment.
- The URL is saved on-device so you do not need to enter it on each launch.
- JavaScript and DOM storage are enabled because Streamlit requires them; file/content access is disabled.
- Non-HTTPS navigation is blocked in the embedded WebView.
- Streamlit session state and optional AI features behave according to the hosted web app; this wrapper does not add offline operation or a local database.
- The package is for educational testing only. MedStudy is not a diagnostic or treatment tool.
