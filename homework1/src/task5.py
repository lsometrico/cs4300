# list of some of my personal favorite books 
fav_books = [
        ("BOMB! The race to build - and steal - the world's most dangerous weapon"), ("Kingdom Hearts Ultimania"),
        ("Last God Standing"), ("Puerto Rico"),
        ("Atomic Habits"), ("How to Become a Monster to Get Away With Murder"),

]

#list slicing to list the first three book
def first_three(books=fav_books):
    return books[:3]


student_database = {
        "Porter Robinson":"S01092019",
        "Hugo Leclerq": "S12122017",
        "Sander Van Djick": "S47569428",
        "Joel Zimmerman": "S327835643",
        "Sonny Moore": "S347678566"
}

def get_student_id(name, database=student_database):
    return database.get(name)

def main():
    print("first three books:")
    for title in first_three():
        print(f"{title}")

    print("student database:")
    for name, student_id in student_database.items():
        print(f"{name}: {student_id}")


if __name__ == "__main__":
    main()