"""
Content validation utilities for blog posts
"""
import re
from typing import List, Tuple, Optional


class ContentValidator:
    """Validates blog post content for quality and completeness."""
    
    MIN_WORD_COUNT = 200
    MAX_WORD_COUNT = 5000
    MIN_HEADING_COUNT = 2
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text, excluding YAML frontmatter."""
        # Remove YAML frontmatter
        content = ContentValidator._remove_frontmatter(text)
        # Count words (simple split-based approach)
        return len(content.split())
    
    @staticmethod
    def count_headings(text: str) -> int:
        """Count markdown headings in text."""
        content = ContentValidator._remove_frontmatter(text)
        # Count # symbols at the beginning of lines
        heading_pattern = r'^#{1,6}\s+.+$'
        return len(re.findall(heading_pattern, content, re.MULTILINE))
    
    @staticmethod
    def _remove_frontmatter(text: str) -> str:
        """Remove YAML frontmatter from text."""
        lines = text.split('\n')
        if lines[0].strip() == "---":
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    return '\n'.join(lines[i+1:])
        return text
    
    @staticmethod
    def validate_content(text: str) -> Tuple[bool, List[str]]:
        """
        Validate blog post content.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check word count
        word_count = ContentValidator.count_words(text)
        if word_count < ContentValidator.MIN_WORD_COUNT:
            issues.append(f"Content too short: {word_count} words (minimum: {ContentValidator.MIN_WORD_COUNT})")
        elif word_count > ContentValidator.MAX_WORD_COUNT:
            issues.append(f"Content too long: {word_count} words (maximum: {ContentValidator.MAX_WORD_COUNT})")
        
        # Check heading count
        heading_count = ContentValidator.count_headings(text)
        if heading_count < ContentValidator.MIN_HEADING_COUNT:
            issues.append(f"Not enough headings: {heading_count} (minimum: {ContentValidator.MIN_HEADING_COUNT})")
        
        # Check for basic structure elements
        content = ContentValidator._remove_frontmatter(text)
        if not content.strip():
            issues.append("No content found after frontmatter")
        
        # Check for code blocks (good practice for technical blogs)
        if '```' not in content:
            issues.append("Consider adding code examples for better technical content")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def get_content_stats(text: str) -> dict:
        """Get statistics about the content."""
        content = ContentValidator._remove_frontmatter(text)
        
        return {
            'word_count': ContentValidator.count_words(text),
            'heading_count': ContentValidator.count_headings(text),
            'paragraph_count': len([p for p in content.split('\n\n') if p.strip()]),
            'code_blocks': content.count('```') // 2,
            'links': len(re.findall(r'\[.*?\]\(.*?\)', content)),
            'images': len(re.findall(r'!\[.*?\]\(.*?\)', content)),
            'character_count': len(content),
            'estimated_reading_time': ContentValidator.count_words(text) // 200  # ~200 words per minute
        }
