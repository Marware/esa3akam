# Changelog

## Unreleased

- Update artifact transfer actions to their Node 24-native releases.
- Require GitHub-verified annotated tags for production releases.
- Build release artifacts with a hash-locked toolchain.

## 0.1.0 - 2026-08-03

- Promote the tested release candidate to the first stable release.
- Publish releases from signed GitHub tags through PyPI Trusted Publishing.
- Adopt SPDX license metadata for current packaging tools.

## 0.1.0rc1 - 2026-08-02

- Port the original Python 2.7 script to a typed Python 3 package.
- Add timezone-aware `format_time` and `format_now` APIs.
- Calculate day-period labels after timezone conversion.
- Add optional day-period output and a command-line interface.
- Correct Arabic hour and minute inflection across the full clock range.
