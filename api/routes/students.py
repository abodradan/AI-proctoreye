import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2
import numpy as np
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services.student_data_handler import StudentDataHandler
from database.database_manager import DatabaseManager
from services_v2.embedding_generator import EmbeddingGenerator
from services_v2.embedding_storage import EmbeddingStorage


router = APIRouter()

# تهيئة الكلاسات
embedding_generator = EmbeddingGenerator()
embedding_storage = EmbeddingStorage()
student_data_handler = StudentDataHandler() # 


@router.post("/add_student")
async def add_student(
    name: str = Form(...),
    number: str = Form(...),
    college: str = Form(...),
    level: str = Form(...),
    specialization: str = Form(...),
    image_file: UploadFile = File(...)
    ):
    try:
        print(f"Received data: name={name}, number={number}, image_array={image_file.filename}")
        
        # قراءة البيانات من الملف وتحويلها إلى numpy array
        image_data = np.frombuffer(await image_file.read(), np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file. Unable to process the uploaded file.")

        # حفظ الصورة في مجلد images
        image_extension = os.path.splitext(image_file.filename)[1]
        image_path = f"images/{number}{image_extension}"
        cv2.imwrite(image_path, image)

        # إنشاء التمثيل المدمج (Embedding)
        embedding = embedding_generator.generate_embedding(image_path)
        
        if embedding is None:
            raise HTTPException(status_code=400, detail="Failed to generate embedding for the uploaded image.")
        
        # حفظ الـ Embedding في ملف JSON
        embedding_storage.save_embedding(number, embedding)

        # إنشاء بيانات الطالب
        student_data = {
            'number': number,
            'StudentName': name,
            'College': college,
            'Level': level,
            'Specialization': specialization,
            'ImagePath': image_path,
        }
        

        # التحقق من وجود الرقم المسجل في قاعدة البيانات
        try:
            if student_data_handler.is_exists(number):
                raise HTTPException(status_code=400, detail="Student with this registration number already exists.")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # حفظ بيانات الطالب في قاعدة البيانات
        result = student_data_handler.save_student(student_data)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to save student data to the database.")

        return JSONResponse(content={"status": "success", "message": "Student added successfully"}, status_code=201)
    
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/students")
async def get_students():
    try:
        students = student_data_handler.fetch_students()
        # print('students', students)
        # تعديل المسار لإضافة رابط الصورة الكامل
        for student in students:
            # print('student', type(student[6]))
            print('students', student['ImagePath'])
            if student.get("ImagePath"):
                student["ImagePath"] = f"http://127.0.0.1:8000/{student['ImagePath']}"
            else:
                print("Invalid data for ImagePath:", student)
            # print('student', student[6])
        
        return JSONResponse(content=students, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")
