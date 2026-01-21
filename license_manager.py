"""
Aventa HFT Pro 2026 - License & Serial Number Management
Manages license activation, verification, and hardware binding
"""

import hashlib
import json
import os
import uuid
import hmac
from datetime import datetime, timedelta
from pathlib import Path
import socket
import subprocess
from cryptography.fernet import Fernet
import base64


class HardwareIDGenerator:
    """Generate unique hardware ID based on system information"""
    
    @staticmethod
    def get_hardware_id():
        """
        Generate a unique hardware ID combining multiple hardware identifiers
        This ensures the same serial number cannot be used on different computers
        """
        try:
            hardware_info = []
            
            # Get MAC Address (most reliable identifier)
            try:
                mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                                       for i in range(0, 48, 8)][::-1])
                hardware_info.append(mac_address)
            except:
                pass
            
            # Get Processor Information
            try:
                if os.name == 'nt':  # Windows
                    result = subprocess.check_output(
                        "wmic cpu get ProcessorId",
                        shell=True,
                        stderr=subprocess.DEVNULL
                    ).decode().split('\n')[1].strip()
                    hardware_info.append(result)
            except:
                pass
            
            # Get Disk Serial Number
            try:
                if os.name == 'nt':  # Windows
                    result = subprocess.check_output(
                        "wmic logicaldisk get VolumeSerialNumber",
                        shell=True,
                        stderr=subprocess.DEVNULL
                    ).decode().split('\n')[1].strip()
                    hardware_info.append(result)
            except:
                pass
            
            # Get Hostname
            try:
                hostname = socket.gethostname()
                hardware_info.append(hostname)
            except:
                pass
            
            # Combine all hardware info
            combined = '|'.join(hardware_info)
            
            # Generate hash
            hardware_id = hashlib.sha256(combined.encode()).hexdigest()[:16].upper()
            
            return hardware_id
        
        except Exception as e:
            print(f"Error generating hardware ID: {e}")
            return "ERROR_HWID"


class SerialKeyGenerator:
    """Generate and validate serial keys"""
    
    def __init__(self, master_key: str = "AVENTA_HFT_PRO_2026"):
        """
        Initialize with a master key
        master_key: Secret key used for HMAC validation
        """
        self.master_key = master_key
    
    @staticmethod
    def generate_serial(hardware_id: str, expiry_days: int = 365) -> str:
        """
        Generate a serial key tied to specific hardware ID
        Format: AV-XXXX-XXXX-XXXX-HHHH
        Where HHHH is derived from hardware ID
        
        expiry_days: -1 for unlimited, 7 for trial, or any positive number for days
        """
        # Create a checksum from hardware ID
        hw_check = hashlib.md5(hardware_id.encode()).hexdigest()[:4].upper()
        
        # Generate random portion
        random_part = str(uuid.uuid4()).replace('-', '')[:16].upper()
        
        # Format as serial: AV-XXXX-XXXX-XXXX-HHHH
        serial = f"AV-{random_part[0:4]}-{random_part[4:8]}-{random_part[8:12]}-{hw_check}"
        
        return serial
    
    def validate_serial(self, serial: str, hardware_id: str) -> bool:
        """
        Validate if serial key is valid for given hardware ID
        """
        try:
            if not serial.startswith("AV-"):
                return False
            
            parts = serial.split('-')
            if len(parts) != 5:
                return False
            
            # Extract hardware check from serial
            serial_hw_check = parts[4]
            
            # Generate expected hardware check
            expected_hw_check = hashlib.md5(hardware_id.encode()).hexdigest()[:4].upper()
            
            # Compare
            return serial_hw_check == expected_hw_check
        
        except Exception as e:
            print(f"Error validating serial: {e}")
            return False


class LicenseManager:
    """Manage software license activation and verification"""
    
    def __init__(self, license_file: str = "license.json"):
        """Initialize license manager"""
        self.license_file = Path(license_file)
        self.hardware_generator = HardwareIDGenerator()
        self.serial_generator = SerialKeyGenerator()
        self.encryption_key = self._generate_encryption_key()
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key from hardware ID"""
        hardware_id = self.hardware_generator.get_hardware_id()
        # Create a 32-byte key from hardware ID
        key = base64.urlsafe_b64encode(
            hashlib.sha256(hardware_id.encode()).digest()
        )
        return key
    
    def get_hardware_id(self) -> str:
        """Get current system hardware ID"""
        return self.hardware_generator.get_hardware_id()
    
    def create_license(self, serial: str, expiry_days: int = -1) -> dict:
        """
        Create a license file with serial number
        
        Args:
            serial: Serial number to activate
            expiry_days: -1 for unlimited, 7 for trial, or positive number for days
        
        Returns license data containing activation information
        """
        hardware_id = self.get_hardware_id()
        
        # Validate serial matches hardware
        if not self.serial_generator.validate_serial(serial, hardware_id):
            return {
                "status": "error",
                "message": "Serial number does not match this hardware"
            }
        
        # Calculate expiry date
        if expiry_days == -1:
            # Unlimited license
            expiry_date = None
            license_type = "unlimited"
        else:
            # Trial or limited license
            expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
            if expiry_days == 7:
                license_type = "trial"
            else:
                license_type = "limited"
        
        license_data = {
            "serial": serial,
            "hardware_id": hardware_id,
            "activation_date": datetime.now().isoformat(),
            "expiry_date": expiry_date,
            "license_type": license_type,
            "expiry_days": expiry_days,
            "status": "active",
            "version": "7.3.6"
        }
        
        return license_data
    
    def save_license(self, license_data: dict) -> bool:
        """Save encrypted license file"""
        try:
            license_json = json.dumps(license_data)
            
            # Encrypt the license data
            cipher = Fernet(self.encryption_key)
            encrypted = cipher.encrypt(license_json.encode())
            
            # Save to file
            with open(self.license_file, 'wb') as f:
                f.write(encrypted)
            
            return True
        except Exception as e:
            print(f"Error saving license: {e}")
            return False
    
    def load_license(self) -> dict:
        """Load and decrypt license file"""
        try:
            if not self.license_file.exists():
                return {"status": "error", "message": "License file not found"}
            
            with open(self.license_file, 'rb') as f:
                encrypted = f.read()
            
            # Decrypt
            cipher = Fernet(self.encryption_key)
            decrypted = cipher.decrypt(encrypted)
            license_data = json.loads(decrypted.decode())
            
            return license_data
        
        except Exception as e:
            print(f"Error loading license: {e}")
            return {"status": "error", "message": f"Failed to load license: {e}"}
    
    def verify_license(self) -> tuple[bool, str]:
        """
        Verify if license is valid and not expired
        Returns (is_valid, message)
        """
        try:
            license_data = self.load_license()
            
            if "status" in license_data and license_data["status"] == "error":
                return False, license_data.get("message", "License verification failed")
            
            hardware_id = self.get_hardware_id()
            
            # Check if hardware matches
            if license_data.get("hardware_id") != hardware_id:
                return False, "License is bound to a different hardware"
            
            # Check if serial is still valid
            serial = license_data.get("serial")
            if not self.serial_generator.validate_serial(serial, hardware_id):
                return False, "Invalid serial number"
            
            if license_data.get("status") != "active":
                return False, "License is not active"
            
            # Check expiry date
            expiry_date_str = license_data.get("expiry_date")
            if expiry_date_str is not None:  # None means unlimited
                expiry_date = datetime.fromisoformat(expiry_date_str)
                if datetime.now() > expiry_date:
                    days_expired = (datetime.now() - expiry_date).days
                    return False, f"License has expired {days_expired} days ago. Please renew your license."
            
            return True, "License is valid"
        
        except Exception as e:
            return False, f"Error verifying license: {e}"
    
    def deactivate_license(self) -> bool:
        """Deactivate current license"""
        try:
            if self.license_file.exists():
                self.license_file.unlink()
            return True
        except Exception as e:
            print(f"Error deactivating license: {e}")
            return False


class LicenseDialog:
    """GUI Dialog for license activation"""
    
    def __init__(self, parent, license_manager: LicenseManager):
        """Initialize license dialog"""
        self.parent = parent
        self.license_manager = license_manager
        self.result = None
    
    def show_activation_dialog(self) -> bool:
        """Show license activation dialog"""
        import tkinter as tk
        from tkinter import messagebox, simpledialog
        
        hardware_id = self.license_manager.get_hardware_id()
        
        # Create dialog window
        dialog = tk.Toplevel(self.parent)
        dialog.title("🔐 Aventa HFT Pro - License Activation")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Center on parent
        dialog.transient(self.parent)
        
        # Main frame
        import tkinter.font as tkFont
        main_frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        title_label = tk.Label(
            main_frame,
            text="License Activation",
            font=title_font,
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=(0, 10))
        
        # Hardware ID display
        hw_frame = tk.LabelFrame(main_frame, text="Hardware ID (Unique to this PC)", 
                                  bg="#f0f0f0", padx=10, pady=10)
        hw_frame.pack(fill=tk.X, pady=(0, 15))
        
        hw_text = tk.Text(hw_frame, height=2, width=50, wrap=tk.WORD)
        hw_text.insert(1.0, hardware_id)
        hw_text.config(state=tk.DISABLED)
        hw_text.pack()
        
        # Serial input
        serial_frame = tk.LabelFrame(main_frame, text="Enter Serial Number", 
                                      bg="#f0f0f0", padx=10, pady=10)
        serial_frame.pack(fill=tk.X, pady=(0, 15))
        
        serial_entry = tk.Entry(serial_frame, font=("Arial", 12))
        serial_entry.pack(fill=tk.X)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        def activate():
            serial = serial_entry.get().strip().upper()
            if not serial:
                messagebox.showerror("Error", "Please enter a serial number")
                return
            
            license_data = self.license_manager.create_license(serial)
            
            if license_data.get("status") == "error":
                messagebox.showerror("Activation Failed", license_data.get("message"))
                return
            
            # Save license
            if self.license_manager.save_license(license_data):
                messagebox.showinfo(
                    "Success",
                    "License activated successfully!\n\n"
                    "This serial number is now bound to this computer."
                )
                self.result = True
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to save license")
        
        activate_btn = tk.Button(
            button_frame,
            text="Activate",
            command=activate,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        activate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=lambda: dialog.destroy(),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT)
        
        self.parent.wait_window(dialog)
        return self.result
    
    def show_license_info(self):
        """Show current license information"""
        import tkinter as tk
        from tkinter import messagebox
        
        license_data = self.license_manager.load_license()
        
        if license_data.get("status") == "error":
            messagebox.showerror("Error", license_data.get("message"))
            return
        
        # Format expiry information
        license_type = license_data.get('license_type', 'unknown')
        expiry_date = license_data.get('expiry_date')
        
        if expiry_date:
            expiry_dt = datetime.fromisoformat(expiry_date)
            days_remaining = (expiry_dt - datetime.now()).days
            if days_remaining < 0:
                expiry_info = f"Expired {abs(days_remaining)} days ago"
            else:
                expiry_info = f"Expires in {days_remaining} days ({expiry_date[:10]})"
        else:
            expiry_info = "No expiry (Unlimited)"
        
        info = f"""
        Serial: {license_data.get('serial')}
        Hardware ID: {license_data.get('hardware_id')}
        Activation Date: {license_data.get('activation_date')[:10]}
        License Type: {license_type.upper()}
        Expiry: {expiry_info}
        Status: {license_data.get('status')}
        Version: {license_data.get('version')}
        """
        
        messagebox.showinfo("License Information", info)


if __name__ == "__main__":
    # Test the license manager
    manager = LicenseManager()
    
    print("=" * 60)
    print("AVENTA HFT PRO 2026 - LICENSE SYSTEM TEST")
    print("=" * 60)
    
    # Get hardware ID
    hardware_id = manager.get_hardware_id()
    print(f"\nHardware ID: {hardware_id}")
    
    # Generate a test serial
    serial = manager.serial_generator.generate_serial(hardware_id)
    print(f"Generated Serial: {serial}")
    
    # Validate serial
    is_valid = manager.serial_generator.validate_serial(serial, hardware_id)
    print(f"Serial Valid: {is_valid}")
    
    # Create license
    license_data = manager.create_license(serial)
    print(f"\nLicense Data:\n{json.dumps(license_data, indent=2)}")
    
    # Save license
    if manager.save_license(license_data):
        print("\nLicense saved successfully")
    
    # Load and verify
    loaded = manager.load_license()
    print(f"\nLoaded License:\n{json.dumps(loaded, indent=2)}")
    
    is_valid, message = manager.verify_license()
    print(f"\nLicense Valid: {is_valid}")
    print(f"Message: {message}")
    
    print("\n" + "=" * 60)
