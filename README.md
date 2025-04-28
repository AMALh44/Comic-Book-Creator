# Comic-Book-Creator

## Overview

This project is an AI-powered comic generator that automatically creates comic book pages from text descriptions using Stable Diffusion. It segments stories into scenes, generates corresponding images, adds speech bubbles, and compiles everything into a professional PDF comic book.

## Features

* Automated Comic Creation: Converts text stories into illustrated comic panels.

* Local AI Generation: Uses a local Stable Diffusion model for fast, private image generation.

* Professional PDF Output: Combines images and text into a polished comic book format.

* Dialogue Integration: Auto-detects and places speech bubbles in the generated images.

## Key Technologies

* Python: Main scripting language.

* Hugging Face Diffusers: For local Stable Diffusion model integration.

* PIL (Python Imaging Library): For image processing.

* FPDF: For creating multi-page PDFs from generated images.

## Workflow

1. Story Input: User provides a written story in paragraph form.

2. Scene Segmentation: The story is broken into smaller scenes.

3. Prompt Enrichment: Each scene is enhanced with visual details (background, characters, style).

4. Image Generation: Stable Diffusion generates images from the enriched prompts.

5. PDF Compilation: Generated images and text are combined into a downloadable PDF.
