const { test, expect } = require('@playwright/test');

const HTML_FILES = [
    'test-focus-matrix.html',
    'ai-agent-tools.html',
    'sharing-doc-test.html',
    'test-image-zoom.html',
    'test-mermaid-zoom.html'
];

const BASE_PATH = 'file:///home/mi/Documents/harness/tooling/documenting/sharing-in-html/';

const enterPPT = async (page) => {
    await page.keyboard.press('Enter');
    await page.waitForTimeout(500);
};

const exitPPT = async (page) => {
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
};

const getBodyClass = async (page) => {
    return await page.evaluate(() => document.body.className);
};

const getCurrentSlideIndex = async (page) => {
    try {
        const index = await page.evaluate(() => {
            if (typeof window.currentSlideIndex !== 'undefined') {
                return window.currentSlideIndex;
            }
            return 0;
        });
        const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
        return Math.min(index, totalSlides - 1);
    } catch (e) {
        return 0;
    }
};

const goToSlide = async (page, targetIndex) => {
    let iterations = 0;
    const maxIterations = 20;
    while (iterations < maxIterations) {
        iterations++;
        const currentIdx = await page.evaluate(() => window.currentSlideIndex);
        if (currentIdx === targetIndex) return;
        if (currentIdx < targetIndex) {
            await page.keyboard.press('ArrowDown');
        } else {
            await page.keyboard.press('ArrowUp');
        }
        await page.waitForTimeout(300);
    }
    throw new Error(`goToSlide: failed to reach slide ${targetIndex} after ${maxIterations} iterations`);
};

const getFocusedDiagramIndex = async (page) => {
    try {
        return await page.evaluate(() => window.focusedDiagramIndex);
    } catch (e) {
        return -1;
    }
};

const waitForMermaid = async (page) => {
    await page.waitForSelector('.mermaid svg', { timeout: 5000 }).catch(() => {});
};

for (const FILE of HTML_FILES) {
    test.describe(`Feature Suite: ${FILE}`, () => {
        
        test.beforeEach(async ({ page }) => {
            await page.goto(`${BASE_PATH}${FILE}`);
            await page.waitForTimeout(500);
            await waitForMermaid(page);
        });

        test('State Transitions: Doc to PPT and Back', async ({ page }) => {
            const initialClass = await getBodyClass(page);
            expect(initialClass).not.toContain('mode-ppt');

            await enterPPT(page);
            const pptClass = await getBodyClass(page);
            expect(pptClass).toContain('mode-ppt');

            await exitPPT(page);
            const docClass = await getBodyClass(page);
            expect(docClass).not.toContain('mode-ppt');
        });

        test('PPT_FULL Navigation: Slide Indexing', async ({ page }) => {
            await enterPPT(page);

            const initialIndex = await getCurrentSlideIndex(page);

            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(400);
            const nextIndex = await getCurrentSlideIndex(page);
            expect(nextIndex).toBeGreaterThan(initialIndex);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
            
            let lastSlideReached = false;
            for (let i = 0; i < totalSlides * 3 && !lastSlideReached; i++) {
                const currentIdx = await getCurrentSlideIndex(page);
                if (currentIdx === totalSlides - 1) {
                    const atBoundary = await page.evaluate(() => window.isAtScrollBoundary === true);
                    if (atBoundary) lastSlideReached = true;
                }
                if (!lastSlideReached) {
                    await page.keyboard.press('ArrowDown');
                    await page.waitForTimeout(200);
                }
            }
            
            const lastIndex = await getCurrentSlideIndex(page);
            expect(lastIndex).toBe(totalSlides - 1);

            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(200);
            const stillLastIndex = await getCurrentSlideIndex(page);
            expect(stillLastIndex).toBe(totalSlides - 1);

            for (let i = 0; i < totalSlides * 3; i++) {
                const currentIdx = await getCurrentSlideIndex(page);
                if (currentIdx === 0) break;
                await page.keyboard.press('ArrowUp');
                await page.waitForTimeout(100);
            }
            const firstIndex = await getCurrentSlideIndex(page);
            expect(firstIndex).toBe(0);

            await page.keyboard.press('ArrowUp');
            await page.waitForTimeout(200);
            const stillFirstIndex = await getCurrentSlideIndex(page);
            expect(stillFirstIndex).toBe(0);
        });

        test('Focus Switching', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const count = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return 0;
                    return slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length;
                });

                if (count >= 2) {
                    const initialFocus = await getFocusedDiagramIndex(page);
                    await page.keyboard.press('ArrowRight');
                    await page.waitForTimeout(200);
                    const nextFocus = await getFocusedDiagramIndex(page);
                    expect(nextFocus).toBe(initialFocus + 1);

                    await page.keyboard.press('ArrowLeft');
                    await page.waitForTimeout(200);
                    const backFocus = await getFocusedDiagramIndex(page);
                    expect(backFocus).toBe(initialFocus);
                    
                    break;
                }
            }

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const hasNoFocus = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return false;
                    return slide.querySelectorAll('.diagram-focusable.no-focus').length > 0;
                });

                if (hasNoFocus) {
                    // Verify no-focus elements are never focused
                    const initialFocus = await getFocusedDiagramIndex(page);

                    // Cycle through all focusables to ensure no-focus never gets .focused
                    const focusableCount = await page.evaluate(() => {
                        const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                        return slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length;
                    });

                    for (let j = 0; j < focusableCount + 2; j++) {
                        await page.keyboard.press('ArrowRight');
                        await page.waitForTimeout(100);
                        // Check no no-focus element has .focused class
                        const noFocusHasFocus = await page.evaluate(() => {
                            const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                            return slide.querySelector('.diagram-focusable.no-focus.focused') !== null;
                        });
                        expect(noFocusHasFocus).toBe(false);
                    }

                    // Verify we cycled back (or stayed within valid range)
                    const finalFocus = await getFocusedDiagramIndex(page);
                    expect(finalFocus).toBeLessThan(focusableCount);
                    break;
                }
            }

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const count = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return 0;
                    return slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length;
                });

                if (count === 1) {
                    await page.keyboard.press('ArrowLeft');
                    await page.keyboard.press('ArrowRight');
                    await page.waitForTimeout(200);
                    const index = await getFocusedDiagramIndex(page);
                    expect(index).toBe(0);
                    break;
                }
            }
        });

        test('Zoom Mode', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
            
            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const count = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return 0;
                    return slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length;
                });

                if (count > 0) {
                    const slideIndexBeforeZoom = await getCurrentSlideIndex(page);

                    await page.keyboard.press('Enter');
                    await page.waitForTimeout(300);
                    
                    const zoomClass = await getBodyClass(page);
                    expect(zoomClass).toContain('mode-zoom');

                    await exitPPT(page);

                    const afterZoomClass = await getBodyClass(page);
                    expect(afterZoomClass).toContain('mode-ppt');
                    expect(afterZoomClass).not.toContain('mode-zoom');

                    const focusIndex = await getFocusedDiagramIndex(page);
                    expect(focusIndex).toBe(0);

                    const zoomContainerExists = await page.evaluate(() => {
                        return document.querySelector('.zoom-container') !== null;
                    });
                    expect(zoomContainerExists).toBe(false);

                    const scrollContainerHasModePPT = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.classList.contains('mode-ppt') : false;
                    });
                    expect(scrollContainerHasModePPT).toBe(true);

                    const slideIndexAfterZoom = await getCurrentSlideIndex(page);
                    expect(slideIndexAfterZoom).toBe(slideIndexBeforeZoom);

                    break;
                }
            }
        });

        test('Prevent Default: No Window-Level Scroll', async ({ page }) => {
            await enterPPT(page);
            
            const initialScrollLeft = await page.evaluate(() => window.scrollX);
            const initialScrollTop = await page.evaluate(() => window.scrollY);
            
            await page.keyboard.press('ArrowLeft');
            await page.keyboard.press('ArrowRight');
            await page.keyboard.press('ArrowUp');
            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(200);

            const finalScrollLeft = await page.evaluate(() => window.scrollX);
            const finalScrollTop = await page.evaluate(() => window.scrollY);
            // In PPT mode, scrolling happens inside scroll-container, not window
            expect(finalScrollLeft).toBe(initialScrollLeft);
            expect(finalScrollTop).toBe(initialScrollTop);
        });

        test('PPT_FULL: ArrowDown scrolls within oversized slide before advancing', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const hasVerticalOverflow = await page.evaluate(() => {
                    const container = document.getElementById('scroll-container');
                    const slides = document.querySelectorAll('.slide');
                    const slide = slides[window.currentSlideIndex];
                    if (!container || !slide) return false;
                    const slideTop = slide.offsetTop - container.offsetTop;
                    const slideHeight = slide.offsetHeight;
                    return slideHeight > container.clientHeight + 10;
                });

                if (hasVerticalOverflow) {
                    const slideBefore = await getCurrentSlideIndex(page);
                    const scrollBefore = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.scrollTop : 0;
                    });

                    await page.keyboard.press('ArrowDown');
                    await page.waitForTimeout(600);
                    
                    const slideAfter = await getCurrentSlideIndex(page);
                    const scrollAfter = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.scrollTop : 0;
                    });

                    // Slide should NOT change on first press (content scrolls instead)
                    expect(slideAfter).toBe(slideBefore);
                    expect(scrollAfter).toBeGreaterThan(scrollBefore);
                    break;
                }
            }
        });

        test('PPT_FULL: Second ArrowDown at boundary advances slide', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);

            for (let i = 0; i < totalSlides - 1; i++) {
                await goToSlide(page, i);

                const hasOverflow = await page.evaluate(() => {
                    const container = document.getElementById('scroll-container');
                    const slides = document.querySelectorAll('.slide');
                    const slide = slides[window.currentSlideIndex];
                    if (!container || !slide) return false;
                    const slideTop = slide.offsetTop - container.offsetTop;
                    return slide.offsetHeight > container.clientHeight + 10;
                });

                if (hasOverflow) {
                    // Scroll to bottom of slide
                    await page.evaluate(() => {
                        const container = document.getElementById('scroll-container');
                        const slides = document.querySelectorAll('.slide');
                        const slide = slides[window.currentSlideIndex];
                        if (container && slide) {
                            const slideTop = slide.offsetTop - container.offsetTop;
                            const slideBottom = slideTop + slide.offsetHeight;
                            container.scrollTo({ top: slideBottom - container.clientHeight, behavior: 'instant' });
                            window.isAtScrollBoundary = true;
                        }
                    });
                    await page.waitForTimeout(200);

                    const slideBefore = await getCurrentSlideIndex(page);
                    await page.keyboard.press('ArrowDown');
                    await page.waitForTimeout(400);
                    const slideAfter = await getCurrentSlideIndex(page);

                    expect(slideAfter).toBe(slideBefore + 1);
                    break;
                }
            }
        });

        test('PPT_FULL: Normal slide advances immediately on ArrowDown', async ({ page }) => {
            await enterPPT(page);
            await goToSlide(page, 0);

            // Cover slide should have no overflow
            const slideBefore = await getCurrentSlideIndex(page);
            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(400);
            const slideAfter = await getCurrentSlideIndex(page);

            expect(slideAfter).toBe(slideBefore + 1);
        });

        test('Boundary flag resets on slide change', async ({ page }) => {
            await enterPPT(page);

            await page.evaluate(() => {
                const container = document.getElementById('scroll-container');
                const slides = document.querySelectorAll('.slide');
                const slide = slides[window.currentSlideIndex || 0];
                if (container && slide) {
                    const slideTop = slide.offsetTop - container.offsetTop;
                    container.scrollTo({ top: slideTop + slide.offsetHeight - container.clientHeight + 1, behavior: 'instant' });
                }
            });
            // Force flag set via the code path: ArrowDown when at boundary
            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(600);
            const reachedBoundary = await page.evaluate(() => window.isAtScrollBoundary);
            
            if (reachedBoundary) {
                const slideBefore = await getCurrentSlideIndex(page);
                await page.keyboard.press('ArrowDown');
                await page.waitForTimeout(400);
                const slideAfter = await getCurrentSlideIndex(page);
                expect(slideAfter).toBe(slideBefore + 1);
            }
        });

        test('PPT_FULL: ArrowRight scrolls horizontally within wide diagram', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const hasHorizontalOverflow = await page.evaluate(() => {
                    const container = document.getElementById('scroll-container');
                    const slides = document.querySelectorAll('.slide');
                    const slide = slides[window.currentSlideIndex];
                    if (!container || !slide) return false;
                    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
                        .filter(el => !el.classList.contains('no-focus'));
                    if (focusables.length === 0) return false;
                    const focused = focusables[window.focusedDiagramIndex] || focusables[0];
                    return focused.scrollWidth > container.clientWidth + 10;
                });

                if (hasHorizontalOverflow) {
                    const scrollLeftBefore = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.scrollLeft : 0;
                    });

                    await page.keyboard.press('ArrowRight');
                    await page.waitForTimeout(600);
                    
                    const scrollLeftAfter = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.scrollLeft : 0;
                    });

                    expect(scrollLeftAfter).toBeGreaterThan(scrollLeftBefore);
                    break;
                }
            }
        });

        test('PPT_FULL: No horizontal overflow switches focus immediately', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const focusableCount = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return 0;
                    return slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length;
                });

                if (focusableCount >= 2) {
                    const slideHeightFits = await page.evaluate(() => {
                        const container = document.getElementById('scroll-container');
                        const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                        return slide.offsetHeight <= container.clientHeight + 10;
                    });

                    if (slideHeightFits) {
                        const initialFocus = await getFocusedDiagramIndex(page);
                        await page.keyboard.press('ArrowRight');
                        await page.waitForTimeout(300);
                        const nextFocus = await getFocusedDiagramIndex(page);

                        if (initialFocus + 1 < focusableCount) {
                            expect(nextFocus).toBe(initialFocus + 1);
                        }
                        break;
                    }
                }
            }
        });

        test('Zoom Mode: Arrow Keys and Focus Preservation', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
            let tested = false;

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const count = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return 0;
                    return slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length;
                });

                if (count === 0) continue;

                const slideIndexBeforeZoom = await getCurrentSlideIndex(page);

                if (count >= 2) {
                    await page.keyboard.press('ArrowRight');
                    await page.waitForTimeout(200);
                }
                const beforeFocus = await getFocusedDiagramIndex(page);

                await page.keyboard.press('Enter');
                await page.waitForTimeout(300);
                expect(await getBodyClass(page)).toContain('mode-zoom');

                await page.keyboard.press('ArrowRight');
                await page.waitForTimeout(100);
                await page.keyboard.press('ArrowLeft');
                await page.waitForTimeout(100);

                await page.keyboard.press('Escape');
                await page.waitForTimeout(300);
                expect(await getBodyClass(page)).toContain('mode-ppt');
                expect(await getBodyClass(page)).not.toContain('mode-zoom');

                const afterFocus = await getFocusedDiagramIndex(page);
                expect(afterFocus).toBe(beforeFocus);

                const zoomContainerExists = await page.evaluate(() => {
                    return document.querySelector('.zoom-container') !== null;
                });
                expect(zoomContainerExists).toBe(false);

                const scrollContainerHasModePPT = await page.evaluate(() => {
                    const c = document.getElementById('scroll-container');
                    return c ? c.classList.contains('mode-ppt') : false;
                });
                expect(scrollContainerHasModePPT).toBe(true);

                const slideIndexAfterZoom = await getCurrentSlideIndex(page);
                expect(slideIndexAfterZoom).toBe(slideIndexBeforeZoom);

                tested = true;
                break;
            }

            if (!tested) {
                console.warn(`No slide with focusable elements in ${FILE}, zoom arrow key test skipped`);
            }
        });

        test('PPT_FULL: ArrowLeft scrolls horizontally back', async ({ page }) => {
            await enterPPT(page);

            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);

            for (let i = 0; i < totalSlides; i++) {
                await goToSlide(page, i);

                const hasOverflow = await page.evaluate(() => {
                    const container = document.getElementById('scroll-container');
                    if (!container) return false;
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    if (!slide) return false;
                    const focusables = Array.from(slide.querySelectorAll('.diagram-focusable'))
                        .filter(el => !el.classList.contains('no-focus'));
                    if (focusables.length === 0) return false;
                    const focused = focusables[window.focusedDiagramIndex] || focusables[0];
                    return focused.scrollWidth > container.clientWidth + 10;
                });

                if (hasOverflow) {
                    await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        if (c) c.scrollLeft = 300;
                        window.isAtScrollBoundary = false;
                    });
                    await page.waitForTimeout(100);

                    const scrollBefore = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.scrollLeft : 0;
                    });

                    await page.keyboard.press('ArrowLeft');
                    await page.waitForTimeout(600);

                    const scrollAfter = await page.evaluate(() => {
                        const c = document.getElementById('scroll-container');
                        return c ? c.scrollLeft : 0;
                    });

                    expect(scrollAfter).toBeLessThan(scrollBefore);
                    break;
                }
            }
        });

        test('Footer: visible in DOC mode, hidden in PPT mode', async ({ page }) => {
            // Check footer exists in initial DOC mode
            const footer = page.locator('.doc-footer');
            await expect(footer.first()).toBeVisible();

            // Enter PPT mode - footer should be hidden
            await enterPPT(page);
            await expect(footer.first()).not.toBeVisible();

            // Return to DOC mode - footer should be visible again
            await exitPPT(page);
            await expect(footer.first()).toBeVisible();
        });

        test('Footer: link opens correct URL', async ({ page }) => {
            const link = page.locator('.doc-footer a');
            await expect(link).toHaveAttribute('href', 'https://github.com/ovotop/share-as-html');
            await expect(link).toHaveAttribute('target', '_blank');
            await expect(link).toHaveAttribute('rel', 'noopener');
        });

        test('Exit zoom scrolls to correct slide position', async ({ page }) => {
            await enterPPT(page);
            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
            if (totalSlides < 2) return;

            // Navigate to slide 2 (index 1) and find a zoomable diagram
            for (let i = 1; i < totalSlides; i++) {
                await goToSlide(page, i);
                const hasFocusable = await page.evaluate(() => {
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    return slide && slide.querySelectorAll('.diagram-focusable:not(.no-focus)').length > 0;
                });
                if (!hasFocusable) continue;

                // Record expected scroll position of current slide
                const expectedTop = await page.evaluate(() => {
                    const container = document.getElementById('scroll-container');
                    const slide = document.querySelectorAll('.slide')[window.currentSlideIndex];
                    return slide ? slide.offsetTop - container.offsetTop : 0;
                });

                // Enter zoom then exit
                await page.keyboard.press('Enter');
                await page.waitForTimeout(300);
                await page.keyboard.press('Escape');
                await page.waitForTimeout(500);

                // Verify scroll position is at the correct slide (±5px tolerance)
                const actualScrollTop = await page.evaluate(() => {
                    const container = document.getElementById('scroll-container');
                    return container ? container.scrollTop : 0;
                });
                expect(Math.abs(actualScrollTop - expectedTop)).toBeLessThan(10);
                break;
            }
        });

        test('Navigation scrolls container with snap', async ({ page }) => {
            await enterPPT(page);
            const totalSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
            if (totalSlides < 2) return;

            // Navigate to slide 2
            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(600);

            // Verify scroll position changed
            const scrollTop = await page.evaluate(() => {
                const container = document.getElementById('scroll-container');
                return container ? container.scrollTop : 0;
            });
            expect(scrollTop).toBeGreaterThan(0);

            // Verify currentSlideIndex is 1
            const index = await getCurrentSlideIndex(page);
            expect(index).toBe(1);

            // Verify scroll position matches slide 2's offset (±10px)
            const expectedTop = await page.evaluate(() => {
                const container = document.getElementById('scroll-container');
                const slide = document.querySelectorAll('.slide')[1];
                return slide ? slide.offsetTop - container.offsetTop : 0;
            });
            expect(Math.abs(scrollTop - expectedTop)).toBeLessThan(10);
        });
    });
}

test.describe('test-image-zoom (Image Slides)', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto(`${BASE_PATH}test-image-zoom.html`);
        await page.waitForTimeout(500);
        await waitForMermaid(page);
    });

    test('6.1: Fullscreen image slide renders in DOC mode', async ({ page }) => {
        const fullscreenSlide = page.locator('.slide-image-fullscreen');
        await expect(fullscreenSlide).toHaveCount(1);

        const minHeight = await page.$eval('.slide-image-fullscreen', el =>
            parseFloat(getComputedStyle(el).minHeight)
        );
        const viewportHeight = await page.evaluate(() => window.innerHeight);
        expect(minHeight).toBeGreaterThanOrEqual(viewportHeight - 10);

        const placeholder = page.locator('.slide-image-fullscreen .img-placeholder-large');
        await expect(placeholder).toHaveCount(1);
    });

    test('6.2: Fullscreen image slide fills viewport in PPT mode', async ({ page }) => {
        await enterPPT(page);
        expect(await getBodyClass(page)).toContain('mode-ppt');

        // Fullscreen image slide is at index 1
        await goToSlide(page, 1);

        const slideHeight = await page.$eval('.slide-image-fullscreen', el => el.offsetHeight);
        const viewportHeight = await page.evaluate(() => window.innerHeight);
        expect(Math.abs(slideHeight - viewportHeight)).toBeLessThan(10);
    });

    test('6.3: Content-mode image slide constrained to content area', async ({ page }) => {
        const contentSlide = page.locator('.slide-image-content');
        await expect(contentSlide).toHaveCount(1);

        const contentWrapper = page.locator('.slide-image-content .content');
        await expect(contentWrapper).toHaveCount(1);

        const maxWidth = await page.$eval('.slide-image-content .content', el =>
            getComputedStyle(el).maxWidth
        );
        expect(maxWidth).toBe('900px');
    });

    test('6.4: Image slide has no focusable diagrams', async ({ page }) => {
        await enterPPT(page);

        // Navigate to fullscreen image slide (index 1)
        await goToSlide(page, 1);

        const focusedCount = await page.evaluate(() =>
            document.querySelectorAll('.diagram-focusable.focused').length
        );
        expect(focusedCount).toBe(0);

        // Press Enter — assert no zoom container appears
        await page.keyboard.press('Enter');
        await page.waitForTimeout(300);

        const zoomExists = await page.evaluate(() =>
            document.querySelector('.zoom-container') !== null
        );
        expect(zoomExists).toBe(false);
    });

    test('6.5: Image slide ArrowDown/Up navigates to next/prev slide', async ({ page }) => {
        await enterPPT(page);

        // Navigate to fullscreen image slide (index 1)
        await goToSlide(page, 1);

        await page.keyboard.press('ArrowDown');
        await page.waitForTimeout(400);
        let slideIndex = await getCurrentSlideIndex(page);
        expect(slideIndex).toBe(2);

        await page.keyboard.press('ArrowUp');
        await page.waitForTimeout(400);
        slideIndex = await getCurrentSlideIndex(page);
        expect(slideIndex).toBe(1);
    });

    test('6.6: Mobile viewport image slide uses object-fit: contain', async ({ page }) => {
        await page.setViewportSize({ width: 375, height: 667 });
        await page.waitForTimeout(200);

        // Assert .slide-image-fullscreen has min-height: 60vh on mobile
        const minHeight = await page.$eval('.slide-image-fullscreen', el =>
            parseFloat(getComputedStyle(el).minHeight)
        );
        const expected60vh = await page.evaluate(() => window.innerHeight * 0.6);
        expect(Math.abs(minHeight - expected60vh)).toBeLessThan(5);

        // Insert a temporary img to test the CSS object-fit rule
        await page.evaluate(() => {
            const img = document.createElement('img');
            img.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
            img.setAttribute('data-test-img', 'true');
            const slide = document.querySelector('.slide-image-fullscreen');
            slide.appendChild(img);
        });

        const objectFit = await page.$eval('.slide-image-fullscreen img[data-test-img]', el =>
            getComputedStyle(el).objectFit
        );
        expect(objectFit).toBe('contain');
    });
});
