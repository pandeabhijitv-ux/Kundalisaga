"""
Generate PDF documentation from Markdown files
"""
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from pathlib import Path
from html.parser import HTMLParser
import re
import os


class MarkdownToPDFConverter:
    """Convert Markdown to PDF using ReportLab"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#FF6B35'),
                spaceAfter=20,
                spaceBefore=20,
                alignment=TA_CENTER
            ))
        
        # Cover title
        if 'CoverTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CoverTitle',
                parent=self.styles['Heading1'],
                fontSize=32,
                textColor=colors.HexColor('#FF6B35'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        # Heading 2
        if 'Heading2Custom' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Heading2Custom',
                parent=self.styles['Heading2'],
                fontSize=18,
                textColor=colors.HexColor('#2C3E50'),
                spaceBefore=15,
                spaceAfter=10,
                borderWidth=1,
                borderColor=colors.HexColor('#3498DB'),
                borderPadding=5
            ))
        
        # Heading 3
        if 'Heading3Custom' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Heading3Custom',
                parent=self.styles['Heading3'],
                fontSize=14,
                textColor=colors.HexColor('#34495E'),
                spaceBefore=12,
                spaceAfter=8
            ))
        
        # Code style - use a different name to avoid conflict
        if 'CodeBlock' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CodeBlock',
                parent=self.styles['Normal'],
                fontSize=8,
                leftIndent=20,
                rightIndent=20,
                spaceBefore=10,
                spaceAfter=10,
                backColor=colors.HexColor('#f8f9fa'),
                borderColor=colors.HexColor('#ddd'),
                borderWidth=1,
                borderPadding=10,
                fontName='Courier'
            ))
    
    def parse_markdown_to_flowables(self, md_text):
        """Parse markdown text and convert to ReportLab flowables"""
        flowables = []
        lines = md_text.split('\n')
        
        i = 0
        in_code_block = False
        code_block = []
        in_table = False
        table_lines = []
        
        while i < len(lines):
            line = lines[i]
            
            # Code blocks
            if line.startswith('```'):
                if in_code_block:
                    # End of code block
                    code_text = '\n'.join(code_block)
                    flowables.append(Preformatted(code_text, self.styles['CodeBlock']))
                    flowables.append(Spacer(1, 0.2*inch))
                    code_block = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                i += 1
                continue
            
            if in_code_block:
                code_block.append(line)
                i += 1
                continue
            
            # Tables
            if '|' in line and not line.strip().startswith('#'):
                if not in_table:
                    in_table = True
                    table_lines = []
                table_lines.append(line)
                i += 1
                # Check if next line is still part of table
                if i < len(lines) and '|' not in lines[i]:
                    # End of table
                    table = self._create_table(table_lines)
                    if table:
                        flowables.append(table)
                        flowables.append(Spacer(1, 0.2*inch))
                    in_table = False
                    table_lines = []
                continue
            
            if not line.strip():
                flowables.append(Spacer(1, 0.1*inch))
                i += 1
                continue
            
            # Headers
            if line.startswith('# '):
                text = line[2:].strip()
                text = self._clean_markdown(text)
                flowables.append(PageBreak())
                flowables.append(Paragraph(text, self.styles['CustomTitle']))
                flowables.append(Spacer(1, 0.2*inch))
            elif line.startswith('## '):
                text = line[3:].strip()
                text = self._clean_markdown(text)
                flowables.append(Paragraph(text, self.styles['Heading2Custom']))
                flowables.append(Spacer(1, 0.15*inch))
            elif line.startswith('### '):
                text = line[4:].strip()
                text = self._clean_markdown(text)
                flowables.append(Paragraph(text, self.styles['Heading3Custom']))
                flowables.append(Spacer(1, 0.1*inch))
            elif line.startswith('#### '):
                text = line[5:].strip()
                text = self._clean_markdown(text)
                flowables.append(Paragraph(text, self.styles['Heading4']))
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                text = self._clean_markdown(text)
                flowables.append(Paragraph(f'• {text}', self.styles['Normal']))
            elif re.match(r'^\d+\. ', line):
                text = re.sub(r'^\d+\. ', '', line).strip()
                text = self._clean_markdown(text)
                flowables.append(Paragraph(f'• {text}', self.styles['Normal']))
            # Inline code
            elif '`' in line:
                text = self._clean_markdown(line)
                text = text.replace('`', '<font face="Courier" color="#c7254e">')
                text = text.replace('`', '</font>')
                flowables.append(Paragraph(text, self.styles['Normal']))
            # Regular paragraph
            else:
                text = self._clean_markdown(line)
                if text:
                    flowables.append(Paragraph(text, self.styles['Normal']))
            
            i += 1
        
        return flowables
    
    def _clean_markdown(self, text):
        """Clean markdown syntax from text"""
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Inline code
        text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#c7254e">\1</font>', text)
        # Links [text](url) - just show text
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        # Remove emojis and special unicode
        text = re.sub(r'[🌟📋🖥️🚀🛑📊🔧💾🔄📞⚙️🔐📈📝📚🎯💰🔍🗄️💡✅❌⚠️🔴🟡🟢💳📁📄💎➕🔄🆕✨🌙☀️🔮📈💰🎨🎓⭐💼📊🏢🏭🏗️🚗⛏️🏨🏃‍♂️🕉️]', '', text)
        return text.strip()
    
    def _create_table(self, table_lines):
        """Create a table from markdown table lines"""
        if not table_lines:
            return None
        
        # Parse table
        rows = []
        for line in table_lines:
            if '---' in line or '===' in line:
                continue
            cells = [cell.strip() for cell in line.split('|')]
            cells = [c for c in cells if c]  # Remove empty cells
            if cells:
                rows.append(cells)
        
        if not rows:
            return None
        
        # Create table
        table = Table(rows)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        return table


def markdown_to_pdf(markdown_file: str, pdf_file: str, title: str = ""):
    """Convert a markdown file to PDF"""
    
    print(f"Converting {markdown_file} to PDF...")
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Create converter
    converter = MarkdownToPDFConverter()
    
    # Build story
    story = []
    
    # Cover page
    styles = converter.styles
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(title, styles['CoverTitle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('AstroKnowledge', styles['Heading2']))
    story.append(Paragraph('Vedic Astrology AI Assistant', styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph('Version 1.0.0 | December 2025', styles['Normal']))
    story.append(PageBreak())
    
    # Content
    flowables = converter.parse_markdown_to_flowables(md_content)
    story.extend(flowables)
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created: {pdf_file}")



def main():
    """Generate all documentation PDFs"""
    
    print("=" * 60)
    print("  AstroKnowledge Documentation PDF Generator")
    print("=" * 60)
    print()
    
    # Check if required packages are installed
    try:
        from reportlab.lib.pagesizes import A4
    except ImportError as e:
        print(f"❌ Error: Missing required package - {e}")
        print()
        print("Please install required packages:")
        print("  pip install reportlab")
        return
    
    # Define documents to convert
    documents = [
        {
            'markdown': 'OPERATIONS_GUIDE.md',
            'pdf': 'AstroKnowledge_Operations_Guide.pdf',
            'title': 'Operations Guide'
        },
        {
            'markdown': 'CONFIGURATION_GUIDE.md',
            'pdf': 'AstroKnowledge_Configuration_Guide.pdf',
            'title': 'Configuration Guide'
        }
    ]
    
    # Create PDFs directory if it doesn't exist
    pdf_dir = Path('docs_pdf')
    pdf_dir.mkdir(exist_ok=True)
    
    # Convert each document
    success_count = 0
    for doc in documents:
        markdown_file = doc['markdown']
        pdf_file = pdf_dir / doc['pdf']
        title = doc['title']
        
        if not Path(markdown_file).exists():
            print(f"⚠️  Warning: {markdown_file} not found, skipping...")
            continue
        
        try:
            markdown_to_pdf(markdown_file, str(pdf_file), title)
            success_count += 1
        except Exception as e:
            print(f"❌ Error converting {markdown_file}: {e}")
    
    print()
    print("=" * 60)
    print(f"✅ Successfully generated {success_count} PDF document(s)")
    print(f"📁 PDFs saved in: {pdf_dir.absolute()}")
    print("=" * 60)
    
    # List generated PDFs
    if success_count > 0:
        print("\nGenerated files:")
        for pdf_file in pdf_dir.glob('*.pdf'):
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"  • {pdf_file.name} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
