# Large Image Quality Enhancer

**Open-source AI image-quality enhancement for large, high-resolution photographs.**

[Deutsch](README.de.md) · [Contributing](CONTRIBUTING.md) · [Third-party licenses](THIRD_PARTY_NOTICES.md) · [Testing status](TESTING.md)

> **Project setup / no release yet.** This repository currently contains documentation, not a downloadable or functioning application. The existing Python and Windows sources, model files, and Windows executable have not yet been added or independently validated for public distribution.

## Purpose

Large Image Quality Enhancer is intended to improve image quality rather than enlarge image dimensions. The existing project has been developed around low-light/shadow enhancement, noise reduction, and batch processing of high-resolution photographs. Python and offline Windows distributions are planned.

## Compatibility and testing

**So far, the software has only been tested with JPEG photographs from an Insta360 X5, up to approximately 71 megapixels (11,904 × 5,952 pixels).** The software is intended to be camera-agnostic, but **other cameras, other image formats, and images larger than 71 MP have not been verified**. No maximum supported image size is claimed.

Tests at approximately 100, 200, and 500 megapixels are planned, not completed. See [TESTING.md](TESTING.md).

## Editions (not published yet)

- **Python edition v3.3:** existing version to be imported after source review.
- **Windows offline edition v4.1.1:** intended portable Windows build; successful installation/build on a separate machine has not yet been confirmed.
- Older versions should remain unchanged when the source is imported.

The intended offline processing does not require cloud image uploads. This does not imply that installation and building can be performed without an internet connection.

## Open source and contributions

We welcome issues, code contributions, documentation improvements, and reproducible tests. Read [CONTRIBUTING.md](CONTRIBUTING.md).

The original project material introduced here is provided under the [MIT license](LICENSE). **Third-party code, models, and libraries keep their respective licenses**, and no redistribution right is implied for unverified weights or conversions. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Independent project

This is an independent community project, **not affiliated with or endorsed by Insta360**. Insta360 and product names are mentioned only to identify the camera used in the reported tests.
