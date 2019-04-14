import io
import os
import re
import json

# Imports the Google Cloud client library
from google.cloud import vision


cred_path = "C:\\Users\\LUCKY\\PycharmProjects\\ass-2\\praktice-ass-2-8bbc2906c9da.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path


# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'report1.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

# Performs label detection on the image file
response = client.text_detection(image=image)
texts = response.text_annotations

# print('Texts:')


cnt = 0
for text in texts:
    # print('\n"{}"'.format(text.description))

    # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #     for vertex in text.bounding_poly.vertices])
    #
    # print('bounds: {}'.format(','.join(vertices)))
    if cnt==0:
        text_to_search = text.description
    cnt += 1

#print(text_to_search)

name_pattern = re.compile(r'Mr(r|s|rs)\.?\s\w+\s\w+')
age_pattern = re.compile(r'Age:\s\d\d\s\w+')
gender_pattern = re.compile(r'Gender.\s\w+')
ref_pattern = re.compile(r'Ref By:\s\w+')
lab_pattern = re.compile(r'\d\d\d\d\d\d\d\d\d')
hemo_creat_pattern = re.compile(r'\n\d\.\d\d')
report_pattern = re.compile(r'Report Status\s\w+')
matches1 = name_pattern.finditer(text_to_search)
matches2 = age_pattern.finditer(text_to_search)
matches3 = gender_pattern.finditer(text_to_search)
matches4 = ref_pattern.finditer(text_to_search)
matches5 = lab_pattern.finditer(text_to_search)
matches6 = hemo_creat_pattern.finditer(text_to_search)
matches7 = report_pattern.finditer(text_to_search)

final_dict = {}

for match in matches1:
    final_dict['Name'] = text_to_search[match.span()[0]:match.span()[1]]

for match in matches2:
    final_dict['Age'] = text_to_search[match.span()[0]:match.span()[1]][5:7]

for match in matches3:
    final_dict['Gender'] = text_to_search[match.span()[0]:match.span()[1]][8:]

for match in matches4:
    final_dict['Ref By'] = text_to_search[match.span()[0]:match.span()[1]][8:]

for match in matches5:
    final_dict['Lab No'] = text_to_search[match.span()[0]:match.span()[1]]

for i,match in enumerate(matches6):
    # print(match)
    if i==0:
        final_dict['Hemoglobin'] = text_to_search[match.span()[0]:match.span()[1]][1:]
    if i==1:
        final_dict['Creatnine'] = text_to_search[match.span()[0]:match.span()[1]][1:]

for match in matches7:
    final_dict['Report Status'] = text_to_search[match.span()[0]:match.span()[1]][14:]

print(final_dict)