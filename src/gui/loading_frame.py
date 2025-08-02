import tkinter as tk
from tkinter import ttk
from typing import Optional

class LoadingFrame(tk.Frame):
    ANIMATION_SPEED = 2  # Progress points per animation frame
    def __init__(self, master=None):
        super().__init__(master, bg="#040F16")  # Set dark navy background
        self.master = master
        self._current_progress = 0
        self._target_progress = 0
        self._animation_id: Optional[str] = None
        
        # Configure style for progress bar
        style = ttk.Style()
        style.configure("Custom.Horizontal.TProgressbar",
                      troughcolor="#040F16",
                      bordercolor="#FBFBFF",
                      background="#55A76A",
                      lightcolor="#55A76A",
                      darkcolor="#55A76A")
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and setup the loading screen widgets."""
        # Create loading label
        # Create frame for labels
        self.label_frame = tk.Frame(self, bg="#040F16")
        self.label_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Create title label
        self.loading_label = tk.Label(
            self.label_frame,
            text="Analyzing Stock Sentiment...",
            font=("Helvetica", 12, "bold"),
            wraplength=400,  # Prevent text from being cut off
            bg="#040F16",   # Dark navy background
            fg="#FBFBFF"    # Almost white text
        )
        self.loading_label.pack(pady=10)
        
        # Create progress bar with increased width
        self.progress_bar = ttk.Progressbar(
            self.label_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=10)
        
        # Create status label with increased width and proper text wrapping
        self.status_label = tk.Label(
            self.label_frame,
            text="Starting analysis...",
            font=("Helvetica", 10),
            wraplength=400,  # Ensure long text wraps properly
            justify=tk.CENTER,  # Center-align wrapped text
            bg="#040F16",   # Dark navy background
            fg="#FBFBFF"    # Almost white text
        )
        self.status_label.pack(pady=10)
        
    def _animate_progress(self):
        """Animate the progress bar smoothly towards target value."""
        if self._current_progress < self._target_progress:
            self._current_progress = min(
                self._current_progress + self.ANIMATION_SPEED,
                self._target_progress
            )
            self.progress_bar["value"] = self._current_progress
            self.update_idletasks()
            
            if self._current_progress < self._target_progress:
                self._animation_id = self.after(20, self._animate_progress)
            else:
                self._animation_id = None
                
    def update_progress(self, value: int, status: str = None):
        """Update progress bar value and status text."""
        # Cancel any ongoing animation
        if self._animation_id:
            self.after_cancel(self._animation_id)
            
        self._target_progress = value
        self._animate_progress()
        
        if status:
            self.status_label["text"] = status
        
    def reset(self):
        """Reset progress bar and status text."""
        if self._animation_id:
            self.after_cancel(self._animation_id)
        
        self._current_progress = 0
        self._target_progress = 0
        self.progress_bar["value"] = 0
        self.status_label["text"] = "Starting analysis..."
        self.update()