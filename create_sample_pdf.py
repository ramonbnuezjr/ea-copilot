#!/usr/bin/env python3
"""
Create a sample PDF document for testing PDF integration
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from pathlib import Path

def create_sample_pdf():
    """Create a sample PDF document for testing."""
    
    # Create output directory if it doesn't exist
    pdf_dir = Path("pdf_documents")
    pdf_dir.mkdir(exist_ok=True)
    
    # Output file path
    output_file = pdf_dir / "sample_ea_framework.pdf"
    
    # Create the PDF document
    doc = SimpleDocTemplate(str(output_file), pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=14
    )
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("Enterprise Architecture Framework", title_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(
        "This document outlines our comprehensive Enterprise Architecture framework "
        "designed to align technology with business objectives while ensuring "
        "scalability, security, and operational excellence.", body_style
    ))
    story.append(Spacer(1, 15))
    
    # Core Principles
    story.append(Paragraph("Core Principles", heading_style))
    principles = [
        "Business Alignment: All technology decisions must directly support business capabilities and strategic objectives.",
        "Standardization First: Prefer standard, widely-adopted technologies over custom solutions.",
        "Security by Design: Security and compliance requirements must be integrated into all architecture decisions.",
        "Data as an Asset: Treat data as a strategic enterprise asset with proper governance.",
        "Agility and Flexibility: Architectures should support rapid change while maintaining stability."
    ]
    
    for principle in principles:
        story.append(Paragraph(f"• {principle}", body_style))
    
    story.append(Spacer(1, 15))
    
    # Technology Standards
    story.append(Paragraph("Technology Standards", heading_style))
    story.append(Paragraph(
        "Our technology stack is organized into three tiers:", body_style
    ))
    
    tiers = [
        ("Foundation Layer", [
            "Cloud Infrastructure: AWS/Azure with multi-region deployment",
            "Containerization: Kubernetes for orchestration, Docker for packaging",
            "Monitoring: Prometheus, Grafana, and ELK stack for observability"
        ]),
        ("Application Layer", [
            "Frontend: React.js with TypeScript for web applications",
            "Backend: Node.js/Express or Python/FastAPI for APIs",
            "Database: PostgreSQL for relational data, Redis for caching"
        ]),
        ("Integration Layer", [
            "API Gateway: Kong or AWS API Gateway",
            "Service Mesh: Istio for microservices communication",
            "CI/CD: GitHub Actions with automated testing and deployment"
        ])
    ]
    
    for tier_name, technologies in tiers:
        story.append(Paragraph(f"<b>{tier_name}:</b>", body_style))
        for tech in technologies:
            story.append(Paragraph(f"  • {tech}", body_style))
        story.append(Spacer(1, 10))
    
    # Risk Management
    story.append(Paragraph("Risk Management", heading_style))
    story.append(Paragraph(
        "Technical debt is managed through a systematic approach:", body_style
    ))
    
    story.append(Paragraph("<b>Assessment Criteria:</b>", body_style))
    criteria = [
        "Business Impact: High, Medium, Low",
        "Technical Risk: Security, Performance, Maintainability",
        "Effort Required: Small, Medium, Large"
    ]
    
    for criterion in criteria:
        story.append(Paragraph(f"• {criterion}", body_style))
    
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Prioritization Matrix:</b>", body_style))
    priorities = [
        "P1 (Critical): Security vulnerabilities, compliance issues",
        "P2 (High): Performance bottlenecks, scalability concerns",
        "P3 (Medium): Code quality, documentation gaps",
        "P4 (Low): Nice-to-have improvements"
    ]
    
    for priority in priorities:
        story.append(Paragraph(f"• {priority}", body_style))
    
    # Build the PDF
    doc.build(story)
    
    print(f"✅ Sample PDF created successfully: {output_file}")
    print(f"📄 File size: {output_file.stat().st_size / 1024:.1f} KB")
    
    return output_file

if __name__ == "__main__":
    try:
        pdf_file = create_sample_pdf()
        print(f"\n🎯 Next steps:")
        print(f"1. The PDF is now in: {pdf_file}")
        print(f"2. Run: python3 demo_pdf_integration.py")
        print(f"3. The system will automatically process the PDF")
        print(f"4. Your RAG system will include PDF content!")
        
    except Exception as e:
        print(f"❌ Error creating PDF: {str(e)}")
        print("Make sure you have reportlab installed: pip3 install reportlab")
