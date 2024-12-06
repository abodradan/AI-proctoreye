from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import os
from datetime import datetime
from services_v2.embedding_storage import EmbeddingStorage
from services_v2.identity_verifier import IdentityVerifier
from services_v2.embedding_generator import EmbeddingGenerator
from database.database_manager import DatabaseManager
from deepface import DeepFace

from services.image_comparer import ImageComparer  # تأكد من أنك قد أنشأت هذه الخدمة بشكل صحيح
import face_recognition


router = APIRouter()

@router.post("/compare_image_deepface")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    # تهيئة الكلاسات
    embedding_storage = EmbeddingStorage()
    identity_verifier = IdentityVerifier()
    embedding_generator = EmbeddingGenerator()
    try:
        
        db_manager = DatabaseManager()
        db_manager.connect()
        db_manager.create_tables()
        print('captured_image_data dddd')  # تعليق لتتبع البيانات
        student_data = db_manager.student_db.find(Number=registration_number)
        if not student_data:
            db_manager.close()
            return JSONResponse(
                content={"status": "error", "message": "Student not found."},
                status_code=404,
            )
        student = student_data[0]  # بيانات الطالب
        student_college = student[3]  # الكلية
        student_level = student[4]  # المستوى
        student_specialization = student[5]  # التخصص
        
        # التحقق من جدول الامتحانات
        today = datetime.today().strftime("%Y-%m-%d")
        # print('student_specialization',student_specialization)
        # print('student_data',student_data)
        # print('student_level',student_level)
        # print('student_level',type(student_level))
        # print('today',today)
        # print(type(today))

        exam_data = db_manager.exam_db.find(
            Date=today, Specialization=student_specialization, Level=student_level
        )
        # print('exam_data')
        # print(exam_data)
        # print('today',today)
        if not exam_data:
            # العثور على أقرب امتحان
            upcoming_exam = db_manager.exam_db.all(
                Specialization=student_specialization, Level=student_level
            )
            next_exam_date = min([exam[1] for exam in upcoming_exam]) if upcoming_exam else "No upcoming exams"
            db_manager.close()
            print("next_exam_date",next_exam_date)
            return JSONResponse(
                content={
                    "status": "error",
                    "message": f"Today is not the exam date. Next exam is on {next_exam_date}.",
                },
                status_code=403,
            )
        
        # for exam in exam_data:
        #     print(f"Exam found: {exam}")
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        # print('captured_image_data',captured_image_data)  # تعليق لفحص بيانات الصورة
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        # print('captured_image_array',captured_image_array)  # تعليق لفحص الصورة المحوَّلة

        if captured_image_array is None:
            print("db_manager.close()")
            db_manager.close()
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # استرجاع الـ embedding المخزن
        stored_embedding = embedding_storage.get_embedding(registration_number)
        # print('stored_embedding',stored_embedding)
        if not stored_embedding:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "No embedding found for the student.",
                },
                status_code=404,
            )

        
        # حفظ الصورة المؤقتة على القرص لاستخدامها مع DeepFace
        temp_image_path = "temp_captured_image.jpg"
        cv2.imwrite(temp_image_path, captured_image_array)
        if not cv2.imwrite(temp_image_path, captured_image_array):
            raise ValueError("Failed to write captured image to disk.")
        print('asdfasdf')

        captured_embedding = embedding_generator.generate_embedding(temp_image_path)
        # print('captured_embedding',captured_embedding)
        os.remove(temp_image_path)
        
        if not captured_embedding:
            return JSONResponse(
                content={"status": "error", "message": "Failed to generate embedding."},
                status_code=500,
            )
        
        # مقارنة الـ embeddings
        match, similarity = identity_verifier.verify_identity(
            stored_embedding, captured_embedding
        )

        if match:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Student verified successfully.",
                    "similarity": similarity,
                },
                status_code=200,
            )
        else:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Student verification failed.",
                    "similarity": similarity,
                },
                status_code=401,
            )
    except Exception as e:
        db_manager.close()
        return JSONResponse(content={"status": "error", "message": f"Error occurred: {str(e)}"}, status_code=500)
    


@router.post("/compare_image_recognition")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    # تهيئة الكلاسات
    embedding_storage = EmbeddingStorage()
    identity_verifier = IdentityVerifier()
    embedding_generator = EmbeddingGenerator()
    

    try:
        db_manager = DatabaseManager()
        db_manager.connect()
        db_manager.create_tables()
        print("captured_image_data ssdsd")
        # استرجاع بيانات الطالب
        student_data = db_manager.student_db.find(Number=registration_number)
        print("student_data : ", student_data)

        if not student_data:
            db_manager.close()
            return JSONResponse(
                content={"status": "error", "message": "Student not found."},
                status_code=404,
            )
        
        student = student_data[0]  # بيانات الطالب
        student_level = student[4]  # المستوى
        student_specialization = student[5]  # التخصص

        # التحقق من جدول الامتحانات
        today = datetime.today().strftime("%Y-%m-%d")
        exam_data = db_manager.exam_db.find(
            Date=today, Specialization=student_specialization, Level=student_level
        )

        if not exam_data:
            # العثور على أقرب امتحان
            upcoming_exam = db_manager.exam_db.all(
                Specialization=student_specialization, Level=student_level
            )
            next_exam_date = min([exam[1] for exam in upcoming_exam]) if upcoming_exam else "No upcoming exams"
            db_manager.close()
            print('next_exam_date', next_exam_date)
            return JSONResponse(
                content={
                    "status": "error",
                    "message": f"Today is not the exam date. Next exam is on {next_exam_date}.",
                },
                status_code=403,
            )

        # قراءة البيانات الخاصة بالصورة الملتقطة
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        if captured_image_array is None:
            db_manager.close()
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # استرجاع الـ embedding المخزن
        stored_embedding = embedding_storage.get_embedding(registration_number)
        if not stored_embedding:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "No embedding found for the student.",
                },
                status_code=404,
            )

        # توليد embedding للصورة الملتقطة
        captured_image_path = "temp_captured_image.jpg"
        cv2.imwrite(captured_image_path, captured_image_array)
        captured_embedding = embedding_generator.generate_embedding(
            captured_image_path
        )
        os.remove(captured_image_path)  # حذف الصورة المؤقتة

        if not captured_embedding:
            db_manager.close()
            return JSONResponse(
                content={"status": "error", "message": "Failed to generate embedding."},
                status_code=500,
            )

        # مقارنة الـ embeddings باستخدام IdentityVerifier
        match, similarity = identity_verifier.verify_identity(
            stored_embedding, captured_embedding
        )
        if match:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Student verified successfully.",
                    "similarity": similarity,
                },
                status_code=200,
            )
        else:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Student verification failed.",
                    "similarity": similarity,
                },
                status_code=401,
            )

    except Exception as e:
        db_manager.close()
        return JSONResponse(
            content={"status": "error", "message": f"Error occurred: {str(e)}"},
            status_code=500,
        )
