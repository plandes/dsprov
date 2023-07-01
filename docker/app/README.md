# Docker image

This repository contains a docker image for the [dsprov] project, which
contains annotations for semantically matching and copy/pasted text between the
discharge summary and electronic health care (EHR) medical notes (note
antecedents) that come before.

This container builds on the [MedSecId Docker container], so it also includes
the [mimic] and [mednlp] tools.



## Usage

The [makefile](makefile) controls building of the image and its life cycle.  To
build the image from scratch:

1. Build or obtain the [mimicdb] image as explained in the [dsprov] docs.
1. Remove any previous Docker image: `make dockerrm`
1. Clean any previous derived objects: `make cleanall`
1. Build the image: `make build`
1. Start the image(s): `make up`


## Obtaining

The [Docker image](https://hub.docker.com/repository/docker/plandes/dsprov)
can be installed with:
```bash
docker pull plandes/dsprov:latest
```


<!-- links -->
[mimicdb]: https://github.com/plandes/mimicdb
[mednlp]: https://github.com/plandes/mednlp
[mimic]: https://github.com/plandes/mimic
[dsprov]: https://github.com/plandes/dsprov
[MedSecId Docker container]: https://github.com/plandes/mimicsid#docker
