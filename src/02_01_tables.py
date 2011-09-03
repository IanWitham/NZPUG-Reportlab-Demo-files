"""Table flowables with PLATYPUS.

Dynamic pdf generation is often about presenting data in one form or another, which
is why the Table flowable is so useful.

A table consist of:

<bullet>&bull;</bullet>Data, supplied as a list of lists.

<bullet>&bull;</bullet>A TableStyle object.
"""
from os.path import join
import csv

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# a handy function which helps to blend smoothly between two colors, but
# unfortunately it has a very long name.
lerp = colors.linearlyInterpolatedColor

title_style = ParagraphStyle(name="TitleStyle",
                             fontName="Times-Bold",
                             fontSize=26,
                             alignment=TA_CENTER,
                             )

# To make a SimpleDocTemplate, just supply a file name for your PDF, and the
# page margins. You can optionally supply non-flowing elements such as headers
# and footers. I will introduce that feature in a later demonstration.
doc = SimpleDocTemplate("02_03_tables.pdf",
                        leftMargin=20*mm,
                        rightMargin=20*mm,
                        topMargin=20*mm,
                        bottomMargin=20*mm)

story = []  # Fill this list with flowable objects

story.append(Paragraph("Kiwi PyCon 2011 Network Traffic",
                       title_style
                       )
             )

# A Spacer flowable is fairly obvious. It is used to ensure that an empty space
# of a given size is left in the frame. This spacer leaves a 25mm gap before
# this next paragraph.
story.append(Spacer(1, 15*mm))

# Prepare the table data as a list of lists, including a header row.
datafile = csv.reader(open("02_02_kiwipycon_wifi_details.csv"))
table_data = list(datafile)

# Prepare the TableStyle.
myTableStyle = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.green),
                           ('LINEABOVE', (0,2), (-1,-1), 0.25, colors.black),
                           ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
                           ('LINEABOVE', (0,1), (-1,1), 2, colors.green),
                           ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
                          )

# add some conditional formatting to the table style
for i, data in enumerate(table_data):
    if not i:
        continue  # skip header row
    for col in range(1,3):
        mb = int(data[col]) # megabytes uploaded or downloaded
        # color each cell from white at 0MB to a maximum of full red at 1000MB
        myTableStyle.add('BACKGROUND', (col, i), (col, i),
                         lerp(colors.white, colors.red, 0, 1000, min(mb, 1000)))

# The table flowables. A couple of points to note:
#  - repeatRows=1 means that 1 row (the header) will repeat at the top of each
#    page that the table flows on to.
#  - colWidths needs to be defined manually if you want the table to span the
#    entire width of the frame.
myTable = Table(table_data, repeatRows=1,
                colWidths=[170/3.*mm]*3, style=myTableStyle)

story.append(myTable)

story.append(Spacer(1, 15*mm))

doc.build(story)

print "done"