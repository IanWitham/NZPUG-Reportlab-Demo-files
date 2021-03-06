"""Automatically document a Reportlab presentation!

This is a special example which ties together several concepts to create
presentation notes. It knows how to loop over the files in this folder and can
render both Python source code and PDF files. Additionally the first doc string
in each Python source code is converted to a series of Paragraph objects in the
interests of nice presentation.

The PDFRW library is used to render PDFs, and a custom flowable is employed to
add the PDF to the story stream.
"""
import os
from os.path import join

from reportlab.platypus.xpreformatted import PythonPreformatted, XPreformatted
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Image, Spacer
from reportlab.platypus import Flowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import ParagraphStyle as PS

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

pageinfo = "Introduction to Reportlab"

class PdfFlowable(Flowable):
    """A custom flowable which draws the first page of a pdf file
    into the frame at 75% scale"""
    def __init__(self, pdf_filename, spaceBefore=12, spaceAfter=12):
        self.spaceBefore = spaceBefore
        self.spaceAfter = spaceAfter
        
        # Read the pdf file data
        pdf_page = PdfReader(pdf_filename, decompress=False).pages[0]
        
        # Convert each page to a pagexobject. This is a special kind of
        # self contained pdf object that can be reused in other pdf files.
        self.xobj = pagexobj(pdf_page)
    
        x, y, width, height = self.xobj.BBox
        self.width = float(width)
        self.height = float(height)

    def wrap(self, *args):
        # returns the height of the object
        return (0, float(self.height)*0.75 + self.spaceBefore + self.spaceAfter)
    
    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(0, self.spaceBefore)
        c.scale(0.75, 0.75)
        # draw a grey shadow under the page
        c.saveState()
        c.translate(10, -10)
        c.setFillColorCMYK(0, 0, 0, 0.2)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.restoreState()
        # draw a white background for the pdf to sit on
        c.saveState()
        c.setFillColorCMYK(0, 0, 0, 0)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.restoreState()
        # draw the pdf page
        c.doForm(makerl(c, self.xobj))
        # draw a black outline around the pdf page
        c.rect(0, 0, self.width, self.height, stroke=1, fill=0)
        c.restoreState()

def myFirstPage(canvas, doc):
    # draws the static elements of the first page
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.5 * inch, "First Page / %s" % pageinfo)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    # draws the static elements of all subsequent pages
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.5 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

base_pre_style = PS('pre',
                fontName="Courier",
                fontSize=9,
                leading=9,
                borderPadding=6,
                spaceBefore=12,
                spaceAfter=12,
                )

code_style = PS('code',
                parent=base_pre_style,
                backColor=colors.whitesmoke,
                )

plain_style = PS('plaintext',
                 parent=base_pre_style,
                 backColor=colors.lightgreen,
                 )

title_style = styles["Heading1"]

def pythonCode(text):
    text = open(text).readlines()
    # A rather naive way to extract to first docstring. Oh well.
    try:
        description = ''.join(text[:text.index('"""\n')])[3:]
        code = text[text.index('"""\n')+1:]
    except ValueError:
        description = None
        code = text
    
    returnVal = []
    
    # First handle the description text (if any)
    if description:
        returnVal.extend(storify(description))
    
    # Then handle the Python source code
    if ''.join(code).strip():
        returnVal.append(PythonPreformatted(''.join(code), code_style))
    
    return returnVal

def storify(text):
        """This function converts a string of text into a list of paragraphs. Each
        paragraph should be separated by 2 newlines. The first paragraph will be
        treated as a heading."""
        textBlocks = text.split("\n\n")
        storyList = [Paragraph(textBlocks[0], styles["Heading2"])]
        storyList += [Paragraph(t, styles["BodyText"]) for t in textBlocks[1:]]
        return storyList
    
def plainText(text):
    text = open(text).read()
    # Snip long text files down to the first 30 lines
    text_lines = text.splitlines()
    if len(text_lines) > 30:
        text_lines = text_lines[:30]
        text_lines.append("-"*37 + " SNIP " + "-"*37)
        text = '\n'.join(text_lines)
    return [XPreformatted(text, plain_style)]

def pdfPage(file_data):
    # handler for pdf files
    return [PdfFlowable(file_data)]

def go():
    doc = SimpleDocTemplate("99_Self_Document.pdf",
                            bottomMargin=20*mm)
    Story = []
    
    Story.append(Paragraph("Introduction to Reportlab", styles["Heading1"]))
    Story.append(Paragraph("Ian Witham, September 2011", styles["Heading2"]))
    Story.append(Paragraph("""Source available from
    <a href="http://github.com/IanWitham/NZPUG-Reportlab-Demo-files/">
    http://github.com/IanWitham/NZPUG-Reportlab-Demo-files/</a>""",
    styles["Heading3"]))
    Story.append(Spacer(1, 30*mm))
    width = 1039 * (72./200)
    height = 1167 * (72./200)
    Story.append(Image(join("images", "0493-Printing-Press-q75-1039x1167.jpg"),
                       width=width, height=height, ))
    
    Story.append(PageBreak())
    
    files = sorted(os.listdir('.'))
    
    handlers = {"py":pythonCode,
                "txt":plainText,
                "csv":plainText,
                "pdf":pdfPage,
                }
    
    for file_name in files:
        if file_name in ("99_Self_Document.pdf", "pdfrw"):
            continue
        print file_name
        file_extension = file_name.split(".")[-1]
        if file_extension in handlers:
            if file_extension == "pdf":
                Story.append(PageBreak())
            heading = Paragraph(file_name, title_style)
            # get a list of new flowables
            file_contents = handlers[file_extension](file_name)
            # add the new flowables to the story
            Story.extend([heading] + file_contents)
    
    # invoke the PLATYPUS engine.
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

go()