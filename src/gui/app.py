import tkinter as tk
from tkinter import messagebox
from typing import Tuple, List, Optional


from ..sentiment_analyzer.main import main as analyze_sentiment
from .loading_frame import LoadingFrame
from .results_frame import ResultsFrame

class StockSentimentApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Sentiment Analyzer")
        self.root.geometry("600x450")  # Increased height for better text display
        self.root.resizable(False, False)
        self.root.configure(bg="#040F16")  # Set dark navy background
        
        # Initialize frames
        self.loading_frame = LoadingFrame(self.root)
        self.results_frame = ResultsFrame(self.root)
        
        # Set callback for Analyze Again button
        print("Setting up Analyze Again callback")  # Debug print
        self.results_frame.set_analyze_callback(self.start_analysis)
        print("Callback set")  # Debug print
        
        # Start with loading frame
        self.show_loading_frame()
        
    def show_loading_frame(self):
        """Display the loading frame."""
        print("Switching to loading frame")  # Debug print
        self.results_frame.pack_forget()
        self.loading_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.loading_frame.reset()
        
    def show_results_frame(self):
        """Display the results frame."""
        print("Switching to results frame")  # Debug print
        self.loading_frame.pack_forget()
        self.results_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
    def handle_progress(self, update_data: dict):
        """Handle progress updates from the sentiment analysis."""
        if 'progress' in update_data and 'message' in update_data:
            # Clean up the message string
            message = str(update_data['message']).strip()
            self.loading_frame.update_progress(
                update_data['progress'],
                message
            )
            
    def start_analysis(self):
        """Start the sentiment analysis process."""
        print("Starting new analysis")  # Debug print
        self.show_loading_frame()
        print("Showed loading frame")  # Debug print
        self.root.update()
        
        try:
            print("Running sentiment analysis")  # Debug print
            # Run sentiment analysis with progress callback
            bullish, bearish = analyze_sentiment(progress_callback=self.handle_progress)
            
            print(f"Analysis complete. Bullish: {bullish}, Bearish: {bearish}")  # Debug print
            # Update results display
            self.results_frame.display_results(bullish, bearish)
            print("Updated results")  # Debug print
            self.show_results_frame()
            print("Showed results frame")  # Debug print
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")  # Debug print
            # Show error message
            tk.messagebox.showerror(
                "Error",
                f"An error occurred during analysis:\n{str(e)}"
            )
            self.show_results_frame()
            
    def run(self):
        """Start the application."""
        # Start initial analysis
        self.root.after(100, self.start_analysis)
        # Start main loop
        self.root.mainloop()

def main():
    app = StockSentimentApp()
    app.run()

if __name__ == "__main__":
    main()