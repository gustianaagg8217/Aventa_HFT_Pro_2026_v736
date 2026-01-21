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
        self.root.geometry("750x750")
        self.root.resizable(False, False)
        
        self.serial_generator = SerialKeyGenerator()
        self.hardware_generator = HardwareIDGenerator()
        
        self.setup_ui()
    
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


class ModernStyle:
    """Modern color scheme"""
    # Primary colors
    PRIMARY = "#2E86AB"      # Professional Blue
    SECONDARY = "#A23B72"    # Purple accent
    SUCCESS = "#06A77D"      # Green
    ACCENT = "#F18F01"       # Orange accent
    
    # Background colors
    BG_DARK = "#1A1F36"      # Dark background
    BG_LIGHT = "#F5F7FA"     # Light background
    BG_CARD = "#FFFFFF"      # Card background
    
    # Text colors
    TEXT_PRIMARY = "#2D3436"  # Dark text
    TEXT_SECONDARY = "#636E72" # Gray text
    TEXT_LIGHT = "#FFFFFF"    # Light text
    
    # Borders
    BORDER = "#DFE6E9"        # Light border


class SerialGeneratorGUI:
    """GUI tool for generating serial numbers"""
    
    def __init__(self, root):
        """Initialize the serial generator GUI"""
        self.root = root
        self.root.title("🔑 Aventa HFT Pro - Serial Number Generator")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        self.root.configure(bg=ModernStyle.BG_LIGHT)
        
        self.serial_generator = SerialKeyGenerator()
        self.hardware_generator = HardwareIDGenerator()
        
        self.setup_styles()
        self.setup_ui()
    
    def setup_styles(self):
        """Setup modern styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure("TFrame", background=ModernStyle.BG_LIGHT)
        style.configure("TLabel", background=ModernStyle.BG_LIGHT, foreground=ModernStyle.TEXT_PRIMARY)
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground=ModernStyle.PRIMARY)
        style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"), foreground=ModernStyle.PRIMARY)
        
        # Labelframe with rounded appearance
        style.configure("TLabelframe", background=ModernStyle.BG_LIGHT, bordercolor=ModernStyle.BORDER)
        style.configure("TLabelframe.Label", background=ModernStyle.BG_LIGHT, foreground=ModernStyle.PRIMARY, font=("Segoe UI", 11, "bold"))
        
        # Button styles
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Accent.TButton", background=[("active", ModernStyle.SECONDARY)])
        
        # Entry style
        style.configure("TEntry", padding=6, fieldbackground=ModernStyle.BG_CARD)
        
    def setup_ui(self):
        """Setup the user interface with scrollbar"""
        # Create main container with scrollbar
        container = tk.Frame(self.root, bg=ModernStyle.BG_LIGHT)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(container, bg=ModernStyle.BG_LIGHT, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create scrollbar with modern styling
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame inside canvas
        main_frame = tk.Frame(canvas, bg=ModernStyle.BG_LIGHT)
        canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)
        
        # Add padding
        main_frame.configure(padx=12, pady=12)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=ModernStyle.PRIMARY, height=50)
        header_frame.pack(fill=tk.X, pady=(0, 10), ipady=8, expand=False)
        
        title_label = tk.Label(
            header_frame,
            text="🔑 Serial Number Generator",
            font=("Segoe UI", 14, "bold"),
            bg=ModernStyle.PRIMARY,
            fg=ModernStyle.TEXT_LIGHT
        )
        title_label.pack(side=tk.LEFT, padx=12, pady=5)
        
        # Input section - CUSTOM FRAME
        input_frame = tk.Frame(main_frame, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=1)
        input_frame.pack(fill=tk.X, pady=8)
        input_frame.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        # Section title
        input_title = tk.Label(
            input_frame,
            text="Customer Hardware ID",
            font=("Segoe UI", 10, "bold"),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.PRIMARY
        )
        input_title.pack(anchor=tk.W, padx=10, pady=(8, 5))
        
        # Input label and field
        input_label = tk.Label(
            input_frame,
            text="Enter Hardware ID:",
            font=("Segoe UI", 9),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY
        )
        input_label.pack(anchor=tk.W, padx=10)
        
        self.hardware_id_entry = tk.Entry(
            input_frame,
            width=50,
            font=("Courier", 9),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        self.hardware_id_entry.pack(fill=tk.X, padx=10, pady=(3, 5))
        self.hardware_id_entry.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        hint_label = tk.Label(
            input_frame,
            text="(Customer should get this from their system)",
            font=("Segoe UI", 8),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_SECONDARY
        )
        hint_label.pack(anchor=tk.W, padx=10, pady=(0, 8))
        
        # OR section
        or_frame = tk.Frame(main_frame, bg=ModernStyle.BG_LIGHT)
        or_frame.pack(fill=tk.X, pady=6)
        
        ttk.Separator(or_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 2))
        or_label = tk.Label(or_frame, text="OR", font=("Segoe UI", 9), bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_SECONDARY)
        or_label.pack()
        ttk.Separator(or_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Auto-generate section
        auto_frame = tk.Frame(main_frame, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=1)
        auto_frame.pack(fill=tk.X, pady=8)
        auto_frame.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        auto_title = tk.Label(
            auto_frame,
            text="Auto-Generate (for Testing)",
            font=("Segoe UI", 10, "bold"),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.PRIMARY
        )
        auto_title.pack(anchor=tk.W, padx=10, pady=(8, 6))
        
        auto_button = tk.Button(
            auto_frame,
            text="🎲 Generate Test Hardware ID",
            command=self.generate_test_hardware_id,
            bg=ModernStyle.PRIMARY,
            fg=ModernStyle.TEXT_LIGHT,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2"
        )
        auto_button.pack(padx=10, pady=(0, 8))
        
        # Output section
        output_frame = tk.Frame(main_frame, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=1)
        output_frame.pack(fill=tk.X, pady=8)
        output_frame.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        output_title = tk.Label(
            output_frame,
            text="Generated Serial Number",
            font=("Segoe UI", 10, "bold"),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.PRIMARY
        )
        output_title.pack(anchor=tk.W, padx=10, pady=(8, 6))
        
        self.serial_display = tk.Text(
            output_frame,
            height=3,
            width=50,
            font=("Courier", 10, "bold"),
            fg=ModernStyle.SUCCESS,
            bg="#F0F8F4",
            relief=tk.FLAT,
            bd=0
        )
        self.serial_display.pack(fill=tk.X, padx=10, pady=6)
        
        # License Type section
        license_frame = tk.Frame(main_frame, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=1)
        license_frame.pack(fill=tk.X, pady=8)
        license_frame.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        license_title = tk.Label(
            license_frame,
            text="License Type",
            font=("Segoe UI", 10, "bold"),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.PRIMARY
        )
        license_title.pack(anchor=tk.W, padx=10, pady=(8, 5))
        
        self.license_type_var = tk.StringVar(value="unlimited")
        
        # Radio buttons dengan custom styling
        radio_frame = tk.Frame(license_frame, bg=ModernStyle.BG_CARD)
        radio_frame.pack(anchor=tk.W, padx=10, pady=3)
        
        radio1 = tk.Radiobutton(
            radio_frame,
            text="🔓 Unlimited (No expiry)",
            variable=self.license_type_var,
            value="unlimited",
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
            cursor="hand2",
            selectcolor=ModernStyle.BG_CARD
        )
        radio1.pack(anchor=tk.W, pady=2)
        
        radio2 = tk.Radiobutton(
            radio_frame,
            text="⏱️ Trial 7 Days (auto expire)",
            variable=self.license_type_var,
            value="trial",
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
            cursor="hand2",
            selectcolor=ModernStyle.BG_CARD
        )
        radio2.pack(anchor=tk.W, pady=2)
        
        radio3 = tk.Radiobutton(
            radio_frame,
            text="📅 Custom Days",
            variable=self.license_type_var,
            value="custom",
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
            cursor="hand2",
            selectcolor=ModernStyle.BG_CARD
        )
        radio3.pack(anchor=tk.W, pady=2)
        
        custom_days_frame = tk.Frame(license_frame, bg=ModernStyle.BG_CARD)
        custom_days_frame.pack(anchor=tk.W, padx=30, pady=(3, 8))
        
        custom_label = tk.Label(
            custom_days_frame,
            text="Number of days:",
            font=("Segoe UI", 9),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY
        )
        custom_label.pack(side=tk.LEFT, padx=(0, 8))
        
        self.custom_days_entry = tk.Entry(
            custom_days_frame,
            width=8,
            font=("Segoe UI", 9),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        self.custom_days_entry.pack(side=tk.LEFT)
        self.custom_days_entry.insert(0, "30")
        self.custom_days_entry.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=ModernStyle.BG_LIGHT)
        button_frame.pack(fill=tk.X, pady=8)
        
        generate_btn = tk.Button(
            button_frame,
            text="✨ Generate Serial",
            command=self.generate_serial,
            bg=ModernStyle.SUCCESS,
            fg=ModernStyle.TEXT_LIGHT,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = tk.Button(
            button_frame,
            text="📋 Copy Serial",
            command=self.copy_serial,
            bg=ModernStyle.PRIMARY,
            fg=ModernStyle.TEXT_LIGHT,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="🔄 Clear",
            command=self.clear_all,
            bg=ModernStyle.ACCENT,
            fg=ModernStyle.TEXT_LIGHT,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Log section
        log_title = tk.Label(
            main_frame,
            text="Generation Log",
            font=("Segoe UI", 10, "bold"),
            bg=ModernStyle.BG_LIGHT,
            fg=ModernStyle.PRIMARY
        )
        log_title.pack(anchor=tk.W, pady=(8, 6))
        
        log_frame = tk.Frame(main_frame, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        log_frame.configure(highlightbackground=ModernStyle.BORDER, highlightthickness=1)
        
        self.log_text = tk.Text(
            log_frame,
            height=6,
            width=60,
            font=("Courier", 8),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log scrollbar
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Initial log
        self.log("Serial Number Generator Started")
        self.log("=" * 60)
        self.log("Instructions:")
        self.log("1. Customer provides their Hardware ID from their system")
        self.log("2. Enter the Hardware ID and select License Type")
        self.log("3. Click 'Generate Serial'")
        self.log("4. Send the serial number to the customer")
        self.log("=" * 60)
        
        # Update canvas scroll region
        main_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
    
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
