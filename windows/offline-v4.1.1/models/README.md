# AI models required for Windows EXE build / Für den Windows-EXE-Bau benötigte Modelle

Model weights are **not distributed** with this repository. / Dieses Repository verteilt **keine KI-Modellgewichte**.

For the **manual** build (`BAUE_WINDOWS_EXE.bat`), put these files in **this** `models` directory. Alternatively, use **`AUTO_BUILD_WINDOWS_EXE.bat`** from the parent directory, which asks permission to download missing model files from external model hosts:

- `DPRNet_1024.tflite`
- `scunet_color_real_psnr.onnx`
- `scunet_color_real_psnr.onnx.data`

Optional: `DPRNet_512.tflite`.

The build script validates their presence, then packages copies into the generated portable EXE folder. Get the model files from lawful sources or from your existing local installation where permitted; follow each model's applicable license and do not publish them without verified redistribution rights. See [model instructions](../MODELLE_HIER_EINFUEGEN.txt) and [third-party notices](../../../THIRD_PARTY_NOTICES.md).

**Deutsch:** Diese drei benötigten Dateien vor dem Bau in diesen Ordner legen. Die Herkunft und Weitergaberechte der Gewichte müssen individuell geprüft werden. Keine Modellgewichte ungeprüft veröffentlichen.
