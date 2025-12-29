#!/usr/bin/env python3
"""
Local Homebrew Taps Cleanup Script
Removes local Homebrew taps with backup functionality.
"""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


class LocalTapsCleanup:
    """Local Homebrew taps cleanup manager"""
    
    def __init__(self, auto_confirm: bool = False, backup: bool = True):
        self.auto_confirm = auto_confirm
        self.backup = backup
        self.backup_dir = Path.cwd() / "backups" / "local-taps"
        self.homebrew_prefix = self.get_homebrew_prefix()
        self.taps_dir = Path(self.homebrew_prefix) / "Library" / "Taps"
        
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def fail(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception:
            return None
    
    def get_homebrew_prefix(self) -> str:
        """Get Homebrew installation prefix"""
        try:
            result = self.run_command("brew --prefix")
            if result and result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "/opt/homebrew"  # Default for Apple Silicon
    
    def get_local_taps(self) -> List[str]:
        """Get list of local Homebrew taps"""
        try:
            result = self.run_command("brew tap")
            if result and result.returncode == 0:
                all_taps = [tap.strip() for tap in result.stdout.split('\n') if tap.strip()]
                return [tap for tap in all_taps if tap.startswith('local/')]
        except:
            pass
        return []
    
    def backup_tap(self, tap_name: str) -> bool:
        """Backup a single tap"""
        try:
            # Get tap directory path
            parts = tap_name.split('/')
            if len(parts) != 2:
                return False
            
            user, repo = parts
            tap_dir = f"{user}/homebrew-{repo}"
            tap_path = self.taps_dir / tap_dir
            
            if not tap_path.exists():
                self.warning(f"Tap directory not found: {tap_path}")
                return False
            
            # Create backup directory
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create timestamped backup
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            tap_backup_name = tap_name.replace('/', '-')
            tap_backup_dir = self.backup_dir / f"{tap_backup_name}-{timestamp}"
            
            # Copy tap directory
            shutil.copytree(tap_path, tap_backup_dir)
            self.success(f"Backed up {tap_name} to {tap_backup_dir}")
            return True
            
        except Exception as e:
            self.warning(f"Failed to backup {tap_name}: {e}")
            return False
    
    def remove_tap(self, tap_name: str) -> bool:
        """Remove a single tap"""
        try:
            # Untap using brew command
            result = self.run_command(f"brew untap {tap_name}")
            if result and result.returncode == 0:
                self.success(f"Untapped {tap_name}")
            else:
                self.warning(f"Failed to untap {tap_name}")
            
            # Also remove directory if it still exists
            parts = tap_name.split('/')
            if len(parts) == 2:
                user, repo = parts
                tap_dir = f"{user}/homebrew-{repo}"
                tap_path = self.taps_dir / tap_dir
                
                if tap_path.exists():
                    shutil.rmtree(tap_path)
                    self.success(f"Removed directory {tap_path}")
            
            return True
            
        except Exception as e:
            self.warning(f"Failed to remove {tap_name}: {e}")
            return False
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        local_taps = self.get_local_taps()
        
        print(f"\n{Colors.CYAN}🏠 LOCAL HOMEBREW TAPS CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        
        if not local_taps:
            print("No local taps found to remove.")
            return
        
        print(f"Found {len(local_taps)} local taps to remove:")
        print()
        
        for tap in local_taps:
            print(f"  • {tap}")
        
        print()
        if self.backup:
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Taps will be backed up before removal")
        else:
            print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ]No backup will be created")
        print()
    
    def run_cleanup(self) -> None:
        """Execute local taps cleanup"""
        local_taps = self.get_local_taps()
        
        self.show_summary()
        
        if not local_taps:
            print("No local taps to remove.")
            return
        
        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Remove all local taps? Type 'YES' to confirm: ")
            if confirmation != "YES":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return
        
        print()
        self.info("Starting local taps cleanup...")
        
        success_count = 0
        
        for tap_name in local_taps:
            print(f"\n🏠 Processing {tap_name}")
            
            # Backup if requested
            if self.backup:
                if self.backup_tap(tap_name):
                    self.info(f"Backup completed for {tap_name}")
                else:
                    self.warning(f"Backup failed for {tap_name}, continuing with removal...")
            
            # Remove tap
            if self.remove_tap(tap_name):
                success_count += 1
        
        print()
        if success_count == len(local_taps):
            print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Local taps cleanup complete!{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[ {Colors.YELLOW}WARN{Colors.RESET} ]Local taps cleanup completed with some issues{Colors.RESET}")
        
        print()
        print(f"Processed {len(local_taps)} taps, {success_count} successful")
        
        if self.backup and success_count > 0:
            print(f"Backups saved to: {self.backup_dir}")
            print("You can restore taps with: make local-taps-restore DIR=backups/local-taps")
        
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Local Homebrew Taps Cleanup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Interactive mode with backup
  %(prog)s -y                 # Auto-confirm cleanup
  %(prog)s --no-backup        # Skip backup creation
        """
    )
    
    parser.add_argument('-y', '--yes', action='store_true',
                       help='Auto-confirm cleanup without asking')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup of taps')
    
    args = parser.parse_args()
    
    cleanup = LocalTapsCleanup(
        auto_confirm=args.yes,
        backup=not args.no_backup
    )
    
    try:
        cleanup.run_cleanup()
    except KeyboardInterrupt:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Cleanup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Cleanup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()