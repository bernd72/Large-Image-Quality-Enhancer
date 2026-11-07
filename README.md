# Large Image Quality Enhancer

**Open-source AI image-quality enhancement for large, high-resolution photographs.**

[Deutsch](README.de.md) · [Contributing](CONTRIBUTING.md) · [Third-party licenses](THIRD_PARTY_NOTICES.md) · [Testing status](TESTING.md) · [Known issues](KNOWN_ISSUES.md)

> **Source available — no ready-to-run release yet.** Python v3.3 source and Windows v4.1.1 EXE build scripts are published. **AI model weights and a compiled EXE are not provided**. You must obtain the required model files through sources whose terms permit your intended use. An existing Windows EXE was reportedly tested on two additional Windows 11 PCs; the GitHub build has not been independently verified.

## Quick start (Windows 11, 64-bit)

1. Download the repository using **Code → Download ZIP**, then extract it to a short location such as `C:\\LIQE\\`.
2. Open `windows/offline-v4.1.1/` and run **[AUTO_BUILD_WINDOWS_EXE.bat](windows/offline-v4.1.1/AUTO_BUILD_WINDOWS_EXE.bat)**. The script can install Python 3.12 for the current user, request your consent to download external model files, install Python dependencies, and build a portable application. **An internet connection is generally required for the initial build.**
3. Alternatively, install **Python 3.12 x64** yourself, obtain the three required model files lawfully in the local `models` folder, and run `BAUE_WINDOWS_EXE.bat`.
4. After a successful build, copy the **entire** `dist/Insta360_X5_KI_Offline/` folder to a Windows PC. Running the generated EXE does not require a Python installation or an internet connection.

**Build status:** the automated build has **not** been verified on a clean Windows PC; build success is not guaranteed. No EXE or model weights are hosted in this repository. The automatic script downloads model files from **separate third-party hosts** only after consent; the SCUNet ONNX conversion is hosted by Heliosoph on Hugging Face, not by the original SCUNet authors. Review [model notices](THIRD_PARTY_NOTICES.md) and [Windows build instructions](windows/offline-v4.1.1/README_OFFLINE.txt).

## Python v3.3 interface language

The [Python v3.3 edition](python/v3.3/) now also offers a **„Sprache / Language“** selector to switch its interface between **Deutsch** and **English** without restarting. This includes model-download controls and batch-processing dialogs. Keep the added [`python/v3.3/x5_i18n.py`](python/v3.3/x5_i18n.py) file alongside `x5_dprnet.py`; the existing `STARTEN.bat` remains unchanged. **Switching languages works offline**, while downloading missing AI models may require internet access. A complete native Windows GUI test is still pending.

## Windows interface language

The current Windows source code provides a **„Sprache / Language“** selector for switching the graphical interface between **Deutsch** and **English**. The change takes effect immediately, including in the batch dialog, without restarting the app. Translations are bundled locally; no internet connection is required to switch languages. **Existing EXE builds are not updated automatically:** rebuild the executable from the latest source to obtain this feature. The new language switch has not yet been tested on a Windows PC.

## Purpose

Large Image Quality Enhancer is intended to improve image quality rather than enlarge image dimensions. The existing project has been developed around low-light/shadow enhancement, noise reduction, and batch processing of high-resolution photographs. Two source editions are available here: Python v3.3 and the Windows offline v4.1.1 build kit. Neither is a prebuilt Windows release.

## Compatibility and testing

**So far, the software has only been tested with JPEG photographs from an Insta360 X5, up to approximately 71 megapixels (11,904 × 5,952 pixels).** The software is intended to be camera-agnostic, but **other cameras, other image formats, and images larger than 71 MP have not been verified**. No maximum supported image size is claimed.

A Windows EXE build was successfully run on a second and third PC, both running Windows 11 (as reported by the developer). The exact EXE build/version and details of the offline test environment remain to be documented; the developer reports that the existing Windows EXE works without internet access. This does **not** establish compatibility with other Windows versions or input formats. Tests at approximately 100, 200, and 500 megapixels are planned, not completed. See [TESTING.md](TESTING.md).

## Known limitation: 2:1 aspect ratio only

According to the latest developer tests, the Windows version currently **processes only images with a 2:1 width-to-height ratio** (for example, 11,904 × 5,952 pixels). **Other aspect ratios cause an error during processing, both for individual images and batch jobs.** The root cause is not yet known. Until fixed, successful processing is only reported for 2:1 inputs. See [known issues](KNOWN_ISSUES.md).

## Known limitation: long Windows paths

The Windows EXE reportedly runs **fully offline** on Windows 11, but problems have occurred when extracting or using it from deeply nested folders. **Workaround:** unpack it to a short path such as `C:\LIQE\` and run it there. The underlying cause and exact path-length limit are not yet confirmed. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Security and build caveats

Both source editions currently disable Pillow's default image-size protection (`Image.MAX_IMAGE_PIXELS = None`) to handle very large photos. **Only open trusted image files** until explicit input-size and memory safeguards are in place. The automatic model bootstrap currently checks the sizes of all three model files but verifies a fixed SHA-256 hash for **only one** SCUNet file; the remaining artifacts are not fully checksum-pinned. See [known issues](KNOWN_ISSUES.md). The generated Windows EXE is not digitally signed.

## Running multiple instances

The Windows executable can be launched multiple times to process jobs in parallel, provided the computer has sufficient resources. According to developer experience, **two instances run simultaneously on a computer with an Intel Core i5-14400 processor**, and **five to six instances are possible on a more powerful machine**. These are example configurations, **not guaranteed performance figures or a fixed software limit**. Effective parallelism depends on CPU load, available RAM, disk throughput, image size, and settings. Monitor resource use; more instances may reduce performance or cause memory pressure.

## Reported processing time

According to developer experience, **processing one complete Insta360 X5 JPEG image of approximately 71 MP takes about 45–50 minutes on an Intel Core i5-14400**. This is a **reported real-world observation, not a standardized benchmark or a guaranteed runtime**. The effect of concurrent instances, RAM configuration, model/settings, and EXE build on this timing has not been systematically recorded.

## Language of the Windows build tools

The automatic launcher [`AUTO_BUILD_WINDOWS_EXE.bat`](windows/offline-v4.1.1/AUTO_BUILD_WINDOWS_EXE.bat) and the PowerShell build steps now display prompts, progress messages and errors **in English**, including Python installation and model-download consent. This is separate from the application's German/English GUI selector. The English build prompts have been reviewed in source code, but the full build has not yet been rerun on an English Windows installation.

## Automatic Windows build without pre-installed Python

**New: one-click build for Windows 11 x64.** In the [Windows build kit](windows/offline-v4.1.1/), double-click **[`AUTO_BUILD_WINDOWS_EXE.bat`](windows/offline-v4.1.1/AUTO_BUILD_WINDOWS_EXE.bat)**. The launcher checks for Python 3.12, installs a per-user copy if needed, asks permission to download the third-party DPRNet and SCUNet AI models from the referenced third-party hosts (Raspberry Pi's repository and Heliosoph's converted SCUNet model on Hugging Face), installs build dependencies, and builds the portable EXE. Internet access is needed for missing components **during the build**, and a corporate proxy may block downloads. No administrator privileges are normally needed, although organizational policies may restrict installation. The resulting EXE runs offline on target PCs and needs no Python installation.

**Important:** Python is installed automatically as a build prerequisite, rather than being eliminated from the build process. The automatic build has not yet been independently tested on a clean Windows system. The existing manual workflow remains available. See [Windows build instructions](windows/offline-v4.1.1/README_OFFLINE.txt).

## Source editions and how to start

- **[Python edition v3.3](python/v3.3/):** source code, `requirements.txt`, and Windows `STARTEN.bat`. Requires compatible 64-bit Python, Python dependencies, and DPRNet/SCUNet model files in a local `models` directory. See [`README_START_HIER.txt`](python/v3.3/README_START_HIER.txt).
- **[Windows offline EXE build kit v4.1.1](windows/offline-v4.1.1/):** sources and `BAUE_WINDOWS_EXE.bat` / `.ps1`. On a Windows x64 computer, install Python 3.12 x64, provide the required model files in `windows/offline-v4.1.1/models/`, then run `BAUE_WINDOWS_EXE.bat` to build your own portable executable using PyInstaller. See [`README_OFFLINE.txt`](windows/offline-v4.1.1/README_OFFLINE.txt) and [`model instructions`](windows/offline-v4.1.1/MODELLE_HIER_EINFUEGEN.txt). The build may need internet for Python dependencies; the resulting executable is intended to operate offline.

**Not included:** compiled EXE, AI model weights, Python virtual environments, and generated build outputs. A successful v4.1.1 build has **not** been verified here on Windows; the version of the previously tested Windows EXE was not recorded. The original source editions are kept separately.

Offline use has been reported for an existing Windows EXE, and photos are processed locally without cloud uploads. Installing dependencies or building the application may require an internet connection. Follow model redistribution rules; please do not upload unverified model files.

## Open source and contributions

We welcome issues, code contributions, documentation improvements, and reproducible tests. Read [CONTRIBUTING.md](CONTRIBUTING.md).

The original project material introduced here is provided under the [MIT license](LICENSE). **Third-party code, models, and libraries keep their respective licenses**, and no redistribution right is implied for unverified weights or conversions. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Independent project

This is an independent community project, **not affiliated with or endorsed by Insta360**. Insta360 and product names are mentioned only to identify the camera used in the reported tests.
