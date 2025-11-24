"""
Web Class Obfuscator Core Module
Professional CSS class name obfuscation for web projects
"""

import os
import shutil
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Any
from pathlib import Path
import logging

from bs4 import BeautifulSoup
import tinycss2
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class ClassMapping:
    """Mapping between original and obfuscated class names."""
    original: str
    obfuscated: str

def obfuscate_identifier(identifier: str, method: str = "shift") -> str:
    """
    Obfuscate an identifier using the specified method.
    
    Args:
        identifier: Original class name
        method: 'shift', 'hash', or 'hex'
    
    Returns:
        Obfuscated identifier
    """
    if not identifier:
        return identifier
    
    if method == "shift":
        # Caesar cipher based on string length
        shift = len(identifier)
        result = []
        for char in identifier:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr(base + (ord(char) - base + shift) % 26))
            else:
                result.append(char)
        return ''.join(result)
    
    elif method == "hash":
        # Generate short, unique hash
        hash_obj = hashlib.md5(identifier.encode('utf-8'))
        return "c" + hash_obj.hexdigest()[:8]
    
    elif method == "hex":
        # Hex encode the string
        return "c" + identifier.encode('utf-8').hex()
    
    else:
        raise ValueError(f"Unknown obfuscation method: '{method}'")

def scan_project_files(folder_path: str, extensions: List[str] = None) -> List[str]:
    """
    Recursively scan folder for files with specified extensions.
    
    Args:
        folder_path: Root directory to scan
        extensions: File extensions to include (default: .html, .css)
    
    Returns:
        List of absolute file paths
    """
    if extensions is None:
        extensions = ['.html', '.css']
    
    path = Path(folder_path)
    if not path.is_dir():
        raise ValueError(f"'{folder_path}' is not a valid directory")
    
    files = []
    for ext in extensions:
        files.extend(str(f) for f in path.rglob(f"*{ext}"))
    
    return sorted(files)

def extract_classes_from_css(css_content: str) -> Set[str]:
    """Extract all class names from CSS content."""
    rules = tinycss2.parse_stylesheet(css_content, skip_comments=True)
    class_names = set()
    
    for rule in rules:
        if rule.type != 'qualified-rule':
            continue
        
        prelude = rule.prelude
        for i, token in enumerate(prelude[1:], 1):
            if (token.type == 'ident' and 
                prelude[i-1] and 
                prelude[i-1].type == 'literal' and 
                prelude[i-1].value == '.'):
                class_names.add(token.value)
    
    return class_names

def extract_classes_from_html(html_content: str) -> Set[str]:
    """Extract all class names from HTML content."""
    soup = BeautifulSoup(html_content, 'lxml')
    class_names = set()
    
    # Extract from class attributes
    for tag in soup.find_all(class_=True):
        classes = tag.get('class', [])
        if isinstance(classes, str):
            classes = [classes]
        class_names.update(classes)
    
    # Extract from inline <style> tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            class_names.update(extract_classes_from_css(style_tag.string))
    
    return class_names

def build_class_mapping(
    all_classes: Set[str], 
    method: str = "shift",
    exclude: Set[str] = None
) -> List[ClassMapping]:
    """
    Build obfuscation mappings ensuring uniqueness.
    
    Args:
        all_classes: Set of class names to process
        method: Obfuscation method
        exclude: Set of classes to skip
    
    Returns:
        Sorted list of mappings
    """
    if exclude is None:
        exclude = set()
    
    mappings = []
    used_names = set()
    
    for class_name in sorted(all_classes):
        if not class_name or class_name in exclude:
            continue
        
        obfuscated = obfuscate_identifier(class_name, method)
        
        # Ensure uniqueness with collision handling
        original_obfuscated = obfuscated
        counter = 1
        while obfuscated in used_names:
            obfuscated = f"{original_obfuscated}_{counter}"
            counter += 1
        
        used_names.add(obfuscated)
        mappings.append(ClassMapping(class_name, obfuscated))
    
    # Sort by length (descending) for safe replacement
    return sorted(mappings, key=lambda x: len(x.original), reverse=True)

def process_css_content(content: str, mappings: List[ClassMapping]) -> str:
    """Replace class names in CSS content."""
    for mapping in mappings:
        # Use word boundaries to avoid partial replacements
        pattern = rf"\.{re.escape(mapping.original)}\b"
        replacement = f".{mapping.obfuscated}"
        content = re.sub(pattern, replacement, content)
    return content

def process_html_content(
    content: str, 
    mappings: List[ClassMapping], 
    css_files: List[str],
    output_suffix: str = "_obfuscated"
) -> str:
    """
    Replace class names in HTML and update CSS links.
    
    Args:
        content: HTML content
        mappings: List of class mappings
        css_files: Original CSS file paths for link updates
        output_suffix: Suffix for obfuscated CSS files
    """
    class_dict = {m.original: m.obfuscated for m in mappings}
    
    # Map original CSS filenames to obfuscated ones
    css_file_mapping = {}
    for css_file in css_files:
        base = Path(css_file).name
        css_file_mapping[base] = f"{Path(base).stem}{output_suffix}{Path(base).suffix}"
    
    soup = BeautifulSoup(content, 'lxml')
    
    # Update CSS file references
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if href:
            file_name = Path(href).name
            if file_name in css_file_mapping:
                new_href = href.replace(file_name, css_file_mapping[file_name])
                link['href'] = new_href
                logging.debug(f"Updated CSS link: {file_name} -> {css_file_mapping[file_name]}")
    
    # Process inline <style> tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            style_tag.string.replace_with(process_css_content(style_tag.string, mappings))
    
    # Update class attributes
    for tag in soup.find_all(class_=True):
        classes = tag.get('class', [])
        if isinstance(classes, str):
            classes = [classes]
        
        updated = [class_dict.get(cls, cls) for cls in classes]
        if updated:
            tag['class'] = updated
    
    return str(soup)

def create_backup(file_path: str) -> Optional[str]:
    """Create a .backup copy of the file."""
    backup_path = f"{file_path}.backup"
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        logging.warning(f"Failed to backup {file_path}: {e}")
        return None

def obfuscate_website(
    folder_path: str,
    output_suffix: str = "_obfuscated",
    extensions: List[str] = None,
    method: str = "shift",
    exclude_classes: List[str] = None,
    create_backup: bool = False
) -> Dict[str, Any]:
    """
    Main obfuscation orchestrator.
    
    Args:
        folder_path: Project root directory
        output_suffix: Output filename suffix
        extensions: File types to process
        method: Obfuscation method
        exclude_classes: Classes to exclude
        create_backup: Whether to backup originals
    
    Returns:
        Statistics dictionary
    """
    if extensions is None:
        extensions = ['.html', '.css']
    
    if exclude_classes is None:
        exclude_classes = []
    
    stats = {
        'processed_css_files': [],
        'processed_html_files': [],
        'total_classes': 0,
        'class_mappings': [],
        'errors': [],
        'backups_created': []
    }
    
    try:
        # Scan files
        logging.info(f"🔍 Scanning: {folder_path}")
        all_files = scan_project_files(folder_path, extensions)
        css_files = [f for f in all_files if f.endswith('.css')]
        html_files = [f for f in all_files if f.endswith('.html')]
        
        logging.info(f"📊 Found {len(css_files)} CSS and {len(html_files)} HTML files")
        
        # Extract classes
        all_classes = set()
        
        for css_file in tqdm(css_files, desc="Scanning CSS"):
            try:
                content = Path(css_file).read_text(encoding='utf-8')
                all_classes.update(extract_classes_from_css(content))
            except Exception as e:
                stats['errors'].append(f"CSS scan error: {css_file} - {e}")
        
        for html_file in tqdm(html_files, desc="Scanning HTML"):
            try:
                content = Path(html_file).read_text(encoding='utf-8')
                all_classes.update(extract_classes_from_html(content))
            except Exception as e:
                stats['errors'].append(f"HTML scan error: {html_file} - {e}")
        
        logging.info(f"🔢 Total unique classes: {len(all_classes)}")
        
        if not all_classes:
            logging.warning("⚠️  No classes found to obfuscate")
            return stats
        
        # Build mappings
        exclude_set = set(exclude_classes)
        mappings = build_class_mapping(all_classes, method, exclude_set)
        stats['total_classes'] = len(mappings)
        stats['class_mappings'] = mappings
        
        # Process CSS files
        logging.info("🎨 Processing CSS files...")
        for css_file in tqdm(css_files, desc="Obfuscating CSS"):
            try:
                if create_backup:
                    backup = create_backup(css_file)
                    if backup:
                        stats['backups_created'].append(backup)
                
                content = Path(css_file).read_text(encoding='utf-8')
                obfuscated = process_css_content(content, mappings)
                output = generate_obfuscated_filename(css_file, output_suffix)
                
                Path(output).write_text(obfuscated, encoding='utf-8')
                stats['processed_css_files'].append({'original': css_file, 'obfuscated': output})
            
            except Exception as e:
                stats['errors'].append(f"CSS process error: {css_file} - {e}")
        
        # Process HTML files
        logging.info("📝 Processing HTML files...")
        for html_file in tqdm(html_files, desc="Obfuscating HTML"):
            try:
                if create_backup:
                    backup = create_backup(html_file)
                    if backup:
                        stats['backups_created'].append(backup)
                
                content = Path(html_file).read_text(encoding='utf-8')
                obfuscated = process_html_content(content, mappings, css_files, output_suffix)
                output = generate_obfuscated_filename(html_file, output_suffix)
                
                Path(output).write_text(obfuscated, encoding='utf-8')
                stats['processed_html_files'].append({'original': html_file, 'obfuscated': output})
            
            except Exception as e:
                stats['errors'].append(f"HTML process error: {html_file} - {e}")
        
        # Final report
        logging.info("\n" + "="*60)
        logging.info("✅ Processing Complete!")
        logging.info("="*60)
        logging.info(f"📁 CSS files: {len(stats['processed_css_files'])}")
        logging.info(f"📄 HTML files: {len(stats['processed_html_files'])}")
        logging.info(f"🔐 Classes obfuscated: {stats['total_classes']}")
        
        if stats['backups_created']:
            logging.info(f"💾 Backups created: {len(stats['backups_created'])}")
        
        if stats['errors']:
            logging.error(f"⚠️  Errors encountered: {len(stats['errors'])}")
            for error in stats['errors']:
                logging.error(f"   - {error}")
        
        return stats
        
    except Exception as e:
        logging.exception(f"💥 Fatal error: {e}")
        stats['errors'].append(str(e))
        return stats

def generate_obfuscated_filename(file_path: str, suffix: str = "_obfuscated") -> str:
    """Generate output filename with suffix."""
    path = Path(file_path)
    return str(path.parent / f"{path.stem}{suffix}{path.suffix}")

# Import here to avoid circular reference
import re