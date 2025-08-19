#!/usr/bin/env python3
"""
PDF Upload Utility for EA Chatbot RAG System
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFUploadUtility:
    """Utility for uploading and managing PDFs in the RAG system."""
    
    def __init__(self, pdf_dir: str = "./pdf_documents"):
        """Initialize the PDF upload utility."""
        self.pdf_dir = Path(pdf_dir)
        self.pdf_dir.mkdir(exist_ok=True)
        
        # Supported PDF extensions
        self.supported_extensions = {'.pdf'}
        
        logger.info(f"PDF upload utility initialized. Directory: {self.pdf_dir}")
    
    def upload_pdf(self, source_path: str) -> Dict[str, Any]:
        """
        Upload a PDF file to the RAG system.
        
        Args:
            source_path: Path to the source PDF file
            
        Returns:
            Dictionary with upload status and file info
        """
        source_path = Path(source_path)
        
        if not source_path.exists():
            return {
                "success": False,
                "error": f"Source file not found: {source_path}",
                "file_info": None
            }
        
        if source_path.suffix.lower() not in self.supported_extensions:
            return {
                "success": False,
                "error": f"Unsupported file type: {source_path.suffix}",
                "file_info": None
            }
        
        try:
            # Generate destination filename
            dest_filename = self._generate_unique_filename(source_path.name)
            dest_path = self.pdf_dir / dest_filename
            
            # Copy file to PDF directory
            shutil.copy2(source_path, dest_path)
            
            # Get file information
            file_info = self._get_file_info(dest_path)
            
            logger.info(f"Successfully uploaded PDF: {dest_filename}")
            
            return {
                "success": True,
                "error": None,
                "file_info": file_info
            }
            
        except Exception as e:
            logger.error(f"Error uploading PDF {source_path}: {str(e)}")
            return {
                "success": False,
                "error": f"Upload failed: {str(e)}",
                "file_info": None
            }
    
    def upload_pdfs_from_directory(self, source_dir: str) -> List[Dict[str, Any]]:
        """
        Upload all PDFs from a source directory.
        
        Args:
            source_dir: Path to source directory
            
        Returns:
            List of upload results
        """
        source_dir = Path(source_dir)
        
        if not source_dir.exists() or not source_dir.is_dir():
            return [{
                "success": False,
                "error": f"Source directory not found: {source_dir}",
                "file_info": None
            }]
        
        results = []
        pdf_files = list(source_dir.glob("*.pdf"))
        
        logger.info(f"Found {len(pdf_files)} PDF files in {source_dir}")
        
        for pdf_file in pdf_files:
            result = self.upload_pdf(str(pdf_file))
            results.append(result)
        
        return results
    
    def list_uploaded_pdfs(self) -> List[Dict[str, Any]]:
        """
        List all uploaded PDFs with their information.
        
        Returns:
            List of PDF file information
        """
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        file_info_list = []
        
        for pdf_file in pdf_files:
            file_info = self._get_file_info(pdf_file)
            file_info_list.append(file_info)
        
        return file_info_list
    
    def remove_pdf(self, filename: str) -> Dict[str, Any]:
        """
        Remove a PDF file from the RAG system.
        
        Args:
            filename: Name of the PDF file to remove
            
        Returns:
            Dictionary with removal status
        """
        file_path = self.pdf_dir / filename
        
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {filename}"
            }
        
        try:
            file_path.unlink()
            logger.info(f"Successfully removed PDF: {filename}")
            
            return {
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error removing PDF {filename}: {str(e)}")
            return {
                "success": False,
                "error": f"Removal failed: {str(e)}"
            }
    
    def clear_all_pdfs(self) -> Dict[str, Any]:
        """
        Remove all PDFs from the RAG system.
        
        Returns:
            Dictionary with removal status
        """
        try:
            pdf_files = list(self.pdf_dir.glob("*.pdf"))
            
            for pdf_file in pdf_files:
                pdf_file.unlink()
            
            logger.info(f"Successfully removed {len(pdf_files)} PDF files")
            
            return {
                "success": True,
                "error": None,
                "files_removed": len(pdf_files)
            }
            
        except Exception as e:
            logger.error(f"Error clearing PDFs: {str(e)}")
            return {
                "success": False,
                "error": f"Clear failed: {str(e)}",
                "files_removed": 0
            }
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename to avoid conflicts."""
        base_name = Path(original_filename).stem
        extension = Path(original_filename).suffix
        
        counter = 1
        filename = original_filename
        
        while (self.pdf_dir / filename).exists():
            filename = f"{base_name}_{counter}{extension}"
            counter += 1
        
        return filename
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get information about a PDF file."""
        stat = file_path.stat()
        
        return {
            "filename": file_path.name,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "upload_time": stat.st_mtime,
            "path": str(file_path)
        }
    
    def get_directory_info(self) -> Dict[str, Any]:
        """Get information about the PDF directory."""
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        total_size = sum(f.stat().st_size for f in pdf_files)
        
        return {
            "total_files": len(pdf_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "directory_path": str(self.pdf_dir)
        }


def main():
    """Main function to demonstrate PDF upload utility."""
    print("PDF Upload Utility for EA Chatbot RAG System")
    print("=" * 60)
    
    # Initialize utility
    utility = PDFUploadUtility()
    
    # Show current directory info
    dir_info = utility.get_directory_info()
    print(f"\nCurrent PDF Directory:")
    print(f"Path: {dir_info['directory_path']}")
    print(f"Files: {dir_info['total_files']}")
    print(f"Total Size: {dir_info['total_size_mb']} MB")
    
    # List current PDFs
    current_pdfs = utility.list_uploaded_pdfs()
    if current_pdfs:
        print(f"\nCurrent PDFs:")
        for pdf in current_pdfs:
            print(f"  - {pdf['filename']} ({pdf['size_mb']} MB)")
    else:
        print(f"\nNo PDFs currently uploaded.")
    
    print(f"\nTo add PDFs:")
    print(f"1. Place PDF files in the '{utility.pdf_dir}' directory")
    print(f"2. Run the vector store builder to process them")
    print(f"3. Use the utility methods to manage PDFs programmatically")
    
    print(f"\nUtility methods available:")
    print(f"- upload_pdf(source_path): Upload a single PDF")
    print(f"- upload_pdfs_from_directory(source_dir): Upload all PDFs from a directory")
    print(f"- list_uploaded_pdfs(): List all uploaded PDFs")
    print(f"- remove_pdf(filename): Remove a specific PDF")
    print(f"- clear_all_pdfs(): Remove all PDFs")


if __name__ == "__main__":
    main()
