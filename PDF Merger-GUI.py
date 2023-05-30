import tkinter as tk
from tkinter import filedialog
import PyPDF2

class PDFMergerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        
        self.pdf_files = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # PDF Selection Button
        self.select_button = tk.Button(self, text="Select PDFs", command=self.select_pdfs)
        self.select_button.pack(pady=10)
        
        # Merge Button
        self.merge_button = tk.Button(self, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=10)
    
    def select_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.pdf_files = list(files)
    
    def merge_pdfs(self):
        if not self.pdf_files:
            self.show_message("Error", "No PDF files selected.")
            return
        
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not output_path:
            return
        
        merger = PyPDF2.PdfMerger()
        
        try:
            for pdf_file in self.pdf_files:
                merger.append(pdf_file)
            
            merger.write(output_path)
            
            self.show_message("Merge Complete", "PDF files merged successfully.")
        
        except PyPDF2.PdfReadError:
            self.show_message("Merge Failed", "Failed to merge PDF files.")
        
        finally:
            merger.close()
    
    def show_message(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        
        label = tk.Label(popup, text=message)
        label.pack(padx=10, pady=10)
        
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)

if __name__ == "__main__":
    app = PDFMergerGUI()
    app.mainloop()
