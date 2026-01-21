"""
INTEGRATION GUIDE - How to modify Aventa_HFT_Pro_2026_v7_3_6.py

Follow these exact steps to integrate the License System.
"""

# ============================================================================
# STEP 1: Add these 2 lines after existing imports (around line 40)
# ============================================================================

# Add after line: "from gui_telegram_integration import get_gui_telegram_integration"
# Add these lines:

"""
# License System
from license_check import enforce_license_on_startup
from license_manager import LicenseManager
"""

# ============================================================================
# STEP 2: Modify the main execution block (lines 5582-5585)
# ============================================================================

# ORIGINAL CODE (lines 5582-5585):
"""
if __name__ == "__main__": 
    root = tk.Tk()
    app = HFTProGUI(root)
    root.mainloop()
"""

# MODIFY TO THIS:
"""
if __name__ == "__main__":
    # ENFORCE LICENSE CHECK BEFORE STARTING GUI
    try:
        if not enforce_license_on_startup():
            print("❌ License verification failed. Exiting application.")
            sys.exit(1)
    except ImportError:
        print("⚠️ License system not found. Running without license protection.")
        print("Make sure license_manager.py and license_check.py are in the same folder.")
    
    # License is valid, start the main application
    root = tk.Tk()
    app = HFTProGUI(root)
    root.mainloop()
"""

# ============================================================================
# STEP 3: OPTIONAL - Add License Menu to GUI (recommended)
# ============================================================================

# Find the HFTProGUI class __init__ method
# Add this line after menubar creation (usually around line 650-700):

"""
# In __init__ of HFTProGUI class:
self.menubar = tk.Menu(root)
root.config(menu=self.menubar)

# ... existing menus ...

# ADD THIS:
# Create Help menu with License options
help_menu = tk.Menu(self.menubar, tearoff=0)
self.menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="License Information", command=self.show_license_info)
help_menu.add_separator()
help_menu.add_command(label="About", command=self.show_about)
"""

# ============================================================================
# STEP 4: Add these methods to HFTProGUI class
# ============================================================================

# Add these methods to the HFTProGUI class:

"""
    def show_license_info(self):
        '''Display current license information'''
        try:
            from license_manager import LicenseManager
            
            manager = LicenseManager()
            license_data = manager.load_license()
            
            if license_data.get("status") == "error":
                messagebox.showerror("Error", license_data.get("message"))
                return
            
            info = f'''
╔════════════════════════════════════════╗
║   AVENTA HFT PRO 2026 - LICENSE INFO   ║
╚════════════════════════════════════════╝

Serial Number:    {license_data.get('serial', 'N/A')}

Hardware ID:      {license_data.get('hardware_id', 'N/A')}

Status:           {license_data.get('status', 'N/A').upper()}

Version:          {license_data.get('version', 'N/A')}

Activation Date:  {license_data.get('activation_date', 'N/A')}

════════════════════════════════════════
This license is permanently bound to 
this computer and cannot be transferred 
to another device.
════════════════════════════════════════
            '''
            
            messagebox.showinfo("License Information", info)
        
        except ImportError:
            messagebox.showinfo(
                "License System",
                "License system is not installed."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load license info: {e}")
    
    def show_about(self):
        '''Display About dialog'''
        about_text = '''
AVENTA HFT PRO 2026 v7.3.6

Professional Algorithmic Trading Platform
Real-time Market Analysis & Automated Execution

© 2026 Aventa Trading Systems
All Rights Reserved

Built with Python, MetaTrader5, and Advanced ML Models
        '''
        messagebox.showinfo("About Aventa HFT Pro", about_text)
"""

# ============================================================================
# FINAL CHECKLIST
# ============================================================================

# ☐ Copy license_manager.py to project folder
# ☐ Copy license_check.py to project folder
# ☐ Edit Aventa_HFT_Pro_2026_v7_3_6.py:
#   ☐ Add 2 import lines after line 7
#   ☐ Modify main block (lines 5582-5585)
#   ☐ Add menu code to __init__
#   ☐ Add show_license_info() method to class
#   ☐ Add show_about() method to class (optional)
# ☐ Install cryptography: pip install cryptography
# ☐ Test program runs and shows license activation dialog
# ☐ Test serial generation tool: python serial_generator.py
# ☐ Test activation and license verification

# ============================================================================
# QUICK COPY-PASTE CODE
# ============================================================================

# COPY THIS TO ADD AT TOP OF FILE (after existing imports):
"""
try:
    from license_check import enforce_license_on_startup
    from license_manager import LicenseManager
    LICENSE_SYSTEM_AVAILABLE = True
except ImportError:
    LICENSE_SYSTEM_AVAILABLE = False
    print("Warning: License system not available")
"""

# COPY THIS TO MODIFY MAIN BLOCK:
"""
if __name__ == "__main__":
    # Check license
    if LICENSE_SYSTEM_AVAILABLE:
        if not enforce_license_on_startup():
            sys.exit(1)
    
    # Start application
    root = tk.Tk()
    app = HFTProGUI(root)
    root.mainloop()
"""

# ============================================================================

print(__doc__)
