#!/usr/bin/env python3
import os
import sys
import argparse
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional, List

from obfuscator import obfuscate_website

# Logo as ASCII art
LOGO_TEXT = """
       _____ _           _     _               _ _____           
      / ____| |         | |   | |             (_)  __ \          
     | (___ | |__   __ _| |__ | |__   __ _ _____| |__) |__ _ ____ 
      \___ \| '_ \ / _` | '_ \| '_ \ / _` |_  / |  _  // _` |_  / 
      ____) | | | | (_| | | | | |_) | (_| |/ /| | | \ \ (_| |/ /  
     |_____/|_| |_|\__,_|_| |_|_.__/ \__,_/___|_|_|  \_\__,_/___| 
                                                                 
   _____            ____  _      __                     _             
  / ____|          / __ \| |    / _|                   | |            
 | |     ___ ___  | |  | | |__ | |_ _   _ ___  ___ __ _| |_ ___  _ __ 
 | |    / __/ __| | |  | | '_ \|  _| | | / __|/ __/ _` | __/ _ \| '__|
 | |____\__ \__ \ | |__| | |_) | | | |_| \__ \ (_| (_| | || (_) | |   
  \_____|___/___/  \____/|_.__/|_|  \__,_|___/\___\__,_|\__\___/|_|                                                                                                                                                                                                   
"""

def clear_screen():
    """Clear console screen cross-platform."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu():
    """Display main menu and handle user input."""
    clear_screen()
    print(LOGO_TEXT)
    print("1) Obfuscator")
    print("2) DeObfuscator")
    print("3) Exit")
    
    choice = input("Choose an option: ").strip()
    
    if choice == "1":
        run_obfuscator()
    elif choice == "2":
        print("\n⚠️  DeObfuscator not implemented yet!")
        input("\nPress Enter to continue...")
    elif choice == "3":
        print("\nExiting...")
        sys.exit(0)
    else:
        print("\n❌ Invalid choice! Please try again.")
        input("\nPress Enter to continue...")

def select_folder() -> Optional[str]:
    """Open folder selection dialog."""
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes("-topmost", True)
    
    folder_path = filedialog.askdirectory(title="Select Project Folder")
    root.destroy()
    
    return folder_path

def run_obfuscator():
    """Run obfuscator with folder selection."""
    clear_screen()
    print(LOGO_TEXT)
    print("Web Class Obfuscator")
    print("\nPress Enter to select folder or type 'esc' to return...")
    
    while True:
        key = input("Your choice: ").strip()
        
        if key == '':
            folder_path = select_folder()
            if folder_path:
                run_obfuscation_process(folder_path)
            else:
                print("\n❌ No folder selected.")
                input("\nPress Enter to continue...")
            break
        elif key.lower() == 'esc':
            return
        else:
            print("❌ Invalid input. Press Enter to continue or type 'esc' to return.")

def run_obfuscation_process(folder_path: str):
    """Execute obfuscation on selected folder."""
    clear_screen()
    print(LOGO_TEXT)
    print(f"Selected folder: {folder_path}")
    print("\nSelect obfuscation method:")
    print("1) Character Shift (Default)")
    print("2) Short Hash")
    print("3) Hex Encoding")
    
    method_choice = input("Choose an option: ").strip()
    method_map = {"1": "shift", "2": "hash", "3": "hex"}
    
    if method_choice not in method_map:
        print("\n❌ Invalid method selection.")
        input("\nPress Enter to continue...")
        return
    
    try:
        print(f"\n🚀 Starting obfuscation...")
        result = obfuscate_website(
            folder_path=folder_path,
            output_suffix="_obfuscated",
            method=method_map[method_choice]
        )
        
        print("\n" + "="*60)
        print("✅ Processing complete!")
        print("="*60)
        print(f"📁 CSS files processed: {len(result['processed_css_files'])}")
        print(f"📄 HTML files processed: {len(result['processed_html_files'])}")
        print(f"🔐 Classes obfuscated: {result['total_classes']}")
        
        if result['errors']:
            print(f"\n⚠️  Errors: {len(result['errors'])}")
            for error in result['errors'][:3]:  # Show first 3 errors
                print(f"   - {error}")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    
    input("\nPress Enter to return to main menu...")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Web Class Obfuscator - Protect your frontend code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"{LOGO_TEXT}\nExamples:\n"
               "  python web_obfuscator.py                    # Interactive mode\n"
               "  python web_obfuscator.py -p ./project     # CLI mode\n"
               "  python web_obfuscator.py -p ./project --method hash --backup"
    )
    
    parser.add_argument("-p", "--path", help="Project folder path (skips menu)")
    parser.add_argument("-s", "--suffix", default="_obfuscated", help="Output file suffix")
    parser.add_argument("--method", choices=["shift", "hash", "hex"], default="shift", help="Obfuscation method")
    parser.add_argument("--exclude", nargs="+", default=[], help="Classes to exclude")
    parser.add_argument("--backup", action="store_true", help="Create backups")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging
    import logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=level)
    
    # CLI mode
    if args.path:
        if not Path(args.path).is_dir():
            print(f"❌ Error: '{args.path}' is not a valid directory")
            sys.exit(1)
        
        print(LOGO_TEXT)
        print(f"🚀 Running in CLI mode on: {args.path}")
        
        try:
            result = obfuscate_website(
                folder_path=args.path,
                output_suffix=args.suffix,
                method=args.method,
                exclude_classes=args.exclude,
                create_backup=args.backup
            )
            
            if result['errors']:
                print(f"\n⚠️  Completed with {len(result['errors'])} errors")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            sys.exit(1)
    else:
        # Interactive menu mode
        try:
            while True:
                display_main_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()