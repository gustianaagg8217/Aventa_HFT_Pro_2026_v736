"""
License activation handler for Aventa HFT Pro
This module integrates license check at program startup
"""

import tkinter as tk
from tkinter import messagebox
import sys
from license_manager import LicenseManager, LicenseDialog


class LicenseCheckWindow:
    """Splash screen for license verification"""
    
    def __init__(self, root=None):
        """Initialize license check window"""
        self.license_manager = LicenseManager()
        self.root = root
        self.window = None
        self.is_licensed = False
    
    def check_license(self) -> bool:
        """
        Check if software is licensed
        If not, show activation dialog
        Returns True if licensed, False otherwise
        """
        # Try to verify existing license
        is_valid, message = self.license_manager.verify_license()
        
        if is_valid:
            print(f"✅ License verified: {message}")
            self.is_licensed = True
            return True
        
        # No valid license - show activation dialog
        print(f"❌ License check failed: {message}")
        
        if not self.root:
            # Create minimal root for dialog
            self.root = tk.Tk()
            self.root.withdraw()
        
        # Show activation dialog
        dialog = LicenseDialog(self.root, self.license_manager)
        result = dialog.show_activation_dialog()
        
        if result:
            self.is_licensed = True
            return True
        else:
            # User canceled activation
            messagebox.showerror(
                "License Required",
                "This software requires activation to run.\n\n"
                "The application will now close."
            )
            return False
    
    def show_splash_screen(self):
        """Show splash screen during license check"""
        self.window = tk.Tk()
        self.window.title("Aventa HFT Pro 2026")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        
        # Center window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content
        frame = tk.Frame(self.window, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            frame,
            text="🚀 AVENTA HFT PRO 2026",
            font=("Arial", 18, "bold"),
            bg="#1a1a1a",
            fg="#4CAF50"
        )
        title.pack(pady=(0, 20))
        
        status = tk.Label(
            frame,
            text="Verifying License...",
            font=("Arial", 12),
            bg="#1a1a1a",
            fg="#FFF"
        )
        status.pack()
        
        self.window.update()
        
        return self.window
    
    def close_splash(self):
        """Close splash screen"""
        if self.window:
            self.window.destroy()
            self.window = None


def enforce_license_on_startup(root=None) -> bool:
    """
    Call this at program startup to enforce license check
    
    Args:
        root: Optional Tkinter root window
    
    Returns:
        True if licensed and program should continue, False otherwise
    """
    license_check = LicenseCheckWindow(root)
    
    # Show splash during check
    splash = license_check.show_splash_screen()
    
    try:
        # Check license
        is_licensed = license_check.check_license()
        return is_licensed
    finally:
        # Close splash
        license_check.close_splash()


if __name__ == "__main__":
    # Test license check
    result = enforce_license_on_startup()
    print(f"License check result: {result}")
    
    if result:
        print("✅ Program can now run")
    else:
        print("❌ Program will exit")
        sys.exit(1)
