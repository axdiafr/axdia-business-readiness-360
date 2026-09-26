# BR360 Corpus Ingest Notes

## Supplied archive

The research corpus arrived as four multipart 7z volumes. The original uploaded volumes were kept untouched.

The first volume contained a zeroed 7z StartHeader even though a valid encoded header was present at the archive tail. For analysis only, a temporary concatenated copy was created under `/tmp`, its StartHeader was reconstructed from the valid encoded-header location/size/CRC, and the encoded header itself was CRC-validated before parsing.

## Static-first extraction

No repository install script, package manager install, build, binary, postinstall, test suite, Docker compose, Makefile or shell script from the corpus was executed.

The parsed archive header contained **332,242 entries** and **54 repositories**. Root metadata confirmed **54 successful downloads / 0 failed downloads**.

A targeted static reference set of **242 files** (root metadata, license material, readmes and selected manifests/docs) was streamed from the solid archive and **242/242 files matched their archived CRC**.

This process was used only to inventory purpose, concepts, structures and licensing. It is not evidence that any third-party repository is safe to execute.
