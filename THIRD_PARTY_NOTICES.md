# Third-party projects, model provenance, and license review / Fremdsoftware und Lizenzen

**Status: preliminary inventory, not a completed legal clearance.** This repository now contains the application's Python source code and Windows build scripts. **No third-party model weights, compiled third-party runtime binaries, or finished Windows EXE are included.** The precise origin and licensing of any external code portions, dependencies, and model conversions still need to be verified before binary/model redistribution. This page does not change the respective owners' licenses.

| Project / Projekt | Upstream / Quelle | Upstream license / Lizenz | Status |
|---|---|---|---|
| DPRNet integration / AI Enhance | [raspberrypi/AI_enhance](https://github.com/raspberrypi/AI_enhance) | [BSD 2-Clause](https://github.com/raspberrypi/AI_enhance/blob/main/LICENSE) | Provenance of the actual `DPRNet_1024.tflite` and optional `DPRNet_512.tflite` files must be checked and original notices preserved. |
| SCUNet | [cszn/SCUNet](https://github.com/cszn/SCUNet) | [Apache 2.0](https://github.com/cszn/SCUNet/blob/main/LICENSE) | Verify precise weights and source of the converted `scunet_color_real_psnr.onnx` and `.onnx.data` pair before distribution. |
| LiteRT / ai-edge-litert | [google-ai-edge/LiteRT](https://github.com/google-ai-edge/LiteRT) | Apache 2.0 | Planned/runtime dependency; verify bundled components and license texts. |
| ONNX Runtime | [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | MIT | Planned/runtime dependency; verify distribution notices. |
| PyInstaller | [pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller) | GPLv2 with special bootloader exception (and Apache-licensed portions) | Build tool; generated executables may be distributed subject to dependency licenses. [Details](https://pyinstaller.org/en/stable/license.html). |
| NumPy, Pillow, OpenCV and transitive packages | Upstream projects / Originalprojekte | Various / Unterschiedlich | Inventory exact installed versions and accompanying legal notices before distributing a binary. |

## Release checklist / Checkliste vor der Veröffentlichung von Software

1. Verify that every uploaded source file is owned by a contributor or redistributable under its original license; preserve attribution, copyright, and modification notices.
2. Track origin, author, download location, license, conversion method and checksums for **each exact AI model artifact**, particularly SCUNet ONNX + external data. Do not publish unverified model files.
3. Supply applicable complete third-party license texts and required notices with any source or Windows release; the root MIT license covers only material licensed by this project's contributors.
4. Generate a dependency inventory (including transitive and bundled binary dependencies) from the actual build, not this provisional list.
5. Scan for credentials, proxy information, private certificates, machine-specific paths, private images and other confidential content.
6. Check the Windows release on a clean offline computer and describe any prerequisites accurately.

**Deutsch:** Diese Übersicht ist eine vorläufige Lizenzbestandsaufnahme, **keine Rechtsfreigabe**. Python-Quellcode und Windows-Bauskripte sind jetzt veröffentlicht; **Modellgewichte und fertige EXE nicht**. Die Herkunft und Lizenzen der Modelle, aller Fremdcode-Bestandteile und später gebündelter Bibliotheken müssen geprüft werden, bevor sie öffentlich weitergegeben werden. Die MIT-Lizenz dieses Repositories ersetzt keine Fremdlizenzen.

**Trademark / Markenhinweis:** Insta360 is a trademark/name of its respective owner. This project is independent and is not endorsed by the manufacturer. / Dieses Projekt ist unabhängig und wird vom Hersteller nicht unterstützt.
