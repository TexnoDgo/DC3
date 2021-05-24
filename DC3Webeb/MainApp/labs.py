'''import fitz

# Open a PDF file and generate an object
doc = fitz.open('C:/Users/nikita/PycharmProjects/DC3/DC3Webeb/media/temp/МК2.00.15.01.000-03 - Блок лазеров.PDF')

for pg in range(doc.pageCount):
    page = doc[pg]
    rotate = int(0)
    # Each size has a scaling factor of 2, which will give us an image that is quadrupled in resolution.
    zoom_x = 2.0
    zoom_y = 2.0
    trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
    pm = page.getPixmap(matrix=trans, alpha=False)
    pm.writePNG('C:/Users/nikita/PycharmProjects/DC3/DC3Webeb/media/temp/МК2.00.15.01.000-03 - Блок лазеров.PNG')'''
