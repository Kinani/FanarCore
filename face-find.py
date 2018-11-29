import sys
import dlib
import cv2
import face_recognition
import os
import psycopg2

if len(sys.argv) < 2:
    print("Usage: face-find <image>")
    exit(1)

found = False
# Take the image file name from the command line
file_name = sys.argv[1]

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()

# Load the image
image = cv2.imread(file_name)

# Run the HOG face detector on the image data
detected_faces = face_detector(image, 1)

# print("Found {} faces in the image file {}".format(len(detected_faces), file_name))

if not os.path.exists("./.faces"):
    os.mkdir("./.faces")


connection_db = psycopg2.connect("user='postgres' host='172.21.0.2' dbname='db'")
db=connection_db.cursor()

# Loop through each face we found in the image
for i, face_rect in enumerate(detected_faces):
    # Detected faces are returned as an object with the coordinates
    # of the top, left, right and bottom edges
    # print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(),
                                                                            #  face_rect.right(), face_rect.bottom()))
    crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]

    encodings = face_recognition.face_encodings(crop)
    threshold = 0.6
    if len(encodings) > 0:
        query = "SELECT file FROM vectors WHERE sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) <= {} ".format(
            ','.join(str(s) for s in encodings[0][0:64]),
            ','.join(str(s) for s in encodings[0][64:128]),
            threshold)
        # print(query)
        db.execute(query)
        # print("The number of parts: ", db.rowcount)
        row = db.fetchone()

        # While
        if row is not None:
            # print(row)
            print("Found encodings")
            row = db.fetchone()
          
        found = True
        db.close()
    else:
        print("No encodings")

if found == False:
        print("No face detected")

if connection_db is not None:
    connection_db.close()