from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    # define the setUp method that will automatically  run before every test method in the class
    def setUp(self):
        # Inside create a user that we can reference  later on in all the tests inside this class.
        # we will use this user’s credentials when  we need to log in to create a post.
        # We’ll also need this user when we manually  create a post and need to set its owner]
        User.objects.create_user(username='adam', password='pass')

    # test we can list posts present in the database
    def test_can_list_posts(self):
        # First, I’ll get the user adam which  we just created in the setUp method,
        # so that I can associate the newly  created post with that use
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')

        # make test network requests by calling  an appropriate method on self-dot-client,
        # namely self.client.get  or .post, .put, and so on,
        # followed by the url we’re making the request to
        response = self.client.get('/posts/')
        # first make it fail by  asserting the status_code isn’t 200.\
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    # make sure that a  logged in user can create a post.
    def test_logged_in_user_can_create_post(self):
        # To test protected routes (which are routes  that require the user to be logged in),
        # we’ll have to log in first using the  APITest client
        self.client.login(username='adam', password='pass')
        # make a post request to ‘/posts/’ with  post data and save the response to a variable
        response = self.client.post('/posts/', {'title': 'a title'})
        # count all posts and check that there is just one
        count = Post.objects.count()
        self.assertEqual(count, 1)
        #  also assert the response  code to be 201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_logged_in_to_make_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        # create two users to test
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        # create two posts, one for each user
        Post.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Post.objects.create(
            owner=brian, title='another title', content='brians content'
        )

    # test to see if it is possible to retrieve a post with a valid id
    def test_can_retrieve_post_using_valid_id(self):
        # create a new test method and make  a get request to fetch the first post
        response = self.client.get('/posts/1/')
        # assert the fetched post’s title is  appropriate, and set the status to 200
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/333/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_test(self):
        # log in as 'adam'
        self.client.login(username='adam', password='pass')
        # send a put request to  a url with their post’s ID
        response = self.client.put(('/posts/1/'), {'title': 'a new title'})
        # we’ll fetch that post  from the database by ID
        post = Post.objects.filter(pk=1).first()
        # Once we have it saved to a variable, we’ll  test that the change to the post title has
        # been persisted
        self.assertEqual(post.title, 'a new title')
        # We’ll also make sure the  200 OK code is sent with the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_post_they_dont_own(self):
        self.client.login(username='brian', password='pass')
        response = self.client.put(('/posts/1/'), {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

