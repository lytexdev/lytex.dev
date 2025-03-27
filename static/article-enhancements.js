document.addEventListener('DOMContentLoaded', function() {
    addLanguageTags();
    addCopyButtons();
    generateTableOfContents();
    processExternalLinks();
});

function addLanguageTags() {
    const codeBlocks = document.querySelectorAll('.codehilite');
    
    codeBlocks.forEach(function(block) {
        const classes = block.className.split(' ');
        let language = 'code';

        for (const cls of classes) {
            if (cls.startsWith('language-')) {
                language = cls.replace('language-', '');
                break;
            }
        }
        
        if (language === 'code') {
            const codeElement = block.querySelector('code');
            if (codeElement && codeElement.className) {
                const codeClasses = codeElement.className.split(' ');
                for (const cls of codeClasses) {
                    if (cls.startsWith('language-')) {
                        language = cls.replace('language-', '');
                        break;
                    }
                }
            }
        }
        
        block.setAttribute('data-language', language);
    });
}

function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('.codehilite');
    
    codeBlocks.forEach(function(block) {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-button';
        copyButton.textContent = 'Copy';
        copyButton.style.position = 'absolute';
        copyButton.style.top = '5px';
        copyButton.style.right = '60px';
        copyButton.style.background = '#333';
        copyButton.style.color = '#fff';
        copyButton.style.border = 'none';
        copyButton.style.borderRadius = '3px';
        copyButton.style.padding = '3px 8px';
        copyButton.style.fontSize = '12px';
        copyButton.style.cursor = 'pointer';
        copyButton.style.zIndex = '2';
        
        copyButton.addEventListener('click', function() {
            const code = block.querySelector('pre').textContent;
            navigator.clipboard.writeText(code).then(function() {
                copyButton.textContent = 'Kopiert!';
                copyButton.style.background = '#4CAF50';
                
                setTimeout(function() {
                    copyButton.textContent = 'Kopieren';
                    copyButton.style.background = '#333';
                }, 2000);
            }).catch(function() {
                copyButton.textContent = 'Fehlgeschlagen';
                copyButton.style.background = '#F44336';
                
                setTimeout(function() {
                    copyButton.textContent = 'Kopieren';
                    copyButton.style.background = '#333';
                }, 2000);
            });
        });

        block.style.position = 'relative';
        block.insertBefore(copyButton, block.firstChild);
    });
}

function generateTableOfContents() {
    const headings = document.querySelectorAll('.markdown-body h2, .markdown-body h3, .markdown-body h4');
    
    if (headings.length < 3) {
        return;
    }
    
    const toc = document.createElement('div');
    toc.className = 'toc';
    
    const tocTitle = document.createElement('div');
    tocTitle.className = 'toc-title';
    tocTitle.textContent = 'Inhaltsverzeichnis';
    toc.appendChild(tocTitle);
    
    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';
    toc.appendChild(tocList);
    
    headings.forEach(function(heading) {
        if (!heading.id) {
            heading.id = heading.textContent
                .toLowerCase()
                .replace(/[^\w\s-]/g, '')
                .replace(/\s+/g, '-');
        }
        
        const level = parseInt(heading.tagName.charAt(1)) - 2;
        
        const tocItem = document.createElement('li');
        tocItem.style.marginLeft = level * 15 + 'px';
        
        const tocLink = document.createElement('a');
        tocLink.href = '#' + heading.id;
        tocLink.textContent = heading.textContent.replace('#', '');
        
        tocItem.appendChild(tocLink);
        tocList.appendChild(tocItem);
    });
    
    const content = document.querySelector('.article-content');
    content.insertBefore(toc, content.firstChild);
}

function processExternalLinks() {
    const links = document.querySelectorAll('.markdown-body a');
    
    links.forEach(function(link) {
        if (link.hostname !== window.location.hostname && link.hostname !== '') {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
            
            if (!link.querySelector('.external-link-icon')) {
                const icon = document.createElement('span');
                icon.className = 'external-link-icon';
                icon.textContent = ' ↗';
                icon.style.fontSize = '0.8em';
                icon.style.verticalAlign = 'super';
                icon.style.color = '#ff6666';
                link.appendChild(icon);
            }
        }
    });
}