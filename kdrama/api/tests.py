from django.test import TestCase
from .models import Drama , Cast , Genre
# Create your tests here.


drama1 = Drama(title="Happy Hours",description="Love Story of panda and angel",category="romance",rating="9.8",img="https://google.com")
drama1.save()
drama2 = Drama(title="Sunday Morning",description="Hacker in the underworld",category="thriller",rating="9.8",img="https://google.com")
drama2.save()
drama3 = Drama(title="whoami ",description="A giant animal breaks house",category="action",rating="9.8",img="https://google.com")
drama3.save()

genre1 = Genre(genre="romance",dramaId=drama2)
genre1.save()
genre2 = Genre(genre="action",dramaId=drama2)
genre2.save()
genre3 = Genre(genre="thrill",dramaId=drama2)
genre3.save()
genre4 = Genre(genre="comedy",dramaId=drama2)
genre4.save()
