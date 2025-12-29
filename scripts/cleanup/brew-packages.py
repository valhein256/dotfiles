#!/usr/bin/env python3
"""
Homebrew Packages Cleanup Script
Removes all Homebrew formulae and casks.
"""

import argparse
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


class BrewPackagesCleanup:
    """Homebrew packages cleanup manager"""
    
    def __init__(self, auto_confirm: bool = False, backup: bool = True):
        self.auto_confirm = auto_confirm
        self.backup = backup
        self.backup_dir = Path.cwd() / "backups"
        
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def fail(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
    
    def run_command(self, cmd: str, capture_output: bool = True, ignore_errors: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            if not ignore_errors and result.returncode != 0:
                return None
            return result
        except Exception:
            return None
    
    def get_custom_taps(self) -> List[str]:
        """Get list of custom (non-homebrew) taps"""
        try:
            result = self.run_command("brew tap")
            if result and result.returncode == 0:
                all_taps = [tap.strip() for tap in result.stdout.split('\n') if tap.strip()]
                # Return taps that don't start with 'homebrew/'
                return [tap for tap in all_taps if not tap.startswith('homebrew/')]
        except:
            pass
        return []
    
    def backup_taps(self) -> None:
        """Backup current tap list"""
        if not self.backup:
            return
            
        self.info("Creating backup of current taps...")
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        
        # Backup taps
        result = self.run_command("brew tap")
        if result and result.returncode == 0:
            taps_backup = self.backup_dir / f"brew-taps-backup-{timestamp}.txt"
            taps_backup.write_text(result.stdout)
        
        self.success("Tap list backed up to backups/")
    
    def remove_custom_taps(self) -> None:
        """Remove all custom (non-homebrew) taps"""
        self.info("Checking custom taps...")
        
        custom_taps = self.get_custom_taps()
        
        if not custom_taps:
            self.success("No custom taps to remove")
            return
        
        print(f"  Found {len(custom_taps)} custom taps to remove:")
        for tap in custom_taps:
            print(f"    • {tap}")
        
        print()
        self.info("Removing custom taps...")
        
        for tap in custom_taps:
            try:
                result = self.run_command(f"brew untap {tap}")
                if result and result.returncode == 0:
                    self.success(f"Removed tap: {tap}")
                else:
                    self.warning(f"Failed to remove tap: {tap}")
            except Exception as e:
                self.warning(f"Error removing tap {tap}: {e}")
        
        remaining_custom_taps = self.get_custom_taps()
        if not remaining_custom_taps:
            self.success("All custom taps removed")
        else:
            self.warning(f"{len(remaining_custom_taps)} custom taps still remain")

    def get_installed_packages(self) -> tuple[List[str], List[str]]:
        """Get lists of installed formulae and casks"""
        formulae = []
        casks = []
        
        # Get formulae
        result = self.run_command("brew list --formula")
        if result and result.returncode == 0:
            formulae = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        
        # Get casks
        result = self.run_command("brew list --cask")
        if result and result.returncode == 0:
            casks = [c.strip() for c in result.stdout.split('\n') if c.strip()]
        
        return formulae, casks
    
    def backup_packages(self) -> None:
        """Backup current package lists"""
        if not self.backup:
            return
            
        self.info("Creating backup of current packages...")
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        
        # Backup formulae
        result = self.run_command("brew list --formula")
        if result and result.returncode == 0:
            formulae_backup = self.backup_dir / f"brew-formulae-backup-{timestamp}.txt"
            formulae_backup.write_text(result.stdout)
        
        # Backup casks
        result = self.run_command("brew list --cask")
        if result and result.returncode == 0:
            casks_backup = self.backup_dir / f"brew-casks-backup-{timestamp}.txt"
            casks_backup.write_text(result.stdout)
        
        self.success("Package list backed up to backups/")
    
    def remove_casks(self) -> None:
        """Remove all installed casks"""
        self.info("Checking installed casks...")
        
        result = self.run_command("brew list --cask")
        if result and result.returncode == 0:
            casks = [c.strip() for c in result.stdout.split('\n') if c.strip()]
            
            if not casks:
                self.success("No casks to remove")
                return
            
            self.info(f"Found {len(casks)} casks to remove:")
            for cask in casks:
                self.info(f"  • {cask}")
            
            # Remove all casks
            self.info(f"Removing {len(casks)} casks...")
            casks_str = ' '.join(f'"{cask}"' for cask in casks)
            result = self.run_command(f"brew uninstall --cask --force {casks_str}", capture_output=False)
            
            if result and result.returncode == 0:
                self.success(f"All {len(casks)} casks removed successfully")
            else:
                self.warning("Some casks may not have been removed")
        else:
            self.success("No casks to remove")
    
    def remove_formulae(self) -> None:
        """Remove all installed formulae"""
        self.info("Checking installed formulae...")
        
        result = self.run_command("brew list --formula")
        if result and result.returncode == 0:
            formulae = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            
            if not formulae:
                self.success("No formulae to remove")
                return
            
            self.info(f"Found {len(formulae)} formulae to remove:")
            for formula in formulae:
                self.info(f"  • {formula}")
            
            # Remove all formulae
            self.info(f"Removing {len(formulae)} formulae...")
            formulae_str = ' '.join(f'"{formula}"' for formula in formulae)
            result = self.run_command(f"brew uninstall --ignore-dependencies --force {formulae_str}", capture_output=False)
            
            if result and result.returncode == 0:
                self.success(f"All {len(formulae)} formulae removed successfully")
            else:
                self.warning("Some formulae may not have been removed")
        else:
            self.success("No formulae to remove")
    
    def cleanup_homebrew(self) -> None:
        """Clean up Homebrew"""
        self.info("Cleaning up Homebrew...")
        self.run_command("brew cleanup --prune=all", capture_output=False)
        self.run_command("brew autoremove", capture_output=False)
        self.success("Homebrew cleaned up")
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        formulae, casks = self.get_installed_packages()
        custom_taps = self.get_custom_taps()
        
        print(f"\n{Colors.CYAN}🍺 HOMEBREW PACKAGES CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will remove:")
        print(f"  📦 {len(formulae)} formulae")
        print(f"  🍱 {len(casks)} casks")
        print(f"  🚰 {len(custom_taps)} custom taps")
        print()
        
        if formulae:
            print("Formulae to remove:")
            for formula in sorted(formulae):
                print(f"  • {formula}")
            print()
        
        if casks:
            print("Casks to remove:")
            for cask in sorted(casks):
                print(f"  • {cask}")
            print()
        
        if custom_taps:
            print("Custom taps to remove:")
            for tap in sorted(custom_taps):
                print(f"  • {tap}")
            print()
        
        if self.backup:
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Package lists will be backed up before removal")
        print()
    
    def run_cleanup(self) -> None:
        """Execute Homebrew packages cleanup"""
        self.show_summary()
        
        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Remove all Homebrew packages and custom taps? Type 'YES' to confirm: ")
            if confirmation != "YES":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return
        
        print()
        self.info("Starting Homebrew packages cleanup...")
        
        # Step 1: Backup
        self.backup_packages()
        self.backup_taps()
        
        # Step 2: Remove custom taps first (before removing packages that might depend on them)
        self.remove_custom_taps()
        
        # Step 3: Remove casks
        self.remove_casks()
        
        # Step 4: Remove formulae
        self.remove_formulae()
        
        # Step 5: Clean up
        self.cleanup_homebrew()
        
        print()
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Homebrew packages cleanup complete!{Colors.RESET}")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Homebrew Packages Cleanup Script",
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
                       help='Skip creating backup of package lists')
    
    args = parser.parse_args()
    
    cleanup = BrewPackagesCleanup(
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