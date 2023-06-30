## makefile automates the build and deployment for python projects

PROJ_TYPE =		python
PROJ_MODULES =		git python-resources python-cli python-doc python-doc-deploy
PIP_ARGS +=		--use-deprecated=legacy-resolver
PY_DEP_POST_DEPS +=	modeldeps
CLEAN_ALL_DEPS +=	data-clean
INFO_TARGETS +=		appinfo

include ./zenbuild/main.mk

.PHONY:			modeldeps
modeldeps:
			$(PIP_BIN) install $(PIP_ARGS) \
				-r src/python/requirements-model.txt --no-deps

.PHONY:			data-clean
data-clean:		clean
			make -C docker/app down || /usr/bin/true
			make -C docker/app cleanall
