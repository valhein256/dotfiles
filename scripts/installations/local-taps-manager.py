#!/usr/bin/env python3
"""
Local Taps Manager
Manage and display information about local Homebrew taps and their formulas.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class LocalTapsManager:
    """Local Homebrew taps manager"""
    
    def __init__(self):
        self.homebrew_prefix = self.get_homebrew_prefix()
        self.taps_dir = Path(self.homebrew_prefix) / "Library" / "Taps"
        
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def error(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception as e:
            self.error(f"Command failed: {cmd} - {e}")
            return None
    
    def get_homebrew_prefix(self) -> str:
        """Get Homebrew installation prefix"""
        result = self.run_command("brew --prefix")
        if result and result.returncode == 0:
            return result.stdout.strip()
        return "/opt/homebrew"  # Default for Apple Silicon
    
    def get_all_taps(self) -> List[str]:
        """Get all installed taps"""
        result = self.run_command("brew tap")
        if result and result.returncode == 0:
            return [tap.strip() for tap in result.stdout.split('\n') if tap.strip()]
        return []
    
    def get_local_taps(self) -> List[str]:
        """Get only local taps"""
        all_taps = self.get_all_taps()
        return [tap for tap in all_taps if tap.startswith('local/')]
    
    def get_tap_path(self, tap_name: str) -> Path:
        """Get the filesystem path for a tap"""
        # Convert tap name to directory structure
        # e.g., "local/custom" -> "local/homebrew-custom"
        parts = tap_name.split('/')
        if len(parts) == 2:
            user, repo = parts
            tap_dir = f"{user}/homebrew-{repo}"
            return self.taps_dir / tap_dir
        return Path()
    
    def get_tap_formulas(self, tap_path: Path) -> List[Dict[str, str]]:
        """Get all formulas in a tap"""
        formulas = []
        formula_dir = tap_path / "Formula"
        
        if formula_dir.exists():
            for formula_file in formula_dir.glob("*.rb"):
                formula_info = {
                    'name': formula_file.stem,
                    'file': str(formula_file),
                    'size': self.get_file_size(formula_file)
                }
                
                # Try to extract basic info from formula
                try:
                    with open(formula_file, 'r') as f:
                        content = f.read()
                        formula_info['description'] = self.extract_description(content)
                        formula_info['version'] = self.extract_version(content)
                        formula_info['url'] = self.extract_url(content)
                except Exception:
                    pass
                
                formulas.append(formula_info)
        
        return formulas
    
    def get_file_size(self, file_path: Path) -> str:
        """Get human-readable file size"""
        try:
            size = file_path.stat().st_size
            if size < 1024:
                return f"{size}B"
            elif size < 1024 * 1024:
                return f"{size/1024:.1f}KB"
            else:
                return f"{size/(1024*1024):.1f}MB"
        except:
            return "Unknown"
    
    def extract_description(self, content: str) -> str:
        """Extract description from formula content"""
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('desc '):
                # Extract text between quotes
                start = line.find('"')
                end = line.rfind('"')
                if start != -1 and end != -1 and start != end:
                    return line[start+1:end]
        return "No description"
    
    def extract_version(self, content: str) -> str:
        """Extract version from formula content"""
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('version '):
                # Extract text between quotes
                start = line.find('"')
                end = line.rfind('"')
                if start != -1 and end != -1 and start != end:
                    return line[start+1:end]
        return "Unknown"
    
    def extract_url(self, content: str) -> str:
        """Extract URL from formula content"""
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('url '):
                # Extract text between quotes
                start = line.find('"')
                end = line.rfind('"')
                if start != -1 and end != -1 and start != end:
                    return line[start+1:end]
        return "No URL"
    
    def list_local_taps(self, detailed: bool = False) -> None:
        """List all local taps and their information"""
        print(f"{Colors.BOLD}🏠 LOCAL HOMEBREW TAPS{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        
        local_taps = self.get_local_taps()
        
        if not local_taps:
            self.info("No local taps found")
            return
        
        for tap_name in local_taps:
            tap_path = self.get_tap_path(tap_name)
            
            print(f"\n{Colors.CYAN}📦 {tap_name}{Colors.RESET}")
            print(f"   Path: {tap_path}")
            
            if tap_path.exists():
                self.success("Tap directory exists")
                
                # Check if it's a git repository
                if (tap_path / ".git").exists():
                    print(f"   Type: Git repository")
                    
                    # Get git info
                    git_info = self.get_git_info(tap_path)
                    if git_info:
                        print(f"   Remote: {git_info.get('remote', 'Unknown')}")
                        print(f"   Branch: {git_info.get('branch', 'Unknown')}")
                        print(f"   Last commit: {git_info.get('last_commit', 'Unknown')}")
                
                # List formulas
                formulas = self.get_tap_formulas(tap_path)
                if formulas:
                    print(f"   Formulas: {len(formulas)}")
                    for formula in formulas:
                        print(f"     • {formula['name']} ({formula['size']})")
                        if detailed:
                            print(f"       Description: {formula.get('description', 'N/A')}")
                            print(f"       Version: {formula.get('version', 'N/A')}")
                            print(f"       File: {formula['file']}")
                else:
                    self.warning("No formulas found in tap")
            else:
                self.error("Tap directory does not exist")
    
    def get_git_info(self, repo_path: Path) -> Dict[str, str]:
        """Get git repository information"""
        git_info = {}
        
        try:
            # Get remote URL
            result = self.run_command(f"cd '{repo_path}' && git remote get-url origin")
            if result and result.returncode == 0:
                git_info['remote'] = result.stdout.strip()
            
            # Get current branch
            result = self.run_command(f"cd '{repo_path}' && git branch --show-current")
            if result and result.returncode == 0:
                git_info['branch'] = result.stdout.strip()
            
            # Get last commit
            result = self.run_command(f"cd '{repo_path}' && git log -1 --format='%h - %s (%cr)'")
            if result and result.returncode == 0:
                git_info['last_commit'] = result.stdout.strip()
                
        except Exception:
            pass
        
        return git_info
    
    def show_tap_details(self, tap_name: str) -> None:
        """Show detailed information about a specific tap"""
        print(f"{Colors.BOLD}🔍 TAP DETAILS: {tap_name}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        
        tap_path = self.get_tap_path(tap_name)
        
        if not tap_path.exists():
            self.error(f"Tap directory does not exist: {tap_path}")
            return
        
        print(f"\n{Colors.CYAN}📍 Location{Colors.RESET}")
        print(f"   Path: {tap_path}")
        
        # Git information
        if (tap_path / ".git").exists():
            print(f"\n{Colors.CYAN}🔗 Git Repository{Colors.RESET}")
            git_info = self.get_git_info(tap_path)
            for key, value in git_info.items():
                print(f"   {key.title()}: {value}")
        
        # Formulas
        formulas = self.get_tap_formulas(tap_path)
        if formulas:
            print(f"\n{Colors.CYAN}📋 Formulas ({len(formulas)}){Colors.RESET}")
            for formula in formulas:
                print(f"\n   • {Colors.BOLD}{formula['name']}{Colors.RESET}")
                print(f"     Description: {formula.get('description', 'N/A')}")
                print(f"     Version: {formula.get('version', 'N/A')}")
                print(f"     File: {formula['file']}")
                print(f"     Size: {formula['size']}")
                
                if formula.get('url'):
                    print(f"     URL: {formula['url']}")
        else:
            print(f"\n{Colors.YELLOW}[ {Colors.YELLOW}WARN{Colors.RESET} ]No formulas found{Colors.RESET}")
    
    def export_tap_info(self, output_file: str) -> None:
        """Export tap information to JSON file"""
        local_taps = self.get_local_taps()
        tap_data = {}
        
        for tap_name in local_taps:
            tap_path = self.get_tap_path(tap_name)
            
            tap_info = {
                'name': tap_name,
                'path': str(tap_path),
                'exists': tap_path.exists(),
                'formulas': []
            }
            
            if tap_path.exists():
                tap_info['git_info'] = self.get_git_info(tap_path)
                tap_info['formulas'] = self.get_tap_formulas(tap_path)
            
            tap_data[tap_name] = tap_info
        
        try:
            with open(output_file, 'w') as f:
                json.dump(tap_data, f, indent=2, default=str)
            self.success(f"Tap information exported to: {output_file}")
        except Exception as e:
            self.error(f"Failed to export tap information: {e}")
    
    def validate_taps(self) -> bool:
        """Validate all local taps"""
        print(f"{Colors.BOLD}[ {Colors.GREEN}OK{Colors.RESET} ] VALIDATING LOCAL TAPS{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        
        local_taps = self.get_local_taps()
        all_valid = True
        
        if not local_taps:
            self.info("No local taps to validate")
            return True
        
        for tap_name in local_taps:
            print(f"\n{Colors.CYAN}Validating {tap_name}:{Colors.RESET}")
            tap_path = self.get_tap_path(tap_name)
            
            # Check if directory exists
            if not tap_path.exists():
                self.error(f"Directory does not exist: {tap_path}")
                all_valid = False
                continue
            
            # Check formulas
            formulas = self.get_tap_formulas(tap_path)
            if not formulas:
                self.warning("No formulas found")
                continue
            
            # Validate each formula
            for formula in formulas:
                formula_name = formula['name']
                result = self.run_command(f"brew audit --formula {tap_name}/{formula_name}")
                
                if result and result.returncode == 0:
                    self.success(f"Formula {formula_name} is valid")
                else:
                    self.error(f"Formula {formula_name} has issues")
                    if result and result.stderr:
                        print(f"       Error: {result.stderr.strip()}")
                    all_valid = False
        
        return all_valid
    
    def backup_local_taps(self, backup_dir: Path) -> bool:
        """Backup all local taps to specified directory"""
        print(f"{Colors.BOLD}💾 BACKING UP LOCAL TAPS{Colors.RESET}")
        
        local_taps = self.get_local_taps()
        if not local_taps:
            self.info("No local taps to backup")
            return True
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        success = True
        
        for tap_name in local_taps:
            tap_path = self.get_tap_path(tap_name)
            if not tap_path.exists():
                self.warning(f"Tap directory does not exist: {tap_path}")
                continue
            
            # Create backup directory for this tap
            tap_backup_name = tap_name.replace('/', '-')
            tap_backup_dir = backup_dir / f"local-tap-{tap_backup_name}"
            
            try:
                # Copy entire tap directory
                import shutil
                if tap_backup_dir.exists():
                    shutil.rmtree(tap_backup_dir)
                shutil.copytree(tap_path, tap_backup_dir)
                self.success(f"Backed up {tap_name} to {tap_backup_dir}")
            except Exception as e:
                self.error(f"Failed to backup {tap_name}: {e}")
                success = False
        
        return success
    
    def remove_local_taps(self) -> bool:
        """Remove all local taps"""
        print(f"{Colors.BOLD}🗑️  REMOVING LOCAL TAPS{Colors.RESET}")
        
        local_taps = self.get_local_taps()
        if not local_taps:
            self.info("No local taps to remove")
            return True
        
        success = True
        for tap_name in local_taps:
            try:
                # Untap the tap
                result = self.run_command(f"brew untap {tap_name}")
                if result and result.returncode == 0:
                    self.success(f"Removed tap: {tap_name}")
                else:
                    self.warning(f"Failed to untap {tap_name}, but continuing...")
                    
                # Also remove the directory if it still exists
                tap_path = self.get_tap_path(tap_name)
                if tap_path.exists():
                    import shutil
                    shutil.rmtree(tap_path)
                    self.success(f"Removed tap directory: {tap_path}")
                    
            except Exception as e:
                self.error(f"Failed to remove {tap_name}: {e}")
                success = False
        
        return success
    
    def restore_local_taps(self, backup_dir: Path) -> bool:
        """Restore local taps from backup directory"""
        print(f"{Colors.BOLD}🔄 RESTORING LOCAL TAPS{Colors.RESET}")
        
        if not backup_dir.exists():
            self.warning(f"Backup directory does not exist: {backup_dir}")
            return True
        
        # Find all tap backups
        tap_backups = list(backup_dir.glob("local-tap-*"))
        if not tap_backups:
            self.info("No local tap backups found")
            return True
        
        success = True
        for tap_backup_dir in tap_backups:
            try:
                # Extract tap name from backup directory name
                # e.g., "local-tap-local-custom" -> "local/custom"
                backup_name = tap_backup_dir.name
                if backup_name.startswith("local-tap-"):
                    tap_name_parts = backup_name[10:].split('-', 1)  # Remove "local-tap-" prefix
                    if len(tap_name_parts) == 2:
                        tap_name = f"{tap_name_parts[0]}/{tap_name_parts[1]}"
                        
                        # Get target path
                        tap_path = self.get_tap_path(tap_name)
                        
                        # Remove existing tap directory if it exists
                        if tap_path.exists():
                            import shutil
                            shutil.rmtree(tap_path)
                        
                        # Create parent directory
                        tap_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Copy backup to target location
                        import shutil
                        shutil.copytree(tap_backup_dir, tap_path)
                        
                        # Add the tap back to brew
                        result = self.run_command(f"brew tap {tap_name}")
                        if result and result.returncode == 0:
                            self.success(f"Restored tap: {tap_name}")
                        else:
                            self.warning(f"Restored files but failed to register tap: {tap_name}")
                            
            except Exception as e:
                self.error(f"Failed to restore {tap_backup_dir.name}: {e}")
                success = False
        
        return success


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Local Homebrew Taps Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                    # List all local taps
  %(prog)s list --detailed         # List with detailed information
  %(prog)s show local/custom       # Show details for specific tap
  %(prog)s export taps.json        # Export tap info to JSON
  %(prog)s validate                # Validate all local taps
  %(prog)s backup backups/         # Backup all local taps
  %(prog)s remove                  # Remove all local taps
  %(prog)s restore backups/        # Restore local taps from backup
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all local taps')
    list_parser.add_argument('--detailed', action='store_true',
                           help='Show detailed information')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show details for specific tap')
    show_parser.add_argument('tap_name', help='Name of the tap (e.g., local/custom)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export tap information to JSON')
    export_parser.add_argument('output_file', help='Output JSON file path')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate all local taps')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup all local taps')
    backup_parser.add_argument('backup_dir', help='Backup directory path')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove all local taps')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore local taps from backup')
    restore_parser.add_argument('backup_dir', help='Backup directory path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = LocalTapsManager()
    
    try:
        if args.command == 'list':
            manager.list_local_taps(detailed=args.detailed)
        elif args.command == 'show':
            manager.show_tap_details(args.tap_name)
        elif args.command == 'export':
            manager.export_tap_info(args.output_file)
        elif args.command == 'validate':
            success = manager.validate_taps()
            sys.exit(0 if success else 1)
        elif args.command == 'backup':
            success = manager.backup_local_taps(Path(args.backup_dir))
            sys.exit(0 if success else 1)
        elif args.command == 'remove':
            success = manager.remove_local_taps()
            sys.exit(0 if success else 1)
        elif args.command == 'restore':
            success = manager.restore_local_taps(Path(args.backup_dir))
            sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()