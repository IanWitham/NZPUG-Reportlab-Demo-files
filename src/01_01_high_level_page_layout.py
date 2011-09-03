"""High level document layout with PLATYPUS.

The high-level way to create PDFs with Reportlab is to use the PLATYPUS page
layout engine.

To use this PLATYPUS engine, one creates a list of "flowable" objects, which
then "flow" throughout the pages of the PDF document in much the same way as
text and images can flow through the pages of a document in a word processor.
Some of the commonly used flowable classes which are included with PLATYPUS are
Paragraph, Spacer, Table and Image. It is also possible to create your own
flowable types.

PLATYPUS also requires a document template on which to operate, which is in turn
made up of one or more page templates. Fortunately it is not necessary to code
your own templates in order to get started with PLATYPUS, because there is a
very versatile document template available by default called SimpleDocTemplate.
SimpleDocTemplate can infer its own page templates from the arguments supplied
to its constructor.

This file demonstrates the use of SimpleDocTemplate, and three built in flowable
types; Paragraph, Spacer, and Image.
"""
from os.path import join

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# Create a couple of paragraph styles. These affects the font and formatting of
# the paragraph you apply them to.
body_style = ParagraphStyle(name="BodyStyle",
                            fontName="Times-Roman",
                            fontSize=14,
                            leading=17,
                            spaceAfter=20,
                            alignment=TA_JUSTIFY,
                            )
title_style = ParagraphStyle(name="TitleStyle",
                             fontName="Times-Bold",
                             fontSize=26,
                             alignment=TA_CENTER,
                             )

# To make a SimpleDocTemplate, just supply a file name for your PDF, and the
# page margins. You can optionally supply non-flowing elements such as headers
# and footers. I will introduce that feature in a later demonstration.
doc = SimpleDocTemplate("01_02_high_level_page_layout.pdf",
                        leftMargin=40*mm,
                        rightMargin=40*mm,
                        topMargin=40*mm,
                        bottomMargin=40*mm)

story = []  # Fill this list with flowable objects

story.append(Paragraph("The Tell-Tale Heart",
                       title_style
                       )
             )

# A Spacer flowable is fairly obvious. It is used to ensure that an empty space
# of a given size is left in the frame. This spacer leaves a 25mm gap before
# this next paragraph.
story.append(Spacer(1, 25*mm))

story.append(Paragraph("""
    TRUE!&#8212;NERVOUS&#8212;VERY, VERY dreadfully nervous I had been and am;
    but why will you say that I am mad? The disease had sharpened my
    senses&#8211;not destroyed&#8211;not dulled them. Above all was the sense of
    hearing acute. I heard all things in the heaven and in the earth. I heard
    many things in hell. How, then, am I mad? Hearken! and observe how
    healthily&#8211;how calmly I can tell you the whole story.
    """, body_style))

story.append(Paragraph("""
    It is impossible to say how first the idea entered my brain; but once
    conceived, it haunted me day and night. Object there was none. Passion there
    was none. I loved the old man. He had never wronged me. He had never given
    me insult. For his gold I had no desire. I think it was his eye! yes, it was
    this! One of his eyes resembled that of a vulture&#8211;a pale blue eye,
    with a film over it. Whenever it fell upon me, my blood ran cold; and so by
    degrees&#8211;very gradually&#8211;I made up my mind to take the life of the
    old man, and thus rid myself of the eye for ever.
    """, body_style))

story.append(Spacer(1, 15*mm))

# Create an Image flowable. By default Reportlab will place images at 72dpi.
# That is, one pixel is equal to one postscript point, and there are 72
# postscript points to an inch. 72dpi is only suitable for on-screen display, so
# if you want your images to look good in printed form this is probably not what
# you want. You will need to determine a way to calculate the actual height and
# width that you need. For this example we will shrink the image down so that it
# prints at 300dpi (a good printer-friendly resolution). The scale factor
# required to achieve this is 72/300.
orig_width, orig_height = 450, 500
scale_factor = 72 / 300.
new_width = orig_width * scale_factor
new_height = orig_height * scale_factor

story.append(Image(join("images", "025-detail-flaming-heart-q75-450x500.jpg"),
                   width=new_width, height=new_height)
             )

doc.build(story)

print "done"