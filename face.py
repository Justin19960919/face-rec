import face_recognition as fr

class Face:

    def __init__(self,input_image):
        # input_image is a path
        self.input_image = fr.load_image_file(input_image)
        self.face_encodings = fr.face_encodings(self.input_image)[0]



