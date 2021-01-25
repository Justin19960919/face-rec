# https://pypi.org/project/face-recognition/
# https://github.com/ageitgey/face_recognition/blob/master/examples/identify_and_draw_boxes_on_faces.py
# https://www.datacamp.com/community/tutorials/face-detection-python-opencv
# Pillow: https://pillow.readthedocs.io/en/stable/


# dependencies
'''
face_recognition
cmake
dlib==19.18
wheel
Pillow # image library

flask # later

'''
# maybe somehow modularize the code a little


import face_recognition as fr       # face recognition
from face import Face               # Face class
from PIL import Image, ImageDraw    # image process
import numpy as np
import os



def label_image(unknown_image_path):

    #### known faces (This we can do before hand)
    #  Create arrays of encodings and names
    known_path = "./known/"
    known_faces = os.listdir("./known")

    known_face_names = []
    known_face_encodings = []

    for face in known_faces:
        if face.endswith(".jpg") or face.endswith(".png"):
            name = face.split(".")[0]
            cur_face = Face(os.path.join(known_path,face))
            known_face_names.append(name)
            known_face_encodings.append(cur_face.face_encodings)


    ## unknown image
    # unknown_image_path = "./unknown/twice_2.jpg"

    test_image = fr.load_image_file(unknown_image_path)


    # Find faces in test image (find faces.py)
    face_locations = fr.face_locations(test_image)
    face_encodings = fr.face_encodings(test_image, face_locations)


    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(test_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    # pil_image.show()

    # You can also save a copy of the new image to disk if you want by uncommenting this line
    pil_image.save(f"./static/results/results.jpg")
