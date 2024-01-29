import dlib
import numpy as np
from PIL import Image
import gradio as gr
import cv2


def ten_rengi_analiz(image):
    # Giriş resmini uygun bir şekilde işleyin (örneğin, boyutu değiştirin, HSV renk uzayına dönüştürün)
    resized_image = cv2.resize(image, (100, 100))
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

    # Cilt rengini tanımlayın (örneğin, buğday rengi bir cilt için)
    cilt_rengi_alt = np.array([0, 20, 70], dtype=np.uint8)
    cilt_rengi_ust = np.array([20, 255, 255], dtype=np.uint8)

    # Cilt rengini maskeleme
    cilt_maske = cv2.inRange(hsv_image, cilt_rengi_alt, cilt_rengi_ust)

    # Cilt rengi bölgesinin yoğunluğunu hesaplayın
    cilt_yogunlugu = np.mean(cilt_maske) / 255.0  # Normalleştirilmiş değer

    # Eşik değeri belirleyin (buğday ten rengi için bir örnek)
    ten_rengi_esik_degeri = 0.6

    # Ten rengini değerlendirin
    if cilt_yogunlugu < ten_rengi_esik_degeri:
        return True
    else:
        return False

# Göz altı durumunu analiz etmek için fonksiyon
def goz_alti_analiz(image):
    # Giriş resmini uygun bir şekilde işleyin (örneğin, boyutu değiştirin, renk uzayını dönüştürün)
    resized_image = cv2.resize(image, (100, 100))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Göz altı rengi için eşik değeri belirleyin (örneğin, koyu göz altı için bir örnek)
    goz_alti_esik_degeri = 50  # Belirli bir eşik değeri

    # Göz altı rengini değerlendirin
    goz_alti_yogunlugu = np.mean(gray_image)  # Yoğunluk değeri
    if goz_alti_yogunlugu < goz_alti_esik_degeri:
        return False
    else:
        return True

def detect_landmarks(image):
    predictor_path = 'C:/Users/u30l35/Desktop/pythonProject4/dlib-models/shape_predictor_68_face_landmarks.dat'

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    image = np.array(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_image, 1)

    for face in faces:
        landmarks = predictor(gray_image, face)
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (255, 0, 0), -1)

    if len(faces) > 0:
        # Bu örnek için, yüzün genişliğini temel alıyoruz
        ten_rengi_cok_koyu_ve_soluk = ten_rengi_analiz(image)
        goz_altlari_cok_koyu = goz_alti_analiz(image)
        face_width = faces[0].right() - faces[0].left()

        if face_width > 140:  # Örnek bir eşik değeri
            prediction = "Zengin"

        else:
            # Ten rengi ve göz altı analizlerini kullanarak "fakir" tahmini yap



            prediction = "Fakir"


        # Tahmini bir metin dosyasına yaz
        # Tahmini bir metin dosyasına yaz
        with open("C:/Users/u30l35/Desktop/pythonProject4/prediction.txt", "w", encoding='utf-8') as file:
            file.write(prediction)

        return image, prediction
    else:
        return image

iface = gr.Interface(fn=detect_landmarks,
                     inputs=gr.Image(),
                     outputs=["image", "text"],
                     title="Rich/Poor Facial Detection",
                     description="Upload an image to detect facial landmarks and get a socioeconomic status prediction.")

if __name__ == "__main__":
    iface.launch()
