# Local build environment used by the Makefile (`make serve`, `make build`).
# Mirrors GitHub Actions: same Ruby series (from .ruby-version) + Node.js,
# which the HTML/JS minifier needs. Gems are installed into ./vendor/bundle
# at run time, so this image rarely needs rebuilding.
ARG RUBY_VERSION=3.3
FROM ruby:${RUBY_VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends nodejs imagemagick \
    && rm -rf /var/lib/apt/lists/*
