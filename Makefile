# Local build/preview helpers. Everything runs inside Docker, using the same
# Ruby version as GitHub Actions (read from .ruby-version), so
# "works locally" == "works on GitHub".
#
#   make serve   -> live preview at http://localhost:4000 (auto-rebuilds on save)
#   make build   -> production build into _site/ (exactly what CI does)
#   make check   -> build, then look for broken internal links / missing images
#   make update  -> update gem versions (rewrites Gemfile.lock)
#   make clean   -> delete build output and caches

RUBY_VERSION := $(shell cat .ruby-version)
IMAGE        := personal-site-jekyll:$(RUBY_VERSION)
PORT         ?= 4000

TTY    := $(shell [ -t 0 ] && echo -it || echo -i)
DOCKER := docker run --rm $(TTY) \
	--user $(shell id -u):$(shell id -g) \
	-e HOME=/tmp \
	-e BUNDLE_PATH=/srv/jekyll/vendor/bundle \
	-v "$(CURDIR)":/srv/jekyll -w /srv/jekyll

.PHONY: serve build check update clean shell install image

# Build the Docker image (cached after the first run).
image:
	docker build -q --build-arg RUBY_VERSION=$(RUBY_VERSION) -t $(IMAGE) . >/dev/null

install: image
	$(DOCKER) $(IMAGE) bundle install

serve: install
	$(DOCKER) -p $(PORT):$(PORT) -p 35729:35729 $(IMAGE) \
		bundle exec jekyll serve --host 0.0.0.0 --port $(PORT) --livereload --force_polling

build: install
	$(DOCKER) -e JEKYLL_ENV=production $(IMAGE) bundle exec jekyll build

check: build
	python3 bin/check_site.py _site

update: image
	$(DOCKER) $(IMAGE) bundle update

shell: image
	$(DOCKER) $(IMAGE) bash

clean:
	rm -rf _site .jekyll-cache .sass-cache .jekyll-metadata
