.DEFAULT_GOAL := prepare

.PHONY: help
help: ## Show available make targets.
	@echo "Available make targets:"
	@awk 'BEGIN { FS = ":.*## " } /^[A-Za-z0-9_.-]+:.*## / { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: install-prek
install-prek: ## Install prek and repo git hooks.
	@echo "==> Installing prek"
	@uv tool install prek
	@echo "==> Installing git hooks with prek"
	@uv tool run prek install

.PHONY: prepare
prepare: download-deps install-prek ## Sync dependencies for all workspace packages and install prek hooks.
	@echo "==> Syncing dependencies for all workspace packages"
	@uv sync --frozen --all-extras --all-packages

.PHONY: prepare-build
prepare-build: download-deps ## Sync dependencies for releases without workspace sources.
	@echo "==> Syncing dependencies for release builds (no sources)"
	@uv sync --all-extras --all-packages --no-sources



.PHONY: format format-bugpilot format-kosong format-pykaos format-bugpilot-sdk
format: format-bugpilot format-kosong format-pykaos format-bugpilot-sdk ## Auto-format all workspace packages.
format-bugpilot: ## Auto-format BugPilot sources with ruff.
	@echo "==> Formatting BugPilot sources"
	@uv run ruff check --fix
	@uv run ruff format
format-kosong: ## Auto-format kosong sources with ruff.
	@echo "==> Formatting kosong sources"
	@uv run --project packages/kosong --directory packages/kosong ruff check --fix
	@uv run --project packages/kosong --directory packages/kosong ruff format
format-pykaos: ## Auto-format pykaos sources with ruff.
	@echo "==> Formatting pykaos sources"
	@uv run --project packages/kaos --directory packages/kaos ruff check --fix
	@uv run --project packages/kaos --directory packages/kaos ruff format
format-bugpilot-sdk: ## Auto-format bugpilot-sdk sources with ruff.
	@echo "==> Formatting bugpilot-sdk sources"
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk ruff check --fix
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk ruff format
.PHONY: check check-bugpilot check-kosong check-pykaos check-bugpilot-sdk
check: check-bugpilot check-kosong check-pykaos check-bugpilot-sdk ## Run linting and type checks for all packages.
check-bugpilot: ## Run linting and type checks for BugPilot.
	@echo "==> Checking BugPilot (ruff + pyright + ty; ty is non-blocking)"
	@uv run ruff check
	@uv run ruff format --check
	@uv run pyright
	@uv run ty check || true
check-kosong: ## Run linting and type checks for kosong.
	@echo "==> Checking kosong (ruff + pyright + ty; ty is non-blocking)"
	@uv run --project packages/kosong --directory packages/kosong ruff check
	@uv run --project packages/kosong --directory packages/kosong ruff format --check
	@uv run --project packages/kosong --directory packages/kosong pyright
	@uv run --project packages/kosong --directory packages/kosong ty check || true
check-pykaos: ## Run linting and type checks for pykaos.
	@echo "==> Checking pykaos (ruff + pyright + ty; ty is non-blocking)"
	@uv run --project packages/kaos --directory packages/kaos ruff check
	@uv run --project packages/kaos --directory packages/kaos ruff format --check
	@uv run --project packages/kaos --directory packages/kaos pyright
	@uv run --project packages/kaos --directory packages/kaos ty check || true
check-bugpilot-sdk: ## Run linting and type checks for bugpilot-sdk.
	@echo "==> Checking bugpilot-sdk (ruff + pyright + ty; ty is non-blocking)"
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk ruff check
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk ruff format --check
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk pyright
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk ty check || true
.PHONY: test test-bugpilot test-kosong test-pykaos test-bugpilot-sdk
test: test-bugpilot test-kosong test-pykaos test-bugpilot-sdk ## Run all test suites.
test-bugpilot: ## Run BugPilot tests.
	@echo "==> Running BugPilot tests"
	@uv run pytest tests -vv
	@uv run pytest tests_e2e -vv
test-kosong: ## Run kosong tests (including doctests).
	@echo "==> Running kosong tests"
	@uv run --project packages/kosong --directory packages/kosong pytest --doctest-modules -vv
test-pykaos: ## Run pykaos tests.
	@echo "==> Running pykaos tests"
	@uv run --project packages/kaos --directory packages/kaos pytest tests -vv
test-bugpilot-sdk: ## Run bugpilot-sdk tests.
	@echo "==> Running bugpilot-sdk tests"
	@uv run --project sdks/bugpilot-sdk --directory sdks/bugpilot-sdk pytest tests -vv
.PHONY: build build-bugpilot build-kosong build-pykaos build-bugpilot-sdk build-bin build-bin-onedir
build: build-bugpilot build-kosong build-pykaos build-bugpilot-sdk ## Build Python packages for release.
build-bugpilot: ## Build the bugpilot and bugpilot sdists and wheels.
	@echo "==> Injecting build SHA"
	@uv run scripts/inject_build_sha.py
	@echo "==> Building bugpilot distributions"
	@uv build --package bugpilot --no-sources --out-dir dist
build-kosong: ## Build the kosong sdist and wheel.
	@echo "==> Building kosong distributions"
	@uv build --package kosong --no-sources --out-dir dist/kosong
build-pykaos: ## Build the pykaos sdist and wheel.
	@echo "==> Building pykaos distributions"
	@uv build --package pykaos --no-sources --out-dir dist/pykaos
build-bugpilot-sdk: ## Build the bugpilot-sdk sdist and wheel.
	@echo "==> Building bugpilot-sdk distributions"
	@uv build --package bugpilot-sdk --no-sources --out-dir dist/bugpilot-sdk
build-bin: ## Build the standalone executable with PyInstaller (one-file mode).
	@echo "==> Injecting build SHA"
	@BUGPILOT_BUILD_SHA=$$(git rev-parse HEAD 2>/dev/null | cut -c1-12) uv run scripts/inject_build_sha.py
	@echo "==> Building PyInstaller binary (one-file)"
	@BUGPILOT_BUILD_SHA=$$(git rev-parse HEAD 2>/dev/null | cut -c1-12) uv run pyinstaller bugpilot.spec
	@mkdir -p dist/onefile
	@if [ -f dist/bugpilot.exe ]; then mv dist/bugpilot.exe dist/onefile/; elif [ -f dist/bugpilot ]; then mv dist/bugpilot dist/onefile/; fi
build-bin-onedir: ## Build the standalone executable with PyInstaller (one-dir mode).
	@echo "==> Injecting build SHA"
	@BUGPILOT_BUILD_SHA=$$(git rev-parse HEAD 2>/dev/null | cut -c1-12) uv run scripts/inject_build_sha.py
	@echo "==> Building PyInstaller binary (one-dir)"
	@rm -rf dist/onedir dist/bugpilot
	@BUGPILOT_BUILD_SHA=$$(git rev-parse HEAD 2>/dev/null | cut -c1-12) PYINSTALLER_ONEDIR=1 uv run pyinstaller bugpilot.spec
	@if [ -f dist/bugpilot/bugpilot-exe.exe ]; then mv dist/bugpilot/bugpilot-exe.exe dist/bugpilot/bugpilot.exe; elif [ -f dist/bugpilot/bugpilot-exe ]; then mv dist/bugpilot/bugpilot-exe dist/bugpilot/bugpilot; fi
	@mkdir -p dist/onedir && mv dist/bugpilot dist/onedir/
.PHONY: ai-test
ai-test: ## Run the test suite with BugPilot.
	@echo "==> Running AI test suite"
	@uv run tests_ai/scripts/run.py tests_ai

.PHONY: gen-changelog gen-docs
gen-changelog: ## Generate changelog with BugPilot.
	@echo "==> Generating changelog"
	@uv run bugpilot --yolo --prompt /skill:gen-changelog
gen-docs: ## Generate user docs with BugPilot.
	@echo "==> Generating user docs"
	@uv run bugpilot --yolo --prompt /skill:gen-docs

include src/bugpilot/deps/Makefile
