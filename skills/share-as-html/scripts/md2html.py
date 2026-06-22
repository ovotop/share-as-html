#!/usr/bin/env python3
"""Convert Markdown presentation projects to self-contained HTML.

Usage:
    python md2html.py <project_dir> [-o <output.html>]

The project directory must contain meta.md and slides/*.md.
Output is a self-contained HTML file with DOC/PPT/Zoom modes.
"""

import argparse
import base64
import html
import mimetypes
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional

import markdown
import yaml
from jinja2 import Template


# ============================================================================
# CSS Template — from share-as-html SKILL.md
# ============================================================================

CSS_TEMPLATE = r"""
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
    --bg: #0f172a;
    --surface: #1e293b;
    --surface2: #334155;
    --border: #475569;
    --text: #e2e8f0;
    --text-dim: #94a3b8;
    --accent: #38bdf8;
    --accent2: #818cf8;
    --green: #4ade80;
    --orange: #fb923c;
    --red: #f87171;
    --yellow: #fbbf24;
}

html { scroll-behavior: smooth; }

body {
    font-family: -apple-system, 'SF Pro Display', 'PingFang SC', 'Noto Sans SC', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

code, pre { font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace; }

.slide {
    min-height: auto;
    padding: 32px 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-bottom: none;
    position: relative;
}

.slide-number {
    position: absolute;
    top: 24px;
    right: 32px;
    font-size: 14px;
    color: var(--text-dim);
    font-family: 'SF Mono', monospace;
}

.cover {
    text-align: center;
    background: linear-gradient(135deg, var(--surface) 0%, var(--bg) 100%);
}

.cover h1 {
    font-size: clamp(32px, 5vw, 48px);
    font-weight: 700;
    margin-bottom: 16px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.cover .subtitle {
    font-size: 24px;
    color: var(--text-dim);
    margin-bottom: 8px;
}

.cover .meta {
    font-size: 14px;
    color: var(--text-dim);
}

.content { max-width: 900px; width: 100%; }

h2 {
    font-size: clamp(24px, 4vw, 36px);
    font-weight: 600;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

h2 .emoji { font-size: 32px; }

h3 {
    font-size: clamp(17px, 2.5vw, 22px);
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 16px;
    margin-top: 24px;
}

p { margin-bottom: 12px; color: var(--text); font-size: clamp(14px, 1.5vw, 16px); }

.point {
    padding: 12px 16px;
    margin-bottom: 8px;
    border-left: 3px solid var(--border);
    background: var(--surface);
    border-radius: 0 8px 8px 0;
}

.point.highlight {
    border-left-color: var(--accent);
    background: rgba(56, 189, 248, 0.08);
}

.point.star {
    border-left-color: var(--yellow);
    background: rgba(251, 191, 36, 0.08);
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}

.card h4 {
    font-size: clamp(14px, 1.5vw, 16px);
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--accent);
}

.card p { font-size: 14px; color: var(--text-dim); }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin: 16px 0; }
.grid-4 { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; margin: 16px 0; }

.flex-row { display: flex; gap: 16px; margin: 16px 0; flex-wrap: wrap; }
.flex-col { display: flex; flex-direction: column; gap: 16px; margin: 16px 0; }
.stack { display: flex; flex-direction: column; gap: 16px; margin: 16px 0; }

.split-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin: 16px 0;
}


pre {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    overflow-x: auto;
}

pre code { font-size: 14px; line-height: 1.5; color: var(--text); }

code {
    background: var(--surface);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
}

.cmd { color: var(--green); }
.comment { color: var(--text-dim); }
.string { color: var(--yellow); }
.keyword { color: var(--accent2); }

.tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    background: var(--surface2);
    color: var(--text-dim);
}

.tag-blue { background: rgba(56, 189, 248, 0.15); color: var(--accent); }
.tag-green { background: rgba(74, 222, 128, 0.15); color: var(--green); }
.tag-orange { background: rgba(251, 146, 60, 0.15); color: var(--orange); }
.tag-purple { background: rgba(129, 140, 248, 0.15); color: var(--accent2); }

.metrics-row { display: flex; gap: 24px; margin: 16px 0; flex-wrap: wrap; }

.metric {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 24px;
    background: var(--surface);
    border-radius: 12px;
    border: 1px solid var(--border);
    min-width: 120px;
}

.metric .value { font-size: 32px; font-weight: 700; color: var(--accent); }
.metric .label { font-size: 13px; color: var(--text-dim); margin-top: 4px; }

.flow { counter-reset: flow-counter; margin: 16px 0; }

.flow-item {
    counter-increment: flow-counter;
    padding: 12px 16px 12px 56px;
    margin-bottom: 8px;
    background: var(--surface);
    border-radius: 8px;
    position: relative;
}

.flow-item::before {
    content: counter(flow-counter);
    position: absolute;
    left: 16px;
    top: 12px;
    width: 28px;
    height: 28px;
    background: var(--accent);
    color: var(--bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
}

th, td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

th {
    background: var(--surface);
    font-weight: 600;
    color: var(--accent);
    font-size: 14px;
}

td { font-size: 14px; }
tr:hover td { background: rgba(56, 189, 248, 0.04); }

ul {
    list-style: none;
    margin: 12px 0;
}

ul li {
    padding: 6px 0 6px 20px;
    position: relative;
    font-size: clamp(14px, 1.5vw, 16px);
}

ul li::before {
    content: '\25B8';
    position: absolute;
    left: 0;
    color: var(--accent);
    font-weight: bold;
}

/* Callout */
.callout {
    padding: 16px 20px;
    border-radius: 8px;
    margin: 16px 0;
    border-left: 4px solid var(--accent);
    background: rgba(56, 189, 248, 0.08);
}

.callout.callout-info { border-left-color: var(--accent); background: rgba(56, 189, 248, 0.08); }
.callout.callout-warn { border-left-color: var(--orange); background: rgba(251, 146, 60, 0.08); }
.callout.callout-tip { border-left-color: var(--green); background: rgba(74, 222, 128, 0.08); }
.callout.callout-danger { border-left-color: var(--red); background: rgba(248, 113, 113, 0.08); }

.callout strong { color: var(--accent); }
.callout.callout-warn strong { color: var(--orange); }
.callout.callout-tip strong { color: var(--green); }

/* Steps */
.steps { margin: 16px 0; }

.step {
    padding: 12px 16px 12px 48px;
    margin-bottom: 8px;
    background: var(--surface);
    border-radius: 8px;
    position: relative;
}

.step::before {
    content: counter(step-counter);
    counter-increment: step-counter;
    position: absolute;
    left: 12px;
    top: 12px;
    width: 26px;
    height: 26px;
    background: var(--accent);
    color: var(--bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}

.steps { counter-reset: step-counter; }

/* Mermaid */
.mermaid {
    display: flex;
    justify-content: center;
    margin: 16px 0;
}

.mermaid svg {
    max-width: 100%;
    height: auto;
}

/* Diagram Focus State */
.diagram-focusable {
    cursor: pointer;
    border: 2px solid transparent;
    border-radius: 8px;
    transition: border-color 0.2s;
    padding: 4px;
}

.diagram-focusable.focused { border-color: var(--accent); }

.diagram-focusable.no-focus {
    opacity: 0.6;
    cursor: default;
    border-color: transparent !important;
}

.diagram-focusable.no-focus:hover { border-color: transparent !important; }

/* Reader narrative (DOC mode only) */
.reader-narrative {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    color: var(--text-dim);
    font-size: 15px;
    line-height: 1.8;
}

.reader-narrative p { color: var(--text-dim); }

/* PPT Mode */
body.mode-ppt { overflow: hidden; }

body.mode-ppt .slide {
    min-height: 100vh;
    padding: 60px 80px;
    border-bottom: 1px solid var(--border);
    scroll-snap-align: start;
    scroll-snap-stop: always;
    align-items: center;
}

body.mode-ppt .slide .content { max-width: 1100px; }

body.mode-ppt .reader-narrative { display: none; }

#scroll-container.mode-ppt {
    scroll-snap-type: y proximity;
    overflow-y: scroll;
    overflow-x: auto;
    height: 100vh;
}

/* Bounce Animations */
@keyframes slide-bounce-down {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(8px); }
}

@keyframes slide-bounce-up {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

@keyframes slide-bounce-left {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(-8px); }
}

@keyframes slide-bounce-right {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(8px); }
}

#scroll-container.bounce-down { animation: slide-bounce-down 0.3s ease-out; }
#scroll-container.bounce-up { animation: slide-bounce-up 0.3s ease-out; }
#scroll-container.bounce-left { animation: slide-bounce-left 0.3s ease-out; }
#scroll-container.bounce-right { animation: slide-bounce-right 0.3s ease-out; }

/* Zoom Mode */
body.mode-zoom .slide { display: none; }

body.mode-zoom .zoom-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    z-index: 100;
    overflow: auto;
}

body.mode-zoom .reader-narrative { display: none; }

/* Responsive */
@media (max-width: 768px) {
    .slide { padding: 24px 16px; }
    body.mode-ppt .slide { padding: 40px 20px; }
    .grid-2, .grid-3, .grid-4, .split-layout { grid-template-columns: 1fr; }
    .flex-row { flex-direction: column; }
}

@media print {
    .slide { page-break-after: always; min-height: auto; padding: 40px; }
}

/* Doc Footer (DOC mode only) */
.doc-footer { text-align: center; padding: 24px 0 32px 0; font-size: 12px; color: var(--text-dim); border-top: 1px solid var(--surface2); margin-top: 48px; }
.doc-footer a { color: var(--text-dim); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }
.doc-footer a:hover { color: var(--accent); }
.doc-footer img { vertical-align: middle; }
body.mode-ppt .doc-footer, body.mode-zoom .doc-footer { display: none; }
"""

# ============================================================================
# JS Template — from share-as-html SKILL.md
# ============================================================================

JS_TEMPLATE = r"""
let currentState = 'DOC';
let currentSlideIndex = 0;
let focusedDiagramIndex = -1;
let isAtScrollBoundary = false;
let zoomTarget = null;

document.addEventListener('keydown', (e) => {
    const slides = document.querySelectorAll('.slide');

    switch(currentState) {
        case 'DOC':
            if (e.key === 'Enter') {
                e.preventDefault();
                enterPPTMode();
            }
            break;

        case 'PPT_FULL':
            if (e.key === 'Escape') {
                e.preventDefault();
                enterDocMode();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                const focused = document.querySelector('.diagram-focusable.focused');
                if (focused) enterZoomMode(focused);
            } else if (e.key === 'ArrowDown' || e.key === ' ') {
                e.preventDefault();
                if (isAtScrollBoundary) {
                    navigateSlide(1);
                } else if (canScrollVertically(1)) {
                    scrollSlideContent(1, 'y');
                    if (!canScrollVertically(1)) {
                        isAtScrollBoundary = true;
                        triggerBounce(1, 'y');
                    }
                } else {
                    navigateSlide(1);
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (isAtScrollBoundary) {
                    navigateSlide(-1);
                } else if (canScrollVertically(-1)) {
                    isAtScrollBoundary = false;
                    scrollSlideContent(-1, 'y');
                    if (!canScrollVertically(-1)) {
                        isAtScrollBoundary = true;
                        triggerBounce(-1, 'y');
                    }
                } else {
                    navigateSlide(-1);
                }
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                if (isAtScrollBoundary) {
                    handleFocusSwitch('ArrowRight');
                } else if (canScrollHorizontally(1)) {
                    scrollSlideContent(1, 'x');
                    if (!canScrollHorizontally(1)) {
                        isAtScrollBoundary = true;
                        triggerBounce(1, 'x');
                    }
                } else {
                    handleFocusSwitch('ArrowRight');
                }
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                if (isAtScrollBoundary) {
                    handleFocusSwitch('ArrowLeft');
                } else if (canScrollHorizontally(-1)) {
                    isAtScrollBoundary = false;
                    scrollSlideContent(-1, 'x');
                    if (!canScrollHorizontally(-1)) {
                        isAtScrollBoundary = true;
                        triggerBounce(-1, 'x');
                    }
                } else {
                    handleFocusSwitch('ArrowLeft');
                }
            }
            break;

        case 'PPT_ZOOM':
            if (e.key === 'Escape') {
                e.preventDefault();
                exitZoomMode();
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                scrollZoomContainer('left');
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                scrollZoomContainer('right');
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (!scrollZoomContainer('up')) {
                    exitZoomMode();
                    navigateSlide(-1);
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (!scrollZoomContainer('down')) {
                    exitZoomMode();
                    navigateSlide(1);
                }
            }
            break;
    }
});

function enterPPTMode() {
    currentState = 'PPT_FULL';
    isAtScrollBoundary = false;
    document.body.className = 'mode-ppt';
    const container = document.getElementById('scroll-container');
    if (container) container.classList.add('mode-ppt');

    const slides = document.querySelectorAll('.slide');
    const scrollTop = container ? container.scrollTop : window.scrollY;
    const viewportCenter = scrollTop + window.innerHeight / 2;
    let nearestIndex = 0;
    let minDistance = Infinity;

    slides.forEach((slide, i) => {
        const slideTop = slide.offsetTop - (container ? container.offsetTop : 0);
        const slideCenter = slideTop + slide.offsetHeight / 2;
        const distance = Math.abs(slideCenter - viewportCenter);
        if (distance < minDistance) {
            minDistance = distance;
            nearestIndex = i;
        }
    });

    currentSlideIndex = nearestIndex;
    slides[nearestIndex].scrollIntoView({ behavior: 'instant' });
    updateFocus();
}

function enterDocMode() {
    currentState = 'DOC';
    document.body.className = '';
    const container = document.getElementById('scroll-container');
    if (container) container.classList.remove('mode-ppt');
    clearFocus();

    const slide = document.querySelectorAll('.slide')[currentSlideIndex];
    if (slide) {
        const target = slide.offsetTop + slide.offsetHeight / 2 - window.innerHeight / 2;
        window.scrollTo({ top: Math.max(0, target), behavior: 'instant' });
    }
}

function enterZoomMode(element) {
    currentState = 'PPT_ZOOM';
    zoomTarget = element;
    document.body.className = 'mode-zoom';

    const container = document.createElement('div');
    container.className = 'zoom-container';
    const clone = element.cloneNode(true);
    clone.classList.add('zoom-content');
    container.appendChild(clone);
    document.body.appendChild(container);
}

function exitZoomMode() {
    currentState = 'PPT_FULL';
    document.body.className = 'mode-ppt';
    const container = document.getElementById('scroll-container');
    if (container) container.classList.add('mode-ppt');

    const zoomContainer = document.querySelector('.zoom-container');
    if (zoomContainer) zoomContainer.remove();
    zoomTarget = null;

    const slides = document.querySelectorAll('.slide');
    if (slides[currentSlideIndex]) {
        const targetTop = slides[currentSlideIndex].offsetTop - (container ? container.offsetTop : 0);
        window.scrollTo({ top: targetTop, behavior: 'instant' });
    }

    updateFocus(true);
}

function navigateSlide(direction) {
    const slides = document.querySelectorAll('.slide');
    const newIndex = Math.max(0, Math.min(slides.length - 1, currentSlideIndex + direction));

    if (newIndex !== currentSlideIndex) {
        currentSlideIndex = newIndex;
        isAtScrollBoundary = false;
        slides[newIndex].scrollIntoView({ behavior: 'instant' });
        updateFocus();
    }
}

function updateFocus(preserveIndex) {
    preserveIndex = preserveIndex || false;
    const savedIndex = focusedDiagramIndex;
    clearFocus();
    if (!preserveIndex) isAtScrollBoundary = false;
    const slide = document.querySelectorAll('.slide')[currentSlideIndex];
    if (!slide) return;

    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
        .filter(function(el) { return !el.classList.contains('no-focus'); });
    if (focusables.length > 0) {
        if (!preserveIndex || savedIndex < 0 || savedIndex >= focusables.length) {
            focusedDiagramIndex = 0;
        } else {
            focusedDiagramIndex = savedIndex;
        }
        focusables[focusedDiagramIndex].classList.add('focused');
    }
}

function clearFocus() {
    document.querySelectorAll('.diagram-focusable.focused').forEach(function(el) {
        el.classList.remove('focused');
    });
    focusedDiagramIndex = -1;
}

function handleFocusSwitch(key) {
    const slide = document.querySelectorAll('.slide')[currentSlideIndex];
    if (!slide) return;

    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
        .filter(function(el) { return !el.classList.contains('no-focus'); });
    if (focusables.length <= 1) return;

    var newIndex;
    if (key === 'ArrowRight') {
        newIndex = Math.min(focusedDiagramIndex + 1, focusables.length - 1);
    } else {
        newIndex = Math.max(focusedDiagramIndex - 1, 0);
    }

    focusedDiagramIndex = newIndex;

    document.querySelectorAll('.diagram-focusable.focused').forEach(function(el) {
        el.classList.remove('focused');
    });
    focusables[focusedDiagramIndex].classList.add('focused');
}

function scrollZoomContainer(direction) {
    const container = document.querySelector('.zoom-container');
    if (!container) return false;

    const scrollAmount = 100;

    switch(direction) {
        case 'up':
            if (container.scrollTop <= 0) return false;
            container.scrollTop -= scrollAmount;
            return true;
        case 'down':
            if (container.scrollTop + container.clientHeight >= container.scrollHeight) return false;
            container.scrollTop += scrollAmount;
            return true;
        case 'left':
            container.scrollLeft -= scrollAmount;
            return true;
        case 'right':
            container.scrollLeft += scrollAmount;
            return true;
    }
    return false;
}

function canScrollVertically(direction) {
    const container = document.getElementById('scroll-container');
    if (!container) return false;
    const slides = document.querySelectorAll('.slide');
    const slide = slides[currentSlideIndex];
    if (!slide) return false;

    const containerScrollTop = container.scrollTop;
    const containerHeight = container.clientHeight;
    const slideTop = slide.offsetTop - container.offsetTop;
    const slideBottom = slideTop + slide.offsetHeight;

    if (direction > 0) {
        return containerScrollTop + containerHeight < slideBottom - 10;
    } else {
        return containerScrollTop > slideTop + 10;
    }
}

function canScrollHorizontally(direction) {
    const container = document.getElementById('scroll-container');
    if (!container) return false;
    const slides = document.querySelectorAll('.slide');
    const slide = slides[currentSlideIndex];
    if (!slide) return false;

    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
        .filter(function(el) { return !el.classList.contains('no-focus'); });
    if (focusables.length === 0 || focusedDiagramIndex < 0 || focusedDiagramIndex >= focusables.length) return false;

    const focused = focusables[focusedDiagramIndex];
    const diagramWidth = focused.scrollWidth;
    const containerWidth = container.clientWidth;

    if (diagramWidth <= containerWidth + 10) return false;

    if (direction > 0) {
        return container.scrollLeft + containerWidth < diagramWidth - 10;
    } else {
        return container.scrollLeft > 10;
    }
}

function scrollSlideContent(direction, axis) {
    const container = document.getElementById('scroll-container');
    if (!container) return false;

    const oldSnap = container.style.scrollSnapType;
    container.style.scrollSnapType = 'none';

    const dimension = axis === 'y' ? 'clientHeight' : 'clientWidth';
    const scrollProp = axis === 'y' ? 'scrollTop' : 'scrollLeft';
    const step = container[dimension] * 0.8;

    container.scrollTo({
        [axis === 'y' ? 'top' : 'left']: container[scrollProp] + direction * step,
        behavior: 'smooth'
    });

    setTimeout(function() {
        container.style.scrollSnapType = oldSnap || 'y proximity';
    }, 500);

    return true;
}

function triggerBounce(direction, axis) {
    const container = document.getElementById('scroll-container');
    if (!container) return;

    var bounceClass;
    if (axis === 'y') {
        bounceClass = direction > 0 ? 'bounce-down' : 'bounce-up';
    } else {
        bounceClass = direction > 0 ? 'bounce-right' : 'bounce-left';
    }

    container.classList.add(bounceClass);
    setTimeout(function() { container.classList.remove(bounceClass); }, 300);
}

window.addEventListener('load', function() {
    document.querySelectorAll('.mermaid svg, img').forEach(function(el) {
        const rect = el.getBoundingClientRect();
        const needsZoom = rect.width > window.innerWidth || rect.height > window.innerHeight;
        if (needsZoom) {
            const wrapper = el.closest('.diagram-focusable') || el.parentElement;
            if (wrapper) wrapper.classList.add('needs-zoom');
        }
    });
});
"""

# ============================================================================
# HTML Template (Jinja2)
# ============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ meta.title }}</title>
    <style>{{ css }}</style>{% if override_css %}
    <style>{{ override_css }}</style>{% endif %}
</head>
<body>
    <div id="scroll-container">
{% for slide in slides %}
        <div class="slide {{ 'cover' if slide.is_cover else '' }}" data-slide="{{ slide.number }}">
{% if slide.number %}
            <span class="slide-number">{{ '%02d'|format(slide.number) }}</span>
{% endif %}
            <div class="content">
{{ slide.visual_html | indent(16, first=True) }}
            </div>
{% if slide.reader_html %}
            <div class="reader-narrative">
{{ slide.reader_html | indent(16, first=True) }}
            </div>
{% endif %}
        </div>
{% endfor %}
        <div class="doc-footer">
            <a href="https://github.com/ovotop/share-as-html" target="_blank" rel="noopener">
                <img src="https://avatars.githubusercontent.com/u/166823538?s=32" alt="ovotop" width="16" height="16">
                Powered by ovotop/share-as-html
            </a>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
    <script>{{ js }}</script>
</body>
</html>"""


# ============================================================================
# Data Structures
# ============================================================================

class _BlockSplitter(HTMLParser):
    """Split HTML into top-level block elements, respecting nested tags."""

    _VOID_TAGS = frozenset({"img", "hr", "br", "input", "source", "link", "meta", "area", "base", "col", "embed", "track", "wbr"})

    def __init__(self):
        super().__init__()
        self.blocks: list[str] = []
        self._buf: list[str] = []
        self._depth = 0
        self._root_tag: str | None = None

    def _append_tag(self, s: str):
        if self._depth == 0:
            self._buf = [s]
            self._root_tag = None
        else:
            self._buf.append(s)

    def handle_starttag(self, tag, attrs):
        a = "".join(f' {k}="{v}"' for k, v in attrs)
        if tag in self._VOID_TAGS:
            s = f"<{tag}{a} />"
            if self._depth == 0:
                self.blocks.append(s)
            else:
                self._buf.append(s)
            return
        s = f"<{tag}{a}>"
        if self._depth == 0:
            self._buf = [s]
            self._root_tag = tag
        else:
            self._buf.append(s)
        self._depth += 1

    def handle_startendtag(self, tag, attrs):
        a = "".join(f' {k}="{v}"' for k, v in attrs)
        s = f"<{tag}{a} />"
        if self._depth == 0:
            self.blocks.append(s)
        else:
            self._buf.append(s)

    def handle_endtag(self, tag):
        self._buf.append(f"</{tag}>")
        self._depth -= 1
        if self._depth == 0 and tag == self._root_tag:
            self.blocks.append("".join(self._buf))
            self._buf = []
            self._root_tag = None

    def handle_data(self, data):
        self._buf.append(data)

    def handle_entityref(self, name):
        self._buf.append(f"&{name};")

    def handle_charref(self, name):
        self._buf.append(f"&#{name};")


def split_top_level_blocks(html_str: str) -> list[str]:
    """Split HTML string into top-level block elements."""
    splitter = _BlockSplitter()
    splitter.feed(html_str)
    return splitter.blocks


class Slide:
    """Represents a single presentation slide."""

    __slots__ = (
        "number", "duration", "layout", "cols", "ratio",
        "gap", "accent", "emoji", "visual_html", "reader_html",
        "is_cover", "raw_layout",
    )

    def __init__(self, frontmatter: dict[str, Any], visual_html: str, reader_html: str = ""):
        self.number: int = frontmatter.get("slide", 0)
        self.duration: str = frontmatter.get("duration", "")
        self.raw_layout: str = frontmatter.get("layout", "default")
        self.layout: str = self.raw_layout.lower() if self.raw_layout else "default"
        self.cols: int = int(frontmatter.get("cols", 2))
        self.ratio: str = frontmatter.get("ratio", "1/1")
        self.gap: int = int(frontmatter.get("gap", 16))
        self.accent: str = frontmatter.get("accent", "")
        self.emoji: str = frontmatter.get("emoji", "")
        self.visual_html: str = visual_html
        self.reader_html: str = reader_html
        self.is_cover: bool = (self.number == 1)

    def wrap_visual(self) -> str:
        inner = self.visual_html

        heading = ""
        m = re.match(r"<h[23][^>]*>.*?</h[23]>\s*", inner, re.DOTALL)
        if m:
            heading = m.group(0)
            inner = inner[m.end():]

        inner = re.sub(
            r"<p>\s*(<(?:div class=\"(?:card|callout|steps|diagram)\"[^>]*>.*?</div>))\s*</p>",
            r"\1", inner, flags=re.DOTALL,
        )

        if self.layout == "grid":
            blocks = split_top_level_blocks(inner)
            blocks = [b for b in blocks if b.strip()]
            if blocks:
                # Separate leading card blocks from the rest:
                # cards → grid, everything else → full-width below
                card_end = 0
                for b in blocks:
                    if b.strip().startswith('<div class="card'):
                        card_end += 1
                    else:
                        break
                
                if card_end > 0 and card_end < len(blocks):
                    card_blocks = blocks[:card_end]
                    other_blocks = blocks[card_end:]
                    result = f'<div class="grid-{self.cols}" style="--grid-cols:{self.cols}; --grid-gap:{self.gap}px; gap:{self.gap}px">{"".join(card_blocks)}</div>'
                    result += "".join(other_blocks)
                    return heading + result
                else:
                    grid_html = f'<div class="grid-{self.cols}" style="--grid-cols:{self.cols}; --grid-gap:{self.gap}px; gap:{self.gap}px">{"".join(blocks)}</div>'
                    return heading + grid_html
            return heading + inner

        elif self.layout == "flex":
            inner = f'<div class="flex-row" style="gap:{self.gap}px">{inner}</div>'
        elif self.layout == "stack":
            inner = f'<div class="stack" style="gap:{self.gap}px">{inner}</div>'
        elif self.layout == "split":
            inner = f'<div class="split-layout" style="gap:{self.gap}px">{inner}</div>'
        elif self.layout == "default":
            # Auto-grid consecutive cards only if they appear at the start of content
            # (after heading), preserving content order
            card_count = inner.count('<div class="card')
            if card_count >= 2:
                cards = re.findall(r'<div class="card[^"]*">.*?</div>', inner, re.DOTALL)
                # Check if cards appear at the start (before any non-card, non-whitespace content)
                first_card_pos = inner.find('<div class="card')
                # Only reorder if cards are the first meaningful content
                prefix = inner[:first_card_pos].strip()
                if prefix == '' or prefix.startswith('<p>') and prefix.count('<') == 1:
                    remaining = re.sub(r'<div class="card[^"]*">.*?</div>', '', inner, flags=re.DOTALL)
                    remaining = re.sub(r'<p>\s*</p>', '', remaining)
                    remaining = re.sub(r'\n{2,}', '\n', remaining).strip()
                    cols = min(len(cards), 4)
                    grid_html = f'<div class="grid-{cols}">{"".join(cards)}</div>'
                    return heading + grid_html + remaining
                # Cards are not at start — keep original order, wrap consecutive cards in grid
                inner = re.sub(
                    r'((?:<div class="card[^"]*">.*?</div>\s*)+)',
                    wrap_card_group,
                    inner,
                    flags=re.DOTALL,
                )

        return heading + inner

    def to_dict(self) -> dict[str, Any]:
        """Return slide data for Jinja2 template rendering."""
        return {
            "number": self.number,
            "visual_html": self.wrap_visual(),
            "reader_html": self.reader_html,
            "is_cover": self.is_cover,
        }


# ============================================================================
# Markdown Parsing
# ============================================================================

def extract_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter from Markdown text.

    Returns (frontmatter_dict, body_text).
    Frontmatter must be between --- delimiters at the start of the file.
    """
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        print(f"Warning: Invalid YAML frontmatter: {e}", file=sys.stderr)
        fm = {}

    body = parts[2].strip()
    return fm, body


def parse_meta(filepath: str) -> dict[str, Any]:
    """Parse meta.md and return metadata dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    fm, _ = extract_frontmatter(text)

    if "title" not in fm:
        print(f"Error: meta.md must contain a 'title' field in frontmatter.", file=sys.stderr)
        sys.exit(1)

    return {
        "title": fm["title"],
        "subtitle": fm.get("subtitle", ""),
        "speaker": fm.get("speaker", ""),
        "date": fm.get("date", ""),
        "target_duration": fm.get("target_duration", ""),
        "theme": fm.get("theme", "dark"),
    }


def parse_outline(filepath: str) -> list[dict[str, str]]:
    """Parse outline.md table. Returns list of {num, section, duration, file}."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    _, body = extract_frontmatter(text)

    outline: list[dict[str, str]] = []
    in_table = False

    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("|") and "---" not in line:
            in_table = True
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 4 and cells[0].isdigit():
                outline.append({
                    "num": cells[0],
                    "section": cells[1],
                    "duration": cells[2],
                    "file": cells[3],
                })
        elif in_table and not line.startswith("|"):
            in_table = False

    return outline


def wrap_card_group(m: re.Match) -> str:
    """Wrap consecutive card divs in a grid container."""
    group_cards = re.findall(r'<div class="card[^"]*">.*?</div>', m.group(1), re.DOTALL)
    cols = min(len(group_cards), 4)
    wrapped = ''.join(group_cards).strip()
    return f'<div class="grid-{cols}">{wrapped}</div>'


def split_visual_reader(html: str) -> tuple[str, str]:
    """Split HTML into visual and reader layers at <!-- reader --> markers."""
    pattern = r"<!--\s*reader\s*-->(.*?)<!--\s*/reader\s*-->"
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        return html, ""

    # Everything before the reader block is visual
    visual = html[: match.start()].strip()
    # The reader block content
    reader = match.group(1).strip()

    return visual, reader


def process_custom_tags(html: str) -> str:
    """Convert custom tags to HTML with CSS classes."""

    # <card title="X">...</card>
    def replace_card(m: re.Match) -> str:
        title = m.group(1).replace('<', '&lt;').replace('>', '&gt;')
        content = m.group(2)
        return f'<div class="card"><h4>{title}</h4>{content}</div>'

    html = re.sub(
        r'<card title="(.*?)">(.*?)</card>',
        replace_card,
        html,
        flags=re.DOTALL,
    )

    # <callout type="X">...</callout>
    def replace_callout(m: re.Match) -> str:
        ctype = m.group(1)
        content = m.group(2)
        css_class = f"callout callout-{ctype}" if ctype else "callout"
        return f'<div class="{css_class}">{content}</div>'

    html = re.sub(
        r'<callout type="(.*?)">(.*?)</callout>',
        replace_callout,
        html,
        flags=re.DOTALL,
    )

    # <callout>...</callout> (without type)
    html = re.sub(
        r'<callout>(.*?)</callout>',
        r'<div class="callout">\1</div>',
        html,
        flags=re.DOTALL,
    )

    # <steps>...</steps> containing <step>...</step>
    def replace_steps(m: re.Match) -> str:
        content = m.group(1)
        content = re.sub(
            r'<step>(.*?)</step>',
            r'<div class="step">\1</div>',
            content,
            flags=re.DOTALL,
        )
        return f'<div class="steps">{content}</div>'

    html = re.sub(
        r"<steps>(.*?)</steps>",
        replace_steps,
        html,
        flags=re.DOTALL,
    )

    return html


def extract_mermaid_blocks(md_text: str) -> tuple[str, list[str]]:
    """Extract ```mermaid code blocks before markdown conversion, replacing with placeholders.

    Returns (modified_text, list_of_mermaid_contents).
    """
    blocks = []

    def replace_mermaid_block(m: re.Match) -> str:
        content = m.group(1).strip()
        idx = len(blocks)
        blocks.append(content)
        return f'\n\n@@MERMAID_{idx}@@\n\n'

    modified = re.sub(
        r'```mermaid\s*\n(.*?)```',
        replace_mermaid_block,
        md_text,
        flags=re.DOTALL,
    )
    return modified, blocks


def restore_mermaid_blocks(raw_html: str, mermaid_blocks: list[str]) -> str:
    """Restore mermaid placeholders back to proper mermaid divs."""

    def replace_placeholder(m: re.Match) -> str:
        idx = int(m.group(1))
        content = mermaid_blocks[idx] if idx < len(mermaid_blocks) else m.group(0)
        content = html.escape(content)
        return f'<div class="diagram-focusable" data-focusable><div class="mermaid">\n{content}\n</div></div>'

    return re.sub(
        r'@@MERMAID_(\d+)@@',
        replace_placeholder,
        raw_html,
    )


def parse_slide(filepath: str) -> Optional[Slide]:
    """Parse a single slide .md file into a Slide object."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    fm, body = extract_frontmatter(text)

    # Validate layout
    valid_layouts = {"grid", "flex", "stack", "split", "default"}
    layout = fm.get("layout", "default")
    if layout not in valid_layouts:
        print(f"Warning: {filepath}: unknown layout '{layout}', falling back to 'default'", file=sys.stderr)
        fm["layout"] = "default"

    # Extract mermaid code blocks before markdown conversion
    body, mermaid_blocks = extract_mermaid_blocks(body)

    # Pre-process card titles: escape < and > inside title="..." to prevent HTML parsing issues
    body = re.sub(
        r'(<card\s+title=")(.*?)(">)',
        lambda m: m.group(1) + m.group(2).replace('<', '&lt;').replace('>', '&gt;') + m.group(3),
        body,
    )

    # Convert Markdown body to HTML
    md = markdown.Markdown(
        extensions=["extra", "md_in_html", "codehilite", "fenced_code", "tables"]
    )
    body_html = md.convert(body)

    # Restore mermaid placeholders (must be before process_custom_tags to keep tag content intact)
    body_html = restore_mermaid_blocks(body_html, mermaid_blocks)

    # Process custom tags
    body_html = process_custom_tags(body_html)

    # Restore mermaid placeholders
    body_html = restore_mermaid_blocks(body_html, mermaid_blocks)

    # Split visual/reader layers
    visual_html, reader_html = split_visual_reader(body_html)

    return Slide(
        frontmatter=fm,
        visual_html=visual_html,
        reader_html=reader_html,
    )


# ============================================================================
# HTML Generation
# ============================================================================

def load_override_css(project_dir: str) -> Optional[str]:
    """Load override.css if it exists."""
    css_path = os.path.join(project_dir, "override.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def render_html(
    slides: list[Slide],
    meta: dict[str, Any],
    override_css: Optional[str] = None,
) -> str:
    """Render complete self-contained HTML using Jinja2."""
    template = Template(HTML_TEMPLATE, trim_blocks=True, lstrip_blocks=True)

    slide_dicts = [s.to_dict() for s in slides]

    return template.render(
        slides=slide_dicts,
        meta=meta,
        css=CSS_TEMPLATE.strip(),
        js=JS_TEMPLATE.strip(),
        override_css=override_css.strip() if override_css else None,
    )


def embed_images(html: str, project_dir: str, threshold_bytes: int) -> str:
    """Embed local assets/ images as base64 data URIs when file size ≤ threshold.

    Images above threshold keep ``../assets/`` relative paths.
    HTTP/HTTPS and data: URIs are left untouched.
    """
    assets_dir = os.path.join(project_dir, "assets")

    def _replace_src(m: re.Match) -> str:
        quote = m.group(1)
        path = m.group(2)

        if not path.startswith("assets/"):
            return m.group(0)

        basename = os.path.basename(path)
        img_path = os.path.join(assets_dir, basename)

        if not os.path.isfile(img_path):
            print(f"Warning: Image not found: {img_path}", file=sys.stderr)
            return f'src={quote}../{path}{quote}'

        file_size = os.path.getsize(img_path)

        if file_size <= threshold_bytes:
            mime_type, _ = mimetypes.guess_type(img_path)
            if not mime_type or not mime_type.startswith("image/"):
                mime_type = "image/png"
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f'src={quote}data:{mime_type};base64,{b64}{quote}'
        else:
            return f'src={quote}../{path}{quote}'

    return re.sub(r'src=(["\'])(?!https?://|data:)([^"\']*?)\1', _replace_src, html)


# ============================================================================
# CLI Interface
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markdown presentation to self-contained HTML"
    )
    parser.add_argument(
        "project_dir",
        help="Project directory containing meta.md and slides/",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output HTML file path (default: <project_dir>/output/sharing.html)",
    )
    parser.add_argument(
        "--no-embed", action="store_true", default=False,
        help="Disable base64 image embedding; all images use relative paths",
    )
    parser.add_argument(
        "--embed-threshold", type=float, default=1.0, metavar="MB",
        help="Max image size (MB) to embed as base64 (default: 1.0)",
    )
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)

    # Validate project directory
    if not os.path.isdir(project_dir):
        print(f"Error: '{project_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    meta_path = os.path.join(project_dir, "meta.md")
    slides_dir = os.path.join(project_dir, "slides")

    if not os.path.isfile(meta_path):
        print(f"Error: '{meta_path}' not found.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(slides_dir):
        print(f"Error: '{slides_dir}' directory not found.", file=sys.stderr)
        sys.exit(1)

    # Parse meta
    meta = parse_meta(meta_path)

    # Parse outline (optional)
    outline_path = os.path.join(project_dir, "outline.md")
    outline = parse_outline(outline_path)
    if outline:
        print(f"Found outline with {len(outline)} sections")

    # Parse slides
    slide_files = sorted(
        f for f in os.listdir(slides_dir) if f.endswith(".md")
    )
    if not slide_files:
        print(f"Error: No .md files found in '{slides_dir}'.", file=sys.stderr)
        sys.exit(1)

    slides: list[Slide] = []
    for sf in slide_files:
        slide_path = os.path.join(slides_dir, sf)
        slide = parse_slide(slide_path)
        if slide:
            slides.append(slide)

    if not slides:
        print("Error: No valid slides parsed.", file=sys.stderr)
        sys.exit(1)

    print(f"Parsed {len(slides)} slides")

    # Load override CSS
    override_css = load_override_css(project_dir)
    if override_css:
        print("Found override.css")

    # Render HTML
    html = render_html(slides, meta, override_css)

    if args.no_embed:
        threshold_bytes = -1  #   0 always > threshold → path-fix only
    else:
        threshold_bytes = int(args.embed_threshold * 1024 * 1024)
    html = embed_images(html, project_dir, threshold_bytes)

    # Write output
    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        output_dir = os.path.join(project_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "sharing.html")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
