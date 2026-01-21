"""
Serial Number Generator Tool for Aventa HFT Pro
Admin tool to generate serial numbers for customers with expiry options
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime, timedelta
from pathlib import Path
from license_manager import SerialKeyGenerator, HardwareIDGenerator, LicenseManager


class SerialGeneratorGUI:
    """GUI tool for generating serial numbers"""
    
    def __init__(self, root):
        """Initialize the serial generator GUI"""
        self.root = root
        self.root.title("🔑 Aventa HFT Pro - Serial Number Generator")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.serial_generator = SerialKeyGenerator()
        self.hardware_generator = HardwareIDGenerator()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Serial Number Generator",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Customer Hardware ID", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(input_frame, text="Enter Hardware ID:").pack(anchor=tk.W)
        
        self.hardware_id_entry = ttk.Entry(input_frame, width=60, font=("Courier", 10))
        self.hardware_id_entry.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(
            input_frame,
            text="(Customer should get this from their system)",
            font=("Arial", 9),
            foreground="gray"
        ).pack(anchor=tk.W)
        
        # OR section
        or_frame = ttk.Frame(main_frame)
        or_frame.pack(fill=tk.X, pady=15)
        
        ttk.Separator(or_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 5))
        ttk.Label(or_frame, text="OR", justify=tk.CENTER).pack()
        ttk.Separator(or_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 0))
        
        # Auto-generate section
        auto_frame = ttk.LabelFrame(main_frame, text="Auto-Generate (for Testing)", padding="10")
        auto_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(
            auto_frame,
            text="Generate Test Hardware ID",
            command=self.generate_test_hardware_id
        ).pack()
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Generated Serial Number", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.serial_display = tk.Text(
            output_frame,
            height=3,
            width=60,
            font=("Courier", 12, "bold"),
            fg="#4CAF50",
            bg="#f5f5f5"
        )
        self.serial_display.pack(fill=tk.X, pady=(0, 5))
        
        # License Type section
        license_frame = ttk.LabelFrame(main_frame, text="License Type", padding="10")
        license_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.license_type_var = tk.StringVar(value="unlimited")
        
        ttk.Radiobutton(
            license_frame,
            text="🔓 Unlimited (No expiry)",
            variable=self.license_type_var,
            value="unlimited"
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(
            license_frame,
            text="⏱️ Trial 7 Days (auto expire)",
            variable=self.license_type_var,
            value="trial"
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(
            license_frame,
            text="📅 Custom Days",
            variable=self.license_type_var,
            value="custom"
        ).pack(anchor=tk.W, pady=5)
        
        custom_days_frame = ttk.Frame(license_frame)
        custom_days_frame.pack(anchor=tk.W, pady=5, padx=(20, 0))
        
        ttk.Label(custom_days_frame, text="Number of days:").pack(side=tk.LEFT, padx=(0, 5))
        self.custom_days_entry = ttk.Entry(custom_days_frame, width=10)
        self.custom_days_entry.pack(side=tk.LEFT)
        self.custom_days_entry.insert(0, "30")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(
            button_frame,
            text="Generate Serial",
            command=self.generate_serial
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Copy Serial",
            command=self.copy_serial
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=5)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Generation Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            width=70,
            font=("Courier", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial log
        self.log("Serial Number Generator Started")
        self.log("=" * 60)
        self.log("Instructions:")
        self.log("1. Customer provides their Hardware ID from their system")
        self.log("2. Enter the Hardware ID and click 'Generate Serial'")
        self.log("3. Send the serial number to the customer")
        self.log("4. Serial can only be activated on that specific computer")
        self.log("=" * 60)
    
    def generate_test_hardware_id(self):
        """Generate a test hardware ID"""
        test_hw_id = self.hardware_generator.get_hardware_id()
        self.hardware_id_entry.delete(0, tk.END)
        self.hardware_id_entry.insert(0, test_hw_id)
        self.log(f"Generated test Hardware ID: {test_hw_id}")
    
    def generate_serial(self):
        """Generate serial number from hardware ID with expiry option"""
        hardware_id = self.hardware_id_entry.get().strip()
        
        if not hardware_id:
            messagebox.showerror("Error", "Please enter a Hardware ID")
            return
        
        if len(hardware_id) < 8:
            messagebox.showerror("Error", "Hardware ID seems too short")
            return
        
        try:
            # Determine expiry days
            license_type = self.license_type_var.get()
            
            if license_type == "unlimited":
                expiry_days = -1
                expiry_label = "Unlimited"
            elif license_type == "trial":
                expiry_days = 7
                expiry_label = "Trial (7 days)"
            elif license_type == "custom":
                try:
                    expiry_days = int(self.custom_days_entry.get())
                    if expiry_days <= 0:
                        messagebox.showerror("Error", "Number of days must be positive")
                        return
                    expiry_label = f"Limited ({expiry_days} days)"
                except ValueError:
                    messagebox.showerror("Error", "Invalid number of days")
                    return
            else:
                expiry_days = -1
                expiry_label = "Unlimited"
            
            # Generate serial
            serial = self.serial_generator.generate_serial(hardware_id, expiry_days)
            
            # Display serial
            self.serial_display.delete(1.0, tk.END)
            self.serial_display.insert(1.0, serial)
            
            # Log
            self.log(f"✓ Generated Serial: {serial}")
            self.log(f"  Hardware ID: {hardware_id}")
            self.log(f"  License Type: {expiry_label}")
            if expiry_days > 0:
                expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
                self.log(f"  Expiry Date: {expiry_date}")
            self.log(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Save to records
            self.save_record(hardware_id, serial, expiry_days, expiry_label)
            
            info_text = f"Serial Generated:\n\n{serial}\n\nType: {expiry_label}"
            messagebox.showinfo("Success", info_text)
        
        except Exception as e:
            self.log(f"✗ Error: {e}")
            messagebox.showerror("Error", f"Failed to generate serial: {e}")
    
    def copy_serial(self):
        """Copy serial to clipboard"""
        try:
            serial = self.serial_display.get(1.0, tk.END).strip()
            if not serial:
                messagebox.showerror("Error", "No serial to copy")
                return
            
            self.root.clipboard_clear()
            self.root.clipboard_append(serial)
            self.log(f"✓ Copied to clipboard: {serial}")
            messagebox.showinfo("Success", "Serial copied to clipboard!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Copy failed: {e}")
    
    def clear_all(self):
        """Clear all fields"""
        self.hardware_id_entry.delete(0, tk.END)
        self.serial_display.delete(1.0, tk.END)
        self.log("Cleared all fields")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def save_record(self, hardware_id: str, serial: str, expiry_days: int = -1, expiry_label: str = "Unlimited"):
        """Save generation record with expiry information"""
        try:
            records_file = Path("serial_records.json")
            
            # Load existing records
            if records_file.exists():
                with open(records_file, 'r') as f:
                    records = json.load(f)
            else:
                records = []
            
            # Calculate expiry date
            if expiry_days == -1:
                expiry_date = None
            else:
                expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
            
            # Add new record
            records.append({
                "serial": serial,
                "hardware_id": hardware_id,
                "generated": datetime.now().isoformat(),
                "license_type": expiry_label,
                "expiry_days": expiry_days,
                "expiry_date": expiry_date,
                "activated": False
            })
            
            # Save
            with open(records_file, 'w') as f:
                json.dump(records, f, indent=2)
        
        except Exception as e:
            self.log(f"Warning: Could not save record: {e}")


class AdminConsole:
    """Admin console for license management"""
    
    def __init__(self, root):
        """Initialize admin console"""
        self.root = root
        self.root.title("Admin Console - Aventa HFT Pro License Management")
        self.root.geometry("800x650")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup admin console UI"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generator tab
        generator_frame = ttk.Frame(notebook)
        notebook.add(generator_frame, text="Serial Generator")
        
        # Create generator GUI inside frame
        temp_root = tk.Tk()
        temp_root.withdraw()
        gen_gui = SerialGeneratorGUI(temp_root)
        
        # Records tab
        records_frame = ttk.Frame(notebook, padding="10")
        notebook.add(records_frame, text="Records")
        
        ttk.Label(
            records_frame,
            text="Serial Number Generation Records",
            font=("Arial", 14, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        records_text = scrolledtext.ScrolledText(
            records_frame,
            height=20,
            width=80,
            font=("Courier", 9)
        )
        records_text.pack(fill=tk.BOTH, expand=True)
        
        # Load records
        try:
            records_file = Path("serial_records.json")
            if records_file.exists():
                with open(records_file, 'r') as f:
                    records = json.load(f)
                
                records_text.insert(tk.END, json.dumps(records, indent=2))
        except Exception as e:
            records_text.insert(tk.END, f"Error loading records: {e}")
        
        records_text.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = SerialGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
