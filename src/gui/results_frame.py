import tkinter as tk
from typing import List

class ResultsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#040F16")  # Set dark navy background
        self.master = master
        # Create container frame for better layout control
        self.container = tk.Frame(self, bg="#040F16")
        self.container.pack(expand=True, fill=tk.BOTH)
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and setup the results display widgets."""
        # Create container frames for bulls and bears
        self.bull_frame = tk.LabelFrame(
            self.container,
            text="Bullish Stocks",
            padx=10,
            pady=5,
            bg="#040F16",
            fg="#FBFBFF",
            font=("Helvetica", 10, "bold"),
            height=150  # Fixed height to reduce empty space
        )
        self.bull_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.bull_frame.pack_propagate(False)  # Maintain fixed height
        
        self.bear_frame = tk.LabelFrame(
            self.container,
            text="Bearish Stocks",
            padx=10,
            pady=5,
            bg="#040F16",
            fg="#FBFBFF",
            font=("Helvetica", 10, "bold"),
            height=150  # Fixed height to reduce empty space
        )
        self.bear_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.bear_frame.pack_propagate(False)  # Maintain fixed height
        
        # Create labels for stocks (initially empty)
        self.bull_labels = []
        self.bear_labels = []
        
        for i in range(3):
            # Bullish labels
            label = tk.Label(
                self.bull_frame,
                text=f"{i+1}. -",
                font=("Helvetica", 12),
                anchor="w",
                bg="#040F16",
                fg="#55A76A"  # Bullish green
            )
            label.pack(pady=5, fill=tk.X)
            self.bull_labels.append(label)
            
            # Bearish labels
            label = tk.Label(
                self.bear_frame,
                text=f"{i+1}. -",
                font=("Helvetica", 12),
                anchor="w",
                bg="#040F16",
                fg="#E63B2E"  # Bearish red
            )
            label.pack(pady=5, fill=tk.X)
            self.bear_labels.append(label)
            
        # Create Analyze Again button
        # Create bottom frame for button
        self.button_frame = tk.Frame(self, bg="#040F16")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 20))
        
        # Create Analyze Again button
        self.analyze_button = tk.Button(
            self.button_frame,
            text="Analyze Again",
            command=lambda: self._on_analyze_click(),  # Wrap in lambda for extra safety
            bg="#040F16",
            fg="#FBFBFF",
            activebackground="#0B1B24",
            activeforeground="#FBFBFF",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=20,
            pady=5,
            font=("Helvetica", 10)
        )
        self.analyze_button.pack(pady=10)
        
    def _on_analyze_click(self):
        """Callback for Analyze Again button - to be set by main app."""
        print("Button clicked!")  # Debug print
        if hasattr(self, '_on_analyze_click_callback'):
            print(f"Calling analyze callback: {self._on_analyze_click_callback}")  # Debug print
            self._on_analyze_click_callback()
        else:
            print("No callback set!")  # Debug print
        
    def set_analyze_callback(self, callback):
        """Set the callback function for Analyze Again button."""
        print(f"Setting analyze callback: {callback}")  # Debug print
        self._on_analyze_click_callback = callback
        # Also update the button's command directly
        self.analyze_button.configure(command=lambda: self._on_analyze_click())
        
    def display_results(self, bullish: List[str], bearish: List[str]):
        """Update the display with new results."""
        # Update bullish stocks
        for i, ticker in enumerate(bullish[:3]):
            self.bull_labels[i]["text"] = f"{i+1}. {ticker}"
            
        # Update bearish stocks
        for i, ticker in enumerate(bearish[:3]):
            self.bear_labels[i]["text"] = f"{i+1}. {ticker}"
            
    def reset(self):
        """Reset the display to initial state."""
        for i in range(3):
            self.bull_labels[i]["text"] = f"{i+1}. -"
            self.bear_labels[i]["text"] = f"{i+1}. -"