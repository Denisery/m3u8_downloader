// Documentation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Generate table of contents
    generateTableOfContents();
    
    // Add copy functionality to code blocks
    setupCodeCopy();
    
    // Add smooth scrolling for anchor links
    setupSmoothScrolling();
    
    // Add active class to current section in TOC
    highlightCurrentSection();
});

/**
 * Generate a table of contents from headings
 */
function generateTableOfContents() {
    const tocContainer = document.getElementById('toc-container');
    if (!tocContainer) return;
    
    const headings = document.querySelectorAll('.docs-content h2, .docs-content h3');
    if (headings.length === 0) return;
    
    const toc = document.createElement('ul');
    toc.className = 'toc-list';
    
    let currentLevel2Item = null;
    let currentLevel2List = null;
    
    headings.forEach(heading => {
        // Add id to the heading if it doesn't have one
        if (!heading.id) {
            heading.id = heading.textContent.toLowerCase().replace(/[^\w]+/g, '-');
        }
        
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${heading.id}`;
        link.textContent = heading.textContent;
        listItem.appendChild(link);
        
        if (heading.tagName === 'H2') {
            toc.appendChild(listItem);
            currentLevel2Item = listItem;
            
            // Create a new list for potential H3s
            currentLevel2List = document.createElement('ul');
            currentLevel2Item.appendChild(currentLevel2List);
        } else if (heading.tagName === 'H3' && currentLevel2List) {
            currentLevel2List.appendChild(listItem);
        }
    });
    
    tocContainer.appendChild(toc);
}

/**
 * Add copy button to code blocks
 */
function setupCodeCopy() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(codeBlock => {
        const container = codeBlock.parentNode;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        
        copyButton.addEventListener('click', () => {
            const code = codeBlock.textContent;
            navigator.clipboard.writeText(code).then(() => {
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                copyButton.textContent = 'Failed';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });
        
        // Add position relative to container for absolute positioning of button
        container.style.position = 'relative';
        copyButton.style.position = 'absolute';
        copyButton.style.top = '5px';
        copyButton.style.right = '5px';
        copyButton.style.padding = '3px 8px';
        copyButton.style.backgroundColor = 'var(--primary-color)';
        copyButton.style.color = 'white';
        copyButton.style.border = 'none';
        copyButton.style.borderRadius = '3px';
        copyButton.style.cursor = 'pointer';
        copyButton.style.fontSize = '12px';
        
        container.appendChild(copyButton);
    });
}

/**
 * Setup smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
                
                // Update URL without scrolling
                history.pushState(null, null, `#${targetId}`);
            }
        });
    });
}

/**
 * Highlight the current section in the table of contents
 */
function highlightCurrentSection() {
    const headings = Array.from(document.querySelectorAll('.docs-content h2, .docs-content h3'));
    if (headings.length === 0) return;
    
    const tocLinks = document.querySelectorAll('.toc-list a');
    if (tocLinks.length === 0) return;
    
    // Add scroll event listener
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY + 100; // Offset for better UX
        
        // Find the current heading
        let currentHeadingIndex = -1;
        
        for (let i = 0; i < headings.length; i++) {
            if (headings[i].offsetTop <= scrollPosition) {
                currentHeadingIndex = i;
            } else {
                break;
            }
        }
        
        // Remove active class from all links
        tocLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Add active class to current link
        if (currentHeadingIndex >= 0) {
            const currentHeadingId = headings[currentHeadingIndex].id;
            const currentLink = document.querySelector(`.toc-list a[href="#${currentHeadingId}"]`);
            if (currentLink) {
                currentLink.classList.add('active');
            }
        }
    });
}

// Add active class style
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .toc-list a.active {
            color: var(--accent-color);
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);
});
