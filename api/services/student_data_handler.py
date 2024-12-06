import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from database.database_manager import DatabaseManager

class StudentDataHandler:
    def __init__(self):
        # إنشاء كائن DatabaseManager مرة واحدة
        self.db_manager = DatabaseManager()
        self.db_manager.connect()
        self.db_manager.create_tables()

    def generate_student_id(self):
        try:            
            # التحقق من وجود بيانات في قاعدة البيانات
            last_student = self.db_manager.student_db.last()
            print('last_student', last_student)
            
            if not last_student:
                return 0
            
            return last_student[0] + 1
        except Exception as e:
            print(f"Error generating student ID: {e}")
            return None

    def is_exists(self, number):
        try:
            # التحقق من وجود الطالب بناءً على الرقم
            student = self.db_manager.student_db.exists(Number=number)
            return bool(student)
        except Exception as e:
            print(f"Error checking registration number: {e}")
            return False

    def save_student(self, student_data):
        try:
            # التحقق من وجود الرقم المسجل في قاعدة البيانات
            if self.is_exists(student_data['number']):
                raise ValueError(f"Student with registration number {student_data['number']} already exists.")
            
            student_data['StudentID'] = self.generate_student_id()
            if student_data['StudentID'] is None:
                return False

            self.db_manager.student_db.create(
                StudentID=student_data['StudentID'],
                StudentName=student_data['StudentName'],
                Number=student_data['number'],
                College=student_data.get('College', None),
                Level=student_data.get('Level', None),
                Specialization=student_data.get('Specialization', None),
                ImagePath=student_data.get('ImagePath', None),
            )
            return True
        except Exception as e:
            error_message = f"Error saving student data: {str(e)}"
            raise ValueError(error_message)

    def fetch_students(self):
        try:
            # استرجاع جميع الطلاب
            students = self.db_manager.student_db.all()

            # تحويل الصفوف إلى قواميس إذا لم تكن كذلك
            formatted_students = []
            for student in students:
                # إذا كانت النتيجة سلسلة نصية أو أي نوع غير متوقع
                if isinstance(student, (list, tuple)):
                    formatted_students.append({
                        "StudentID": student[0],
                        "StudentName": student[1],
                        "Number": student[2],
                        "College": student[3],
                        "Level": student[4],
                        "Specialization": student[5],
                        "ImagePath": student[6] if len(student) > 6 else None
                    })
                elif isinstance(student, dict):
                    formatted_students.append(student)  # إذا كانت البيانات صحيحة كقواميس

            return formatted_students
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return []

