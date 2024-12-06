from services.student_data_handler import StudentDataHandler
from database.database_manager import DatabaseManager

if __name__ == '__main__':
    # db_manager = DatabaseManager()
    # # db_manager.close()
    # db_manager.connect()
    # db_manager.create_tables()

    handler = StudentDataHandler()
    print('studentHandler', handler.generate_student_id())
    # student_data = {
    #     "StudentName": "abod",
    #     "number": "22160033",
    #     "College": "Computer Science",
    #     "Level": "2",
    #     "Specialization": "Computer Science",
    #     "ImagePath": "/images/ahmed.jpg"
    # }
    # handler.save_student(student_data)
    # print('studentHandler', handler.generate_student_id())
    # student_data1 = {
    #     "StudentName": "Ahmed",
    #     "number": "22160034",
    #     "College": "Computer Science",
    #     "Level": "2",
    #     "Specialization": "AI",
    #     "ImagePath": "/images/ahmed.jpg"
    # }
    # handler.save_student(student_data1)
    print('studentHandler', handler.generate_student_id())
    is_exists = handler.is_exists('22160029')
    print('is_exists', is_exists)