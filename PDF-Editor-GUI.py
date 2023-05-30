import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os


class PdfEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor")

        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.selected_file = None

        self.create_widgets()

    def create_widgets(self):
        # Merge Files Button
        merge_files_btn = tk.Button(self.root, text="Merge PDF Files", command=self.merge_files)
        merge_files_btn.pack()

        # Split File Button
        split_file_btn = tk.Button(self.root, text="Split PDF File", command=self.split_file)
        split_file_btn.pack()

        # Rotate Pages Button
        rotate_pages_btn = tk.Button(self.root, text="Rotate PDF Pages", command=self.rotate_pages)
        rotate_pages_btn.pack()

        # Extract Text Button
        extract_text_btn = tk.Button(self.root, text="Extract Text", command=self.extract_text)
        extract_text_btn.pack()

        # Watermark PDF Button
        watermark_pdf_btn = tk.Button(self.root, text="Watermark PDF", command=self.watermark_pdf)
        watermark_pdf_btn.pack()

    def merge_files(self):
        merge_file_list = self.pdf_file_list()
        if merge_file_list:
            merged_file_name = self.input_dialog("Merge PDF Files", "Enter the name for the merged file:")
            if merged_file_name:
                self.merge_pdf_files(merge_file_list, merged_file_name)
                self.show_message("Merge PDF Files", "Files merged successfully!")

    def merge_pdf_files(self, file_list, merged_file_name):
        merged_pdf = PyPDF2.PdfFileMerger()
        for file_name in file_list:
            file_path = os.path.join(self.dir, file_name)
            merged_pdf.append(file_path)
        merged_file_path = os.path.join(self.dir, merged_file_name)
        merged_pdf.write(merged_file_path)
        merged_pdf.close()

    def split_file(self):
        file_name = self.select_file()
        if file_name:
            page_ranges = self.input_dialog("Split PDF File", "Enter the page ranges (comma-separated) to split:")
            if page_ranges:
                self.split_pdf_file(file_name, page_ranges)
                self.show_message("Split PDF File", "File split successfully!")

    def split_pdf_file(self, file_name, page_ranges):
        file_path = os.path.join(self.dir, file_name)
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages
            pages_to_split = self.parse_page_ranges(page_ranges, num_pages)
            if pages_to_split:
                file_base_name = os.path.splitext(file_name)[0]
                for i, page_range in enumerate(pages_to_split):
                    output_path = os.path.join(self.dir, f"{file_base_name}_split_{i+1}.pdf")
                    self.extract_pages(file_path, page_range, output_path)

    def parse_page_ranges(self, page_ranges, num_pages):
        page_ranges = page_ranges.strip().split(",")
        pages_to_split = []
        for page_range in page_ranges:
            page_range = page_range.strip()
            if "-" in page_range:
                start, end = page_range.split("-")
                start = int(start.strip())
                end = int(end.strip())
                if start <= end <= num_pages:
                    pages_to_split.append((start, end))
            else:
                page = int(page_range)
                if 1 <= page <= num_pages:
                    pages_to_split.append((page, page))
        return pages_to_split

    def extract_pages(self, file_path, page_range, output_path):
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_writer = PyPDF2.PdfFileWriter()
            for page_num in range(pdf_reader.numPages):
                if self.is_page_in_range(page_num + 1, page_range):
                    page = pdf_reader.getPage(page_num)
                    pdf_writer.addPage(page)
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

    def rotate_pages(self):
        file_name = self.select_file()
        if file_name:
            page_range = self.input_dialog("Rotate PDF Pages", "Enter the page range to rotate:")
            if page_range:
                angle = self.input_dialog("Rotate PDF Pages", "Enter the rotation angle (multiple of 90):")
                if angle and self.angle_check(angle):
                    output_file_name = self.input_dialog("Rotate PDF Pages", "Enter the output file name:")
                    if output_file_name:
                        self.rotate_pdf_pages(file_name, page_range, angle, output_file_name)
                        self.show_message("Rotate PDF Pages", "Pages rotated successfully!")

    def rotate_pdf_pages(self, file_name, page_range, angle, output_file_name):
        file_path = os.path.join(self.dir, file_name)
        output_path = os.path.join(self.dir, output_file_name)
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_writer = PyPDF2.PdfFileWriter()
            for page_num in range(pdf_reader.numPages):
                if self.is_page_in_range(page_num + 1, page_range):
                    page = pdf_reader.getPage(page_num)
                    page.rotateClockwise(int(angle))
                pdf_writer.addPage(page)
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

    def extract_text(self):
        file_name = self.select_file()
        if file_name:
            output_file_name = self.input_dialog("Extract Text", "Enter the output file name:")
            if output_file_name:
                self.extract_pdf_text(file_name, output_file_name)
                self.show_message("Extract Text", "Text extracted successfully!")

    def extract_pdf_text(self, file_name, output_file_name):
        file_path = os.path.join(self.dir, file_name)
        output_path = os.path.join(self.dir, output_file_name)
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)

    def watermark_pdf(self):
        file_name = self.select_file()
        if file_name:
            watermark_type = self.input_dialog("Watermark PDF", "Select watermark type (text/image):")
            if watermark_type:
                if watermark_type.lower() == "text":
                    watermark_text = self.input_dialog("Watermark PDF", "Enter the watermark text:")
                    if watermark_text:
                        output_file_name = self.input_dialog("Watermark PDF", "Enter the output file name:")
                        if output_file_name:
                            self.watermark_pdf_text(file_name, watermark_text, output_file_name)
                            self.show_message("Watermark PDF", "PDF watermarked successfully!")
                elif watermark_type.lower() == "image":
                    watermark_image = self.select_image()
                    if watermark_image:
                        output_file_name = self.input_dialog("Watermark PDF", "Enter the output file name:")
                        if output_file_name:
                            self.watermark_pdf_image(file_name, watermark_image, output_file_name)
                            self.show_message("Watermark PDF", "PDF watermarked successfully!")

    def watermark_pdf_text(self, file_name, watermark_text, output_file_name):
        file_path = os.path.join(self.dir, file_name)
        output_path = os.path.join(self.dir, output_file_name)
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_writer = PyPDF2.PdfFileWriter()
            watermark_page = self.create_watermark_page(watermark_text)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                page.mergePage(watermark_page)
                pdf_writer.addPage(page)
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

    def create_watermark_page(self, watermark_text):
        watermark_pdf = PyPDF2.PdfFileWriter()
        watermark_page = PyPDF2.pdf.PageObject.createBlankPage(None, 100, 100)
        watermark_page.mergeScaledTranslatedPage(watermark_text, 1, 0, 0)
        watermark_pdf.addPage(watermark_page)
        watermark_page_data = watermark_pdf.getPage(0).to_json()
        return PyPDF2.pdf.PageObject.createFromJson(watermark_page_data)

    def watermark_pdf_image(self, file_name, watermark_image, output_file_name):
        file_path = os.path.join(self.dir, file_name)
        output_path = os.path.join(self.dir, output_file_name)
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_writer = PyPDF2.PdfFileWriter()
            watermark_page = self.create_watermark_page_image(watermark_image)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                page.mergePage(watermark_page)
                pdf_writer.addPage(page)
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

    def create_watermark_page_image(self, watermark_image):
        watermark_pdf = PyPDF2.PdfFileReader(watermark_image)
        watermark_page = watermark_pdf.getPage(0)
        watermark_page_data = watermark_page.to_json()
        return PyPDF2.pdf.PageObject.createFromJson(watermark_page_data)

    def pdf_file_list(self):
        file_list = filedialog.askopenfilenames(initialdir=self.dir, title="Select PDF Files",
                                                filetypes=(("PDF files", "*.pdf"),))
        return file_list

    def select_file(self):
        file_path = filedialog.askopenfilename(initialdir=self.dir, title="Select PDF File",
                                               filetypes=(("PDF files", "*.pdf"),))
        if file_path:
            self.selected_file = os.path.basename(file_path)
        return self.selected_file

    def select_image(self):
        image_path = filedialog.askopenfilename(initialdir=self.dir, title="Select Image File",
                                                filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif"),))
        return image_path

    def input_dialog(self, title, message):
        return tk.simpledialog.askstring(title, message, parent=self.root)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def is_page_in_range(self, page_num, page_range):
        for start, end in page_range:
            if start <= page_num <= end:
                return True
        return False

    def angle_check(self, angle):
        try:
            angle = int(angle)
            return angle % 90 == 0
        except ValueError:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = PdfEditorGUI(root)
    root.mainloop()
