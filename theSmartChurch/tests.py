from django.test import TestCase
from .models import Profile,Project
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        '''
        run before test
        '''
        user1=User(username='larissa')
        user1.save()
        self.profile1=Profile(user=user1,bio='Backend developer',email='lala@gmail.com')

    def test_instance(self):
        '''
        test profile object initialization 
        '''
        self.assertTrue(isinstance(self.profile1,Profile))


    def test_save(self):
        '''
        test profile save 
        '''
        self.profile1.save()
        profiles=Profile.objects.all()
        self.assertTrue(len(profiles)>=1)


class ProjectTest(TestCase):
    def setUp(self):
        '''
        run before test
        '''
        user1=User(username='larissa')
        user1.save()
        profile1=Profile(user=user1,bio='Backend developer',email='lala@gmail.com')
        profile1.save()
        self.project1=Project(profile=profile1,name='project1',description='Testing description',link='www.testing.com')
    

    def test_instance(self):
        '''
        test project object initialization
        '''
        self.assertTrue(isinstance(self.project1,Project))


    def test_save(self):
        '''
        test project save 
        '''
        self.project1.save()
        projects=Project.objects.all()
        self.assertTrue(len(projects)>=1)

    def test_search(self):
        '''
        test search method for project search method
        '''
        self.project1.save()
        search_term='p'
        search_projects=Project.search_by_name(search_term)
        self.assertTrue(len(search_projects)==1 )


class ProjectTest(TestCase):
    def setUp(self):
        '''
        run before test
        '''
        user1=User(username='floride')
        user1.save()
        profile1=Profile(user=user1,bio='Backend developer',email='flo.tuyisenge@gmail.com')
        profile1.save()
        self.project1=Project(profile=profile1,name='project1',description='Testing description',link='www.testing.com')
    

    def test_instance(self):
        '''
        test project object initialization
        '''
        self.assertTrue(isinstance(self.project1,Project))


    def test_save(self):
        '''
        test project save 
        '''
        self.project1.save()
        projects=Project.objects.all()
        self.assertTrue(len(projects)>=1)

    def test_search(self):
        '''
        test search method for project search method
        '''
        self.project1.save()
        search_term='p'
        search_projects=Project.search_by_name(search_term)
        self.assertTrue(len(search_projects)==1 )
