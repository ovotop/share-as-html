## MODIFIED Requirements

### Requirement: PPT mode wider content in generated HTML

#### Scenario: PPT mode wider content in generated HTML (modified)

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .slide .content { width: 1680px; aspect-ratio: 16 / 9; max-width: none; transform-origin: center center; }`
- **AND** the CSS SHALL contain `body.mode-ppt .slide { padding: 60px 120px; overflow: hidden; }`
- **AND** the CSS SHALL contain a responsive override: `@media (max-width: 768px) { body.mode-ppt .slide .content { width: 100%; aspect-ratio: auto; transform: none; } }`
- **AND** the JavaScript SHALL contain an `updateContentScale()` function that applies `transform: scale()` to `.slide .content` elements
- **AND** the JavaScript SHALL call `updateContentScale()` on entering PPT mode, navigating slides, and window resize
- **AND** the CSS SHALL NOT contain `body.mode-ppt .slide .content { max-width: 1100px; }`
