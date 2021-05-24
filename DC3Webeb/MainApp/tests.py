from django.test import TestCase

# Create your tests here.
import zipfile
import os
from os.path import basename

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

archive_file_path = os.path.join(BASE_DIR, 'media/temp/') + 'test_archive.zip'
file1_path = 'C:/Users/nikita/PycharmProjects/DC3/DC3Webeb/media/PDF_DRAW_WT_QR_CODE/3V8ICf797cLlS.PDF'
file2_path = 'C:/Users/nikita/PycharmProjects/DC3/DC3Webeb/media/PDF_DRAW_WT_QR_CODE/AIhAuJ1M2GCvl.PDF'

z = zipfile.ZipFile(archive_file_path, 'w')
z.write(file1_path, basename(file1_path))
z.write(file2_path, basename(file2_path))
z.close()
