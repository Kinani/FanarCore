import sys
import dlib
import cv2
import face_recognition
import os
import psycopg2



        

def find_face(imagepath):
    # Create a HOG face detector using the built-in dlib class
    face_detector = dlib.get_frontal_face_detector()
    if not os.path.exists("./.faces"):
        os.mkdir("./.faces")
    connection_db = psycopg2.connect("user='postgres' host='172.21.0.2' dbname='db'")
    db=connection_db.cursor()
    file_name = "."+imagepath
    # print(file_name)
    # Load the image
    image = cv2.imread(file_name)
    # Run the HOG face detector on the image data
    detected_faces = face_detector(image, 1)
    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces):
    # Detected faces are returned as an object with the coordinates
        crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]

        encodings = face_recognition.face_encodings(crop)
        if len(encodings) > 0:
            query = "SELECT file FROM vectors ORDER BY " + \
                    "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) ASC LIMIT 1 ;".format(','.join(str(s) for s in encodings[0][0:63]),','.join(str(s) for s in encodings[0][64:127]),)
            db.execute(query)
            # print("The number of parts: ", db.rowcount)
            row = db.fetchone()

            while row is not None:
                # print(row)
                result = "Found"
                return result
                row = db.fetchone()

            db.close()
            if connection_db is not None:
                connection_db.close()
            

        else:
            result = face_add(file_name)
            if connection_db is not None:
                connection_db.close()
            return result
    
def face_add(imagepath):
    # Create a HOG face detector using the built-in dlib class
    face_detector = dlib.get_frontal_face_detector()
    if not os.path.exists("./.faces"):
        os.mkdir("./.faces")
    connection_db = psycopg2.connect("user='postgres' host='172.21.0.2' dbname='db'")
    db=connection_db.cursor()
    file_name = imagepath
    # Load the image
    image = cv2.imread(file_name)
    # Run the HOG face detector on the image data
    detected_faces = face_detector(image, 1)
    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces):
    # Detected faces are returned as an object with the coordinates
        crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]

        encodings = face_recognition.face_encodings(crop)
        if len(encodings) > 0:
            query = "INSERT INTO vectors (file, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}]))".format(file_name,','.join(str(s) for s in encodings[0][0:63]),','.join(str(s) for s in encodings[0][64:127]),)
            db.execute(query)
            connection_db.commit()
            # print("new face encodings added")
        cv2.imwrite("./.faces/aligned_face_{}_{}_crop.jpg".format(file_name.replace('/', '_'), i), crop)
        
    if connection_db is not None:
        connection_db.close()
    result = "NotFoundAndAdded"
    return result


        

if __name__== "__main__":
    print(sys.argv[1])
    find_face(sys.argv[1])