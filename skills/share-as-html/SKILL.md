---
name: share-as-html
description: Create rich HTML sharing/presentation documents with doc/ppt/zoom modes. Use when creating technical sharing slides, demo presentations, or knowledge sharing HTML docs. Supports dark theme, mermaid diagrams, keyboard navigation.
---

# Sharing Document Skill

Generate self-contained HTML presentation documents with three viewing modes: **Doc** (free scroll), **PPT** (snap slides), and **Zoom** (focus on diagrams/images).

## Trigger Rules

Activate when user mentions:
- "分享"、"演示"、"slides"、"技术分享"、"分享文档"、"分享ppt"
- "用HTML做分享"、"创建演示文档"
- Any request to create an HTML presentation or sharing document

If format is unclear, ask: "用 HTML 分享文档还是其他格式？"

## Content Constraints

**AVOID ASCII diagrams** — Chinese text alignment is unreliable in monospace.
- Use **mermaid** diagrams instead (flowchart, sequence, class, state, gantt, mindmap)
- Use **images** for screenshots or complex diagrams
- Mermaid is preferred for most diagram types

## Workflow

Two paths available. **Prefer Markdown for anything beyond a one-off quick share.**

### Path A: Markdown (Recommended)

Create a Markdown project and convert to HTML with `scripts/md2html.py`.

**Step 1: Create project structure**

```
<project>/
├── meta.md              ← YAML frontmatter: title, subtitle, speaker, date, duration
├── outline.md           ← Markdown table: sections with timing
├── speaker-script.md    ← Presenter script (not rendered to HTML)
├── override.css         ← Optional human CSS overrides
├── slides/
│   ├── 01-cover.md
│   ├── 02-<name>.md
│   └── ...
└── assets/
```

**Step 2: Write Markdown slides**

Each slide file has YAML frontmatter with a `layout.grid` describing the visual structure. The Markdown body is pure content — zero HTML tags.

```yaml
---
slide: 2
duration: 5min
emoji: 🤔
layout:
  grid:
    - [{card: "卡片 A"}, {card: "卡片 B"}]    # row 1: two cards
    - [{callout: "info"}]                      # row 2: full-width callout
---
```

```yaml
# Image slide layout:
layout:
  image:
    src: assets/hero.jpg
    alt: Cover image
    mode: fullscreen  # or "content" (default)
```

**Cell types:**

| Type | YAML | Slot body |
|------|------|-----------|
| `card` | `{card: "标题"}` | Markdown content inside the card |
| `callout` | `{callout: "variant"}` | Markdown content (variant: info, warning, tip, danger) |
| `steps` | `{steps: null}` | Numbered list (rendered with `.step` CSS) |
| `metrics` | `{metrics: null}` | `值 : 标签` lines, one per metric |
| `split` | `{split: null}` | Two consecutive slots → left/right columns |
| `raw` | `{raw: null}` | Plain markdown, no container wrapper |
| `image` | `{image: {src, alt, mode}}` | Single image as slide content (mode: fullscreen or content) |

**Slot delimiter** — `=== slot ===` separates cell content in body:

```markdown
---
slide: 3
layout:
  grid:
    - [{card: "左卡片"}, {card: "右卡片"}]
---

## 页面标题

卡片 A 的内容。**粗体** 和 `行内代码` 正常。

=== slot ===

卡片 B 的内容。代码块也正常工作：

```
echo "hello"
```

=== slot ===

**提示** 这是 callout 里的内容。
```

- Each cell in the grid maps to one content slot, in row-major order
- Heading (first `##`) belongs before the first `=== slot ===`
- Mermaid code blocks inside slots work normally
- `<!-- reader -->...<!-- /reader -->` markers inside slots for DOC mode content

**Step 3: Convert to HTML**

```bash
python scripts/md2html.py <project_dir> [-o <output.html>]
```

Dependencies: `pip install markdown PyYAML jinja2`

**Step 4: Open in browser**

```bash
xdg-open <project_dir>/output/sharing.html    # Linux
open <project_dir>/output/sharing.html        # macOS
```

### Path B: Direct HTML (Quick/Draft)

For simple one-off shares, generate HTML directly.

**Step 1**: Ask user where to save.

**Step 2**: Generate self-contained HTML with inline CSS/JS. Use the CSS Template and JS Template below.

**Step 3**: Write to file and open in browser.

---

## CSS Template

Copy this ENTIRE CSS block into the `<style>` tag of generated HTML:

```css
/* ===== Reset & Variables ===== */
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

/* ===== Base Styles ===== */
html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, 'SF Pro Display', 'PingFang SC', 'Noto Sans SC', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

code, pre {
    font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
}

/* ===== Slide Container (Doc Mode Default) ===== */
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

/* ===== Cover Slide ===== */
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

/* ===== Content Container ===== */
.content {
    max-width: 900px;
    width: 100%;
}

/* ===== Typography ===== */
h2 {
    font-size: clamp(24px, 4vw, 36px);
    font-weight: 600;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

h2 .emoji {
    font-size: 32px;
}

h3 {
    font-size: clamp(17px, 2.5vw, 22px);
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 16px;
    margin-top: 24px;
}

p {
    margin-bottom: 12px;
    color: var(--text);
    font-size: clamp(14px, 1.5vw, 16px);
}

/* ===== Points / List Items ===== */
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

.point::before {
    content: '';
}

/* ===== Cards ===== */
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

.card p {
    font-size: 14px;
    color: var(--text-dim);
}

/* ===== Grid Layout ===== */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 16px 0;
}

@media (max-width: 768px) {
    .grid-2 {
        grid-template-columns: 1fr;
    }
}

/* ===== Code Blocks ===== */
pre {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    overflow-x: auto;
}

pre code {
    font-size: 14px;
    line-height: 1.5;
    color: var(--text);
}

code {
    background: var(--surface);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
}

/* Syntax Highlighting Classes */
.cmd { color: var(--green); }
.comment { color: var(--text-dim); }
.string { color: var(--yellow); }
.keyword { color: var(--accent2); }

/* ===== Tags ===== */
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

/* ===== Metrics ===== */
.metrics-row {
    display: flex;
    gap: 24px;
    margin: 16px 0;
    flex-wrap: wrap;
}

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

.metric .value {
    font-size: 32px;
    font-weight: 700;
    color: var(--accent);
}

.metric .label {
    font-size: 13px;
    color: var(--text-dim);
    margin-top: 4px;
}

/* ===== Flow / Numbered List ===== */
.flow {
    counter-reset: flow-counter;
    margin: 16px 0;
}

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

/* ===== Tables ===== */
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

td {
    font-size: 14px;
}

tr:hover td {
    background: rgba(56, 189, 248, 0.04);
}

/* ===== Custom List ===== */
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
    content: '▸';
    position: absolute;
    left: 0;
    color: var(--accent);
    font-weight: bold;
}

/* ===== Mermaid ===== */
.mermaid {
    display: flex;
    justify-content: center;
    margin: 16px 0;
}

.mermaid svg {
    max-width: 100%;
    height: auto;
}

/* ===== Diagram Focus State ===== */
.diagram-focusable {
    cursor: pointer;
    border: 2px solid transparent;
    border-radius: 8px;
    transition: border-color 0.2s;
    padding: 4px;
}

.diagram-focusable.focused {
    border-color: var(--accent);
}

/* ===== No-Focus State ===== */
.diagram-focusable.no-focus {
    opacity: 0.6;
    cursor: default;
    border-color: transparent !important;
}

.diagram-focusable.no-focus:hover {
    border-color: transparent !important;
}

/* ===== Image Slide Layout ===== */
.slide-image-fullscreen {
    /* DOC mode: constrains to content area, inherits slide padding */
}

.slide-image-fullscreen img {
    max-width: 900px;
    width: 100%;
    height: auto;
    object-fit: contain;
}

.slide-image-content img {
    width: 100%;
    height: auto;
    object-fit: contain;
}

/* ===== PPT Mode (Snap Scrolling) ===== */
body.mode-ppt {
    overflow: hidden;
}

body.mode-ppt .slide {
    min-height: 100vh;
    padding: 60px 80px;
    border-bottom: 1px solid var(--border);
    scroll-snap-align: start;
    scroll-snap-stop: always;
    align-items: center;
}

body.mode-ppt .slide .content { max-width: 1100px; }

#scroll-container.mode-ppt {
    scroll-snap-type: y proximity;
    overflow-y: scroll;
    overflow-x: auto;
    height: 100vh;
}

body.mode-ppt .slide-image-fullscreen {
    min-height: 100vh;
    padding: 0;
    overflow: hidden;
    position: relative;
}

body.mode-ppt .slide-image-fullscreen img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    position: absolute;
    top: 0;
    left: 0;
    max-width: none;
}

/* ===== Bounce Animations ===== */
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

/* ===== Zoom Mode ===== */
body.mode-zoom .slide {
    display: none;
}

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

body.mode-zoom .zoom-content {
    /* No size restrictions — let container scroll */
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
    .slide { padding: 24px 16px; }
    body.mode-ppt .slide { padding: 40px 20px; }
    .grid-2, .grid-3, .grid-4, .split-layout { grid-template-columns: 1fr; }
    .flex-row { flex-direction: column; }
    body.mode-ppt .slide-image-fullscreen { min-height: 60vh; }
    body.mode-ppt .slide-image-fullscreen img { object-fit: contain; }
}

/* ===== Doc Footer (DOC mode only) ===== */
.doc-footer {
    text-align: center;
    padding: 24px 0 32px 0;
    font-size: 12px;
    color: var(--text-dim);
    border-top: 1px solid var(--surface2);
    margin-top: 48px;
}

.doc-footer a {
    color: var(--text-dim);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.doc-footer a:hover {
    color: var(--accent);
}

.doc-footer img {
    vertical-align: middle;
}

body.mode-ppt .doc-footer,
body.mode-zoom .doc-footer {
    display: none;
}
```

---

## JavaScript Template

Copy this ENTIRE JS block into the `<script>` tag of generated HTML:

```javascript
// ===== State Machine =====
let currentState = 'DOC'; // DOC | PPT_FULL | PPT_ZOOM
let currentSlideIndex = 0;
let focusedDiagramIndex = -1;
let isAtScrollBoundary = false;
let zoomTarget = null;

// ===== Keyboard Handler =====
document.addEventListener('keydown', (e) => {
    const slides = document.querySelectorAll('.slide');
    
    switch(currentState) {
        case 'DOC':
            if (e.key === 'Enter') {
                e.preventDefault();
                enterPPTMode();
            }
            // Arrow keys use default scroll behavior in doc mode
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

// ===== Mode Switch Functions =====
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

// ===== Navigation Functions =====
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

function updateFocus(preserveIndex = false) {
    const savedIndex = focusedDiagramIndex;
    clearFocus();
    if (!preserveIndex) isAtScrollBoundary = false;
    const slide = document.querySelectorAll('.slide')[currentSlideIndex];
    if (!slide) return;
    
    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
        .filter(el => !el.classList.contains('no-focus'));
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
    document.querySelectorAll('.diagram-focusable.focused').forEach(el => {
        el.classList.remove('focused');
    });
    focusedDiagramIndex = -1;
}

function handleFocusSwitch(key) {
    const slide = document.querySelectorAll('.slide')[currentSlideIndex];
    if (!slide) return;
    
    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
        .filter(el => !el.classList.contains('no-focus'));
    if (focusables.length <= 1) return;
    
    let newIndex;
    if (key === 'ArrowRight') {
        newIndex = Math.min(focusedDiagramIndex + 1, focusables.length - 1);
    } else {
        newIndex = Math.max(focusedDiagramIndex - 1, 0);
    }
    
    focusedDiagramIndex = newIndex;
    
    document.querySelectorAll('.diagram-focusable.focused').forEach(el => {
        el.classList.remove('focused');
    });
    focusables[focusedDiagramIndex].classList.add('focused');
}

// ===== Zoom Scroll Functions =====
function scrollZoomContainer(direction) {
    const container = document.querySelector('.zoom-container');
    if (!container) return false;
    
    const scrollAmount = 100;
    const { scrollTop, scrollLeft, scrollHeight, scrollWidth, clientHeight, clientWidth } = container;
    
    switch(direction) {
        case 'up':
            if (scrollTop <= 0) return false;
            container.scrollTop -= scrollAmount;
            return true;
        case 'down':
            if (scrollTop + clientHeight >= scrollHeight) return false;
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

// ===== Scroll Within Slide Functions =====
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
        .filter(el => !el.classList.contains('no-focus'));
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
    
    setTimeout(() => {
        container.style.scrollSnapType = oldSnap || 'y proximity';
    }, 500);
    
    return true;
}

function triggerBounce(direction, axis) {
    const container = document.getElementById('scroll-container');
    if (!container) return;
    
    const bounceClass = axis === 'y'
        ? (direction > 0 ? 'bounce-down' : 'bounce-up')
        : (direction > 0 ? 'bounce-right' : 'bounce-left');
    
    container.classList.add(bounceClass);
    setTimeout(() => container.classList.remove(bounceClass), 300);
}

// ===== Mermaid Initialization =====
window.addEventListener('load', () => {
    document.querySelectorAll('.mermaid svg, img').forEach(el => {
        const rect = el.getBoundingClientRect();
        const needsZoom = rect.width > window.innerWidth || rect.height > window.innerHeight;
        if (needsZoom) {
            const wrapper = el.closest('.diagram-focusable') || el.parentElement;
            if (wrapper) wrapper.classList.add('needs-zoom');
        }
    });
});
```

---

## HTML Structure Templates

### Standard Slide

```html
<div class="slide">
    <span class="slide-number">N</span>
    <div class="content">
        <h2><span class="emoji">X</span> 标题</h2>
        内容...
    </div>
</div>
```

### Cover Slide

```html
<div class="slide cover">
    <div>
        <h1>标题</h1>
        <p class="subtitle">副标题</p>
        <p class="meta">作者 · 日期</p>
    </div>
</div>
```

### Image Slide (Fullscreen)

```html
<div class="slide slide-image-fullscreen">
    <span class="slide-number">N</span>
    <img src="assets/hero.jpg" alt="Cover illustration">
</div>
```

### Image Slide (Content)

```html
<div class="slide slide-image-content">
    <span class="slide-number">N</span>
    <div class="content">
        <img src="assets/diagram.jpg" alt="Diagram">
    </div>
</div>
```

### Image with Zoom Support

```html
<div class="diagram-focusable" data-focusable>
    <img src="..." alt="..." style="max-width: 100%; height: auto;">
</div>
```

### Mermaid Diagram

```html
<div class="diagram-focusable" data-focusable>
    <div class="mermaid">
        graph TD
            A[开始] --> B{判断}
            B -->|是| C[处理]
            B -->|否| D[结束]
    </div>
</div>
```

### No-Focus Diagrams

To make a diagram non-focusable (skipped during left/right navigation), add the `.no-focus` class:

```html
<div class="diagram-focusable no-focus" data-focusable>
    <img src="..." alt="decorative image">
</div>
```

Visual effect: semi-transparent (opacity: 0.6), no hover effect, skipped during focus switching.

### Grid Layout

```html
<div class="grid-2">
    <div class="card">
        <h4>标题</h4>
        <p>内容</p>
    </div>
    <div class="card">
        <h4>标题</h4>
        <p>内容</p>
    </div>
</div>
```

### Code Block

```html
<pre><code><span class="comment"># 注释</span>
<span class="cmd">$</span> command <span class="string">"arg"</span>
<span class="keyword">keyword</span> value</code></pre>
```

### Metrics Row

```html
<div class="metrics-row">
    <div class="metric">
        <span class="value">42</span>
        <span class="label">标签</span>
    </div>
    <div class="metric">
        <span class="value">100%</span>
        <span class="label">完成率</span>
    </div>
</div>
```

### Points List

```html
<div class="point">普通要点</div>
<div class="point highlight">高亮要点</div>
<div class="point star">重要要点</div>
```

### Flow / Numbered Steps

```html
<div class="flow">
    <div class="flow-item">第一步描述</div>
    <div class="flow-item">第二步描述</div>
    <div class="flow-item">第三步描述</div>
</div>
```

### Tags

```html
<span class="tag">默认</span>
<span class="tag tag-blue">蓝色</span>
<span class="tag tag-green">绿色</span>
<span class="tag tag-orange">橙色</span>
<span class="tag tag-purple">紫色</span>
```

---

## Complete HTML Skeleton

Use this as the starting template for generated documents:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标题</title>
    <style>
        /* [PASTE FULL CSS HERE] */
    </style>
</head>
<body>
    <div id="scroll-container">
        <!-- Slide 1: Cover -->
        <div class="slide cover">
            <div>
                <h1>标题</h1>
                <p class="subtitle">副标题</p>
                <p class="meta">作者 · 日期</p>
            </div>
        </div>

        <!-- Slide 2+: Content -->
        <div class="slide">
            <span class="slide-number">2</span>
            <div class="content">
                <h2><span class="emoji">X</span> 标题</h2>
                <!-- content here -->
            </div>
        </div>

        <!-- More slides... -->

        <div class="doc-footer">
            <a href="https://github.com/ovotop/share-as-html" target="_blank" rel="noopener">
                Powered by <img src="https://avatars.githubusercontent.com/u/61374409?s=96&v=4" alt="ovotop" width="48" height="48"> ovotop/share-as-html
            </a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'dark' });
        /* [PASTE FULL JS HERE] */
    </script>
</body>
</html>
```

---

## Mermaid Guide

### CDN
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
```

### Initialization
```javascript
mermaid.initialize({ startOnLoad: true, theme: 'dark' });
```

### Supported Diagram Types
- `graph TD` / `graph LR` — Flowchart
- `sequenceDiagram` — Sequence diagram
- `classDiagram` — Class diagram
- `stateDiagram-v2` — State diagram
- `gantt` — Gantt chart
- `mindmap` — Mind map

### Usage Rules
- Wrap in `<div class="mermaid">` tags, NOT markdown code fences
- Use `data-focusable` on parent div to enable zoom mode
- Keep diagrams simple; complex ones may not render well

### Example
```html
<div class="diagram-focusable" data-focusable>
    <div class="mermaid">
        sequenceDiagram
            participant A as 用户
            participant B as 系统
            A->>B: 请求
            B-->>A: 响应
    </div>
</div>
```

---

## Image Guide

- Recommended width: ≤ 1200px for full display
- Larger images may trigger zoom mode automatically
- Use `data-focusable` attribute on wrapper to enable focus/zoom
- Always include `alt` text for accessibility

### Image Slide Modes

- **Fullscreen mode** (`slide-image-fullscreen`): image fills entire slide with `object-fit: cover` — may crop edges. Best for cover photos or section dividers.
- **Content mode** (`slide-image-content`): image fits within 16:9 content area with `object-fit: contain` — letterboxed if aspect ratio differs. Best for diagrams or screenshots.

### Example
```html
<div class="diagram-focusable" data-focusable>
    <img src="screenshot.png" alt="功能截图" style="max-width: 100%; height: auto;">
</div>
```

---

## Keyboard Reference

| Mode | Key | Action |
|------|-----|--------|
| DOC | `Enter` | Enter PPT mode |
| DOC | Arrow keys | Normal scroll |
| PPT | `Esc` | Back to DOC mode |
| PPT | `↓` / `Space` | Scroll content / Next slide |
| PPT | `↑` | Scroll content / Previous slide |
| PPT | `←` / `→` | Scroll content / Switch focus |
| PPT | `Enter` | Zoom into focused diagram |
| ZOOM | `Esc` | Exit zoom, back to PPT |
| ZOOM | Arrow keys | Scroll zoomed content |
| ZOOM | `↑` at top | Exit zoom, go to prev slide |
| ZOOM | `↓` at bottom | Exit zoom, go to next slide |
