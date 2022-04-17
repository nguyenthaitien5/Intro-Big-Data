

from operator import sub
from tkinter import image_names
import streamlit as st
from deepface import DeepFace
from deepface.basemodels import Facenet
from deepface.basemodels import OpenFace
from deepface.basemodels import FbDeepFace
from deepface.basemodels import VGGFace
import time
import time
import subprocess

from PIL import Image
import os
import shutil
import itertools

from subprocess import Popen, PIPE
import signal
# pro = subprocess.run("hadoop fs -get /data/Five_Faces Five_Facess", shell=True)
# if not os.path.exists("E:\FaceNet\Five_Faces"):
#   os.rename("E:\FaceNet\Five_Facess","E:\FaceNet\Five_Faces")
# os.kill(pro.pid ,  signal.SIGTERM)


def load_image(image_file):
    img = Image.open(image_file)
    return img


...


def FaceNet_Recognition(model_array, model):
    for filename in os.listdir("imageUser/"):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_user = os.path.join('E:\FaceNet\imageUser', filename)
        try:

            return DeepFace.find(img_path=image_user, db_path="E:\\FaceNet\\Five_Faces", model_name=model_array, model=model, detector_backend='mtcnn'), 1

        except:
            return None, -1


def Upload_Predict(model_array, model, image_file, check):
    df, temp = FaceNet_Recognition(model_array, model)

    if temp == -1:
        print("None")
        html_string = "<h3>"+"None"+"</h3>"

        st.markdown(html_string, unsafe_allow_html=True)
        return None
    else:

        temp = df[df.columns[1::]].values.tolist()
        face_identity = []
        for i in range(min(len(df), 2)):

            string_predict = df.iloc[i].identity

            predict_html = string_predict[string_predict.find(
                "Five_Faces"):string_predict.find("/")]

            html_string = "<h3>"+predict_html[11:]+"</h3>"

            st.markdown(html_string, unsafe_allow_html=True)

            if predict_html[11:] not in face_identity:
                face_identity.append(predict_html[11:])

            image = Image.open(string_predict)

            col1, col2 = st.columns(2)
            col1.image(image, use_column_width=True)
            col2.write(temp[i][0])
        return face_identity


def saveImage(name, image, image_name):

    file_path = "Five_Faces/"
    file_path += name
    file_path += "/"
    #name_image = name + "_" + str(len(df)) + ".jpg"
    #str_ = ''.join(file_path)

    with open(os.path.join(file_path, image_name), "wb") as f:

        f.write((image).getbuffer())
    # #  haoop fs -put <localsrc> <dest>
    cmd_path = "hadoop fs -put "
    cmd_path += os.path.join(file_path, image_name)
    cmd_path += " /data/Five_Faces/"
    cmd_path += name
    print(cmd_path)
    subprocess.run(cmd_path, shell=True)
    return


def deletePriviousUser():

    for filename in os.listdir('imageUser'):
        file_path = os.path.join('imageUser', filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def deleteFolder():

    if os.path.exists("E:\FaceNet\Five_Faces"):

        if len(os.listdir("E:\FaceNet\Five_Faces")) == 0:
            os.rmdir("E:\FaceNet\Five_Faces")
        else:
            print("Folder is not empty")
    else:
        print("File not found in the directory")


def main(model_array, model):
    check_save = False
    if st.button("Quit"):

        with st.empty():
            for seconds in range(5):
                st.write(f"⏳ {seconds} seconds ... quit")
                time.sleep(1)
        shutil.rmtree('E:\FaceNet\Five_Faces')

        # quit()
        st.stop()
        st.write("✔️ 1 minute over!")

    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    check = False
    if image_file is None:
        check = False
    if image_file is not None and check_save == False:
        deletePriviousUser()
        check = True
        # To See details
        file_details = {"filename": image_file.name, "filetype": image_file.type,
                        "filesize": image_file.size}
        # st.write(file_details)
        st.image(load_image(image_file), width=250)

        # Saving upload

        with open(os.path.join("imageUser/", image_file.name), "wb") as f:

            f.write((image_file).getbuffer())

        Face_identity = []
        check_identity = 0
        if check == True:
            for i in range(4):
                html_string = "<h3>"+model_array[i]+"</h3>"

                st.markdown(html_string, unsafe_allow_html=True)
                Face_identity.append(Upload_Predict(
                    model_array[i], model[i], image_file, check_save))

            if Face_identity[0] is not None:
                # check_identity = ''
                Face_identity = list(
                    itertools.chain.from_iterable(Face_identity))
                Face_identity = list(set(Face_identity))
                check_save = True

            len_FaceIdentity = len(Face_identity)
            cols = st.columns(len_FaceIdentity)
            if check_save == True:
                for i in range(len_FaceIdentity):
                    name_Save = Face_identity[i]
                    str_save = "Save Image For " + name_Save
                    if cols[i].button(str_save):
                        with st.empty():
                            for seconds in range(6):
                                st.write(f"⏳ {seconds} seconds ... save image")
                                time.sleep(1)
                        saveImage(name_Save, image_file, image_file.name)
                        check_save = False

            print("len")
            print(len_FaceIdentity)
            if Face_identity.count(None) == 4 or len_FaceIdentity > 1:

                with st.form(key='my_form'):
                    text_input = st.text_input(label='Enter some text')
                    submit_button = st.form_submit_button(label='Submit')
                if text_input != "" and submit_button:
                    new_directory = '/data/Five_Faces/'+text_input
                    process = subprocess.call(
                        ['hadoop', 'fs', '-mkdir', new_directory], stdout=PIPE, stderr=PIPE, shell=True)
                    path = os.path.join(
                        'E:\\FaceNet\\Five_Faces\\', text_input)

                    os.mkdir(path)
                    saveImage(text_input, image_file, image_file.name)


st.subheader("Image")


def loadModel():
    model = []
    model.append(Facenet.loadModel())
    model.append(VGGFace.loadModel())
    model.append(OpenFace.loadModel())
    model.append(FbDeepFace.loadModel())
    return model

process = Popen(['hadoop', 'fs', '-get','/data/Five_Faces','Five_Faces'], stdout=PIPE, stderr=PIPE,shell=True)
if os.path.exists("E:\\FaceNet\\Five_Faces"):
 os.kill(process.pid ,  signal.SIGTERM)


models_array = ["Facenet", "VGG-Face",  "OpenFace", "DeepFace"]
model = loadModel()


main(models_array, model)
