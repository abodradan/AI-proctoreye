from services.student_data_handler import StudentDataHandler
from database.database_manager import DatabaseManager

if __name__ == '__main__':
    db_manager = DatabaseManager()
    # db_manager.close()
    db_manager.connect()
    db_manager.create_tables()

    # db_manager.exam_db.create(Date="2024-12-06", TimeSlot="10:00 - 12:00", Period="First", Level="2", Specialization="AI", Duration="02:00:00", StudentCount=50)
    # db_manager.exam_db.create(Date="2024-12-07", TimeSlot="10:00 - 12:00", Period="First", Level="4", Specialization="CS", Duration="02:00:00", StudentCount=50)
    # db_manager.exam_db.create(Date="2024-12-08", TimeSlot="10:00 - 12:00", Period="First", Level="3", Specialization="CS", Duration="02:00:00", StudentCount=50)
    # db_manager.exam_db.create(Date="2024-12-09", TimeSlot="10:00 - 12:00", Period="First", Level="2", Specialization="CS", Duration="02:00:00", StudentCount=50)
    # db_manager.exam_db.create(Date="2024-12-10", TimeSlot="10:00 - 12:00", Period="First", Level="1", Specialization="CS", Duration="02:00:00", StudentCount=50)
    # db_manager.exam_db.create(Date="2024-12-06", TimeSlot="12:00 - 02:00", Period="Second", Level="4", Specialization="CS", Duration="02:00:00", StudentCount=50)

    # handler = StudentDataHandler()
    # print('db_manager', db_manager.exam_db.all())
    
    exam_data = db_manager.exam_db.find(
            Date='2024-12-06', Specialization='CS', Level=4
        )
    # print('exam_data',exam_data)
    print('exam_data', db_manager.exam_db.find(
            Date='2024-12-06', Specialization='CS', Level=4
        ))
    db_manager.close()
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
    # print('studentHandler', handler.generate_student_id())
    # is_exists = handler.is_exists('22160029')
    # print('is_exists', is_exists)