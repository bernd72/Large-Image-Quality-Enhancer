# Large Image Quality Enhancer

**Open-source AI image-quality enhancement for large, high-resolution photographs.**

[Deutsch](README.de.md) · [Contributing](CONTRIBUTING.md) · [Third-party licenses](THIRD_PARTY_NOTICES.md) · [Testing status](TESTING.md) · [Known issues](KNOWN_ISSUES.md)

> **Project setup / no release yet.** This repository currently contains documentation, not a downloadable or functioning application. The existing Python and Windows sources, model files, and Windows executable have not yet been added or legally cleared for public distribution. An existing Windows EXE build has been reported as working on two additional Windows 11 PCs; this is user-reported testing, not a release verification.

## Purpose

Large Image Quality Enhancer is intended to improve image quality rather than enlarge image dimensions. The existing project has been developed around low-light/shadow enhancement, noise reduction, and batch processing of high-resolution photographs. Python and offline Windows distributions are planned.

## Compatibility and testing

**So far, the software has only been tested with JPEG photographs from an Insta360 X5, up to approximately 71 megapixels (11,904 × 5,952 pixels).** The software is intended to be camera-agnostic, but **other cameras, other image formats, and images larger than 71 MP have not been verified**. No maximum supported image size is claimed.

A Windows EXE build was successfully run on a second and third PC, both running Windows 11 (as reported by the developer). The exact EXE build/version and details of the offline test environment remain to be documented; the developer reports that the existing Windows EXE works without internet access. This does **not** establish compatibility with other Windows versions or input formats. Tests at approximately 100, 200, and 500 megapixels are planned, not completed. See [TESTING.md](TESTING.md).

## Known limitation: long Windows paths

The Windows EXE reportedly runs **fully offline** on Windows 11, but problems have occurred when extracting or using it from deeply nested folders. **Workaround:** unpack it to a short path such as `C:\LIQE\` and run it there. The underlying cause and exact path-length limit are not yet confirmed. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Running multiple instances

The Windows executable can be launched multiple times to process jobs in parallel, provided the computer has sufficient resources. According to developer experience, **two instances run simultaneously on a computer with an Intel Core i5-14400 processor**, and **five to six instances are possible on a more powerful machine**. These are example configurations, **not guaranteed performance figures or a fixed software limit**. Effective parallelism depends on CPU load, available RAM, disk throughput, image size, and settings. Monitor resource use; more instances may reduce performance or cause memory pressure.

## Reported processing time

According to developer experience, **processing one complete Insta360 X5 JPEG image of approximately 71 MP takes about 45–50 minutes on an Intel Core i5-14400**. This is a **reported real-world observation, not a standardized benchmark or a guaranteed runtime**. The effect of concurrent instances, RAM configuration, model/settings, and EXE build on this timing has not been systematically recorded.

## Editions (not published yet)

- **Python edition v3.3:** existing version to be imported after source review.
- **Windows offline edition v4.1.1:** intended portable Windows build. A Windows EXE build has been reported working on two additional Windows 11 PCs; the precise tested build/version has not yet been recorded and must not be assumed to be v4.1.1.
- Older versions should remain unchanged when the source is imported.

Offline use has been reported for an existing Windows EXE, and photos are processed locally without cloud uploads. This does not imply that installing dependencies or building the application can be performed without an internet connection.

## Open source and contributions

We welcome issues, code contributions, documentation improvements, and reproducible tests. Read [CONTRIBUTING.md](CONTRIBUTING.md).

The original project material introduced here is provided under the [MIT license](LICENSE). **Third-party code, models, and libraries keep their respective licenses**, and no redistribution right is implied for unverified weights or conversions. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Independent project

This is an independent community project, **not affiliated with or endorsed by Insta360**. Insta360 and product names are mentioned only to identify the camera used in the reported tests.
