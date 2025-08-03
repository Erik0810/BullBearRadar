import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Dict, Any

from ..stock_performance.stock_data import StockData

class StockDetailsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#040F16")
        self.stock_data = StockData()
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and setup the stock details display widgets."""
        
        # Create header frame for title and back button
        self.header_frame = tk.Frame(self, bg="#040F16")
        self.header_frame.pack(fill=tk.X, padx=20, pady=(20,10))
        
        # Create left container for back button with specific dimensions
        self.back_container = tk.Frame(self.header_frame, bg="#040F16", width=120, height=40)
        self.back_container.pack(side=tk.LEFT, pady=5)
        self.back_container.pack_propagate(False)
        self.back_container.grid_propagate(False)
        
        # Back button with higher contrast styling
        self.back_button = tk.Button(
            self.back_container,
            text="← Back",
            command=self._on_back_click,
            bg="#1E90FF",  # Bright blue background
            fg="#FFFFFF",  # White text
            activebackground="#007FFF",  # Slightly darker blue when active
            activeforeground="#FFFFFF",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=15,
            pady=8,
            font=("Helvetica", 12, "bold")
        )
        self.back_button.place(relx=0, rely=0.5, anchor="w")  # Center vertically in container
        
        # Title label in center of header
        self.title_label = tk.Label(
            self.header_frame,
            text="",  # Will be set when displaying stock
            font=("Helvetica", 18, "bold"),  # Increased font size
            bg="#040F16",
            fg="#FBFBFF"
        )
        self.title_label.pack(side=tk.LEFT, expand=True, padx=(0, 120))  # Increased right padding to match back button
        
        # Key statistics frame
        self.stats_frame = tk.LabelFrame(
            self,
            text="Key Statistics",
            bg="#040F16",
            fg="#FBFBFF",
            font=("Helvetica", 12, "bold"),  # Increased font size
            padx=15,  # Increased horizontal padding
            pady=10   # Increased vertical padding
        )
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(0, 15))  # Increased bottom padding
        
        # Statistics labels
        stats_style = {
            "font": ("Helvetica", 11),  # Increased font size
            "bg": "#040F16",
            "fg": "#FBFBFF",
            "pady": 3  # Added vertical spacing between stats
        }
        
        self.price_label = tk.Label(
            self.stats_frame,
            text="Current Price: -",
            **stats_style
        )
        self.price_label.pack(anchor="w")
        
        self.market_cap_label = tk.Label(
            self.stats_frame,
            text="Market Cap: -",
            **stats_style
        )
        self.market_cap_label.pack(anchor="w")
        
        self.pe_ratio_label = tk.Label(
            self.stats_frame,
            text="P/E Ratio: -",
            **stats_style
        )
        self.pe_ratio_label.pack(anchor="w")
        
        # Price history chart
        # Price history chart with border
        self.chart_frame = tk.LabelFrame(
            self,
            text="Price History",
            bg="#040F16",
            fg="#FBFBFF",
            font=("Helvetica", 12, "bold"),
            padx=5,
            pady=5
        )
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))  # Increased bottom padding
        
    def _format_market_cap(self, market_cap: int) -> str:
        """Format market cap in billions/millions."""
        if market_cap >= 1e9:
            return f"${market_cap / 1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap / 1e6:.2f}M"
        else:
            return f"${market_cap:,.0f}"
            
    def display_stock(self, ticker: str):
        """Display stock details for the given ticker."""
        # Fetch stock data
        data = self.stock_data.get_stock_history(ticker)
        if not data:
            return
            
        # Update header
        self.title_label.config(text=f"{data['name']} ({ticker})")
        
        # Update statistics
        self.price_label.config(text=f"Current Price: ${data['price']:.2f}")
        self.market_cap_label.config(text=f"Market Cap: {self._format_market_cap(data['market_cap'])}")
        self.pe_ratio_label.config(text=f"P/E Ratio: {data['pe_ratio']:.2f}")
        
        # Create and display price history chart
        self._create_price_chart(data['history'])
        
    def _create_price_chart(self, history):
        """Create and display the price history chart."""
        # Clear previous chart if it exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Create figure and plot
        fig = Figure(figsize=(10, 5), dpi=100)  # Larger chart size for better visibility
        fig.patch.set_facecolor('#040F16')
        
        # Add subplot with adjusted margins
        ax = fig.add_subplot(111)
        fig.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9)  # Adjust margins
        
        ax.set_facecolor('#040F16')
        ax.tick_params(colors='white', labelsize=9)  # Adjusted label size
        
        for spine in ax.spines.values():
            spine.set_color('white')
            
        # Plot price history
        ax.plot(history.index, history['Close'], color='#55A76A', linewidth=2)  # Thicker line
        ax.set_title('Price History (1 Year)', color='white', pad=10, fontsize=12)
        ax.grid(True, alpha=0.2)
        
        # Format x-axis
        ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # Limit number of x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')  # Adjusted rotation and alignment
        
        # Add the plot to the frame
        # Create a container frame for the canvas with padding
        canvas_container = tk.Frame(self.chart_frame, bg="#040F16", padx=10, pady=5)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=canvas_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def _on_back_click(self):
        """Callback for Back button - to be set by main app."""
        if hasattr(self, '_on_back_click_callback'):
            self._on_back_click_callback()
            
    def set_back_callback(self, callback):
        """Set the callback function for Back button."""
        self._on_back_click_callback = callback