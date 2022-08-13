from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase 
from rest_framework import status

from accounts.models import CustomUser
from .models import Anime

# Create your tests here.

class AnimeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = CustomUser.objects.create_user(
            username="admin", password="pass",is_staff=True,is_superuser=True
        )
        testuser1.save()

        testuser2 = CustomUser.objects.create_user(
            username="mohammad", password="pass",is_staff=True
        )
        testuser2.save()

        testuser3 = CustomUser.objects.create_user(
            username="ahmad", password="pass"
        )
        testuser3.save()

        test_thing = Anime.objects.create(
            user=testuser1,
            title ="Attack on Titan",
            overview="Attack on Titan is the best anime  ever ever",
            release_date = "2013-04-07",
            vote_average = 12.0,
            vote_count = 123,
        )
        test_thing.save()

        test_thingNotAdmin = Anime.objects.create(
            user=testuser2,
            title ="Demon Slayer",
            overview="Demon Slayer is very sad anime",
            release_date = "2018-04-07",
            vote_average = 9.9,
            vote_count = 564,
        )
        test_thingNotAdmin.save()

    def setUp(self):
        self.client.login(username='admin', password="pass")


    def test_anime_model(self):
        anime = Anime.objects.get(id=1)
        actual_owner = str(anime.user)
        actual_title = str(anime.title)
        actual_overview = str(anime.overview)
        self.assertEqual(actual_owner, "admin")
        self.assertEqual(actual_title, "Attack on Titan")
        self.assertEqual(
            actual_overview, "Attack on Titan is the best anime  ever ever"
        )

    def test_get_anime_list(self):
        url = reverse("animes")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        things = response.data
        self.assertEqual(len(things), 2)
        self.assertEqual(things[0]["title"], "Attack on Titan")


    def test_auth_required(self):
        self.client.logout()
        url = reverse("animes")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete(self):
        self.client.logout()
        self.client.login(username='ahmad', password="pass")
        url = reverse("anime_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



# Tests for Ahmad user he is  is_active = True, is_staff=False, is_superuser=False


    def test_only_active_can_read_data(self):
        self.client.logout()
        self.client.login(username='ahmad', password="pass")

        url = reverse("animes")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        things = response.data
        self.assertEqual(len(things), 2)
        self.assertEqual(things[0]["title"], "Attack on Titan")
    
    def test_active_can_see_detail(self):
        self.client.logout()
        self.client.login(username='ahmad', password="pass")

        url = reverse("anime_detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_active_can_not_add(self):
        self.client.logout()
        self.client.login(username='ahmad', password="pass")

        url = reverse("animes")
        data = {
            "title": "Hunter X Hunter",
            "overview": "Hunter X Hunter Hunter X Hunter Hunter X Hunter Hunter X Hunter Hunter X Hunter",
            "release_date": "2022-08-09",
            "vote_average": 9.1,
            "vote_count": 1500,
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_only_active_can_not_update(self):
        self.client.logout()
        self.client.login(username='ahmad', password="pass")

        url = reverse("anime_detail", args=[1])
        data = {
            "title": "Hunter X Hunter",
            "overview": "Hunter X Hunter Hunter X Hunter Hunter X Hunter Hunter X Hunter Hunter X Hunter",
            "release_date": "2022-08-09",
            "vote_average": 9.1,
            "vote_count": 1500,
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_only_active_can_not_delete(self):
        self.client.logout()
        self.client.login(username='ahmad', password="pass")

        url = reverse("anime_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Tests for Mohammad user he is  is_active= True, is_staff= True, is_superuser= False


    def test_only_staff_can_add(self):
        self.client.logout()
        self.client.login(username='mohammad', password="pass")

        url = reverse("animes")
        data = {
            "title": "Hunter X Hunter",
            "overview": "Hunter X Hunter Hunter X Hunter Hunter X Hunter Hunter X Hunter Hunter X Hunter",
            "release_date": "2022-08-09",
            "vote_average": 9.1,
            "vote_count": 1500,
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_only_staff_can_not_update_if_he_not_the_owner(self):
        self.client.logout()
        self.client.login(username='mohammad', password="pass")
        
        url = reverse("anime_detail", args=[1])
        data = {
            "title": "Attack on Titan",
            "overview": "Attack on Titan better than one peace",
            "release_date": "2013-04-07",
            "vote_average": 9.9,
            "vote_count": 22954,
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_staff_can_update_if_he_the_owner(self):
       
        self.client.logout()
        self.client.login(username='mohammad', password="pass")

        url = reverse("anime_detail", args=[2])
        data = {
            "title": "Hunter X Hunter",
            "overview": "Hunter X Hunter Hunter in very nice anime",
            "release_date": "2022-08-09",
            "vote_average": 9.1,
            "vote_count": 1500,
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_only_staff_can_not_delete_if_he_not_the_owner(self):
        self.client.logout()
        self.client.login(username='mohammad', password="pass")
        
        url = reverse("anime_detail", args=[1])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_delete_if_he_the_owner(self):
        self.client.logout()
        self.client.login(username='mohammad', password="pass")


        url = reverse("anime_detail", args=[2])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        


# Tests for Admin user he is  is_active= True, is_staff= True, is_superuser= True

    def test_only_superuser_can_update_any(self):
        self.client.logout()
        self.client.login(username='admin', password="pass")

        url = reverse("anime_detail", args=[2])
        data = {
            "title": "Hunter X Hunter",
            "overview": "Hunter X Hunter Hunter in very nice anime",
            "release_date": "2022-08-09",
            "vote_average": 9.1,
            "vote_count": 1500,
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_only_superuser_can_delete_any(self):
        self.client.logout()
        self.client.login(username='admin', password="pass")
        url = reverse("anime_detail", args=[2])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


        

