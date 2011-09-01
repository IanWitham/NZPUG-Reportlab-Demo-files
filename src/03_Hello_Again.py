from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# Create a couple of paragraph styles
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

Title = "Hello world"
pageinfo = "platypus example"

doc = SimpleDocTemplate("03_Hello_Again.pdf",
                        leftMargin=40*mm,
                        rightMargin=40*mm,
                        topMargin=40*mm,
                        bottomMargin=40*mm)

story = []  # Fill this list with flowable objects

story.append(Paragraph("The Tell-Tale Heart",
                       title_style
                       )
             )

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

story.append(Paragraph("&#9829;", title_style))


doc.build(story)

