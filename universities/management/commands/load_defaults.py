from universities.models import FacilityMaster

facility_list = [
    "Libraries", "Laboratories", "Sports Facilities", "Student Center", "Dormitories",
    "Cafeterias", "Health Center", "ICT Centers", "Lecture Halls", "Auditoriums",
    "Chapel/Prayer Rooms", "Hostels", "Research Centers", "Recreational Parks",
    "Transport Services", "Career Counseling Centers", "E-Learning Facilities",
    "Student Accommodation", "Swimming Pool", "Wi-Fi Across Campus"
]

for name in facility_list:
    FacilityMaster.objects.get_or_create(name=name)

print("Facilities added successfully!")