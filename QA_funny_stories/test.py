#!/usr/bin/env python
import unittest2
import client


class userTest(unittest2.TestCase):
    @classmethod
    def setUpClass(self):
        client.createURL().registration('user', 'pass')

    def test_registration(self):
        result = client.createURL().registration('user1', 'pass1')
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'user1': 'OK'}, body)
        self.assertEqual(200, code)

    def test_reg_loginExist(self):
        result = client.createURL().registration('user', 'pass')
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'user': 'error! login exists'}, body)
        self.assertEqual(200, code)

    def test_logOut_after_logIn(self):
        client.createURL().log_in('user', 'pass')
        result = client.createURL().log_out()
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'user': 'log out'}, body)
        self.assertEqual(200, code)

    def test_logOut_without_logIn(self):
        client.createURL().log_out()
        result = client.createURL().log_out()
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'log in!'}, body)
        self.assertEqual(200, code)

    def test_logIn_registered_User(self):
        result = client.createURL().log_in('user', 'pass')
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'user': 'OK'}, body)
        self.assertEqual(200, code)

    def test_logIn_without_logOut(self):
        client.createURL().log_in('user', 'pass')
        result = client.createURL().log_in('user', 'pass')
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'log out!'}, body)
        self.assertEqual(200, code)

    def test_logIn_unregistered_User(self):
        client.createURL().log_out()
        result = client.createURL().log_in('unreg_user', 'pass')
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'unreg_user': 'registration?'}, body)
        self.assertEqual(200, code)

    def test_logIn_invalid_password(self):
        client.createURL().log_out()
        result = client.createURL().log_in('user', 'pass1')
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'invalid password'}, body)
        self.assertEqual(200, code)


class storyTest(unittest2.TestCase):
    @classmethod
    def setUpClass(self):
        client.createURL().registration('userStory', 'pass')
        joke = "Xa - Xa - Xa!!!"
        client.createURL().add_story('joke1', joke)
        client.createURL().add_story('joke2', joke)
        client.createURL().log_out()
        client.createURL().registration('userStory1', 'pass')
        client.createURL().log_out()

    def test_addStory_logOut(self):
        joke = "Xa - Xa - Xa!!!"
        client.createURL().log_out()
        result = client.createURL().add_story('joke1', joke)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'log in!!!'}, body)
        self.assertEqual(200, code)

    def test_addStory_logIn(self):
        joke = "Xa - Xa - Xa!!!"
        client.createURL().log_in('userStory1', 'pass')
        result = client.createURL().add_story('joke1', joke)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'joke1': joke}, body)
        self.assertEqual(200, code)
        client.createURL().del_story(3)

    def test_del_exist_Story_login(self):
        client.createURL().log_in('userStory', 'pass')
        client.createURL().add_story('joke1', 'Xa - Xa - Xa!!!')
        result = client.createURL().del_story(3)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'story': 'OK'}, body)
        self.assertEqual(200, code)

    def test_delStory_logOut(self):
        client.createURL().log_out()
        result = client.createURL().del_story(1)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'log in!'}, body)
        self.assertEqual(200, code)

    def test_del_no_exist_Story(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().del_story(9999)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'this story does not exist'}, body)
        self.assertEqual(200, code)

    def test_get_listStory_log_in(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().list_all()
        body = eval(result[0])
        code = result[1]
        self.assertEqual(code, 200)
        self.assertEqual(body, {'stories': [[ 'ID: 1'
                                            , u'Story name: joke1'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ],
                                            [ 'ID: 2'
                                            , u'Story name: joke2'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ]]})

    def test_get_listStory_log_out(self):
        client.createURL().log_out()
        result = client.createURL().list_all()
        body = eval(result[0])
        code = result[1]
        self.assertEqual(200, code)
        self.assertEqual(body, {'stories': [[ 'ID: 1'   
                                            , u'Story name: joke1'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ], 
                                            [ 'ID: 2'
                                            , u'Story name: joke2'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ]]})

    def test_get_story(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().list_story(2)
        body = eval(result[0])
        code = result[1]
        self.assertEqual(200, code)
        self.assertEqual(body, {'stories': ['ID: 2'   
                                            , u'Story name: joke2'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ]})

    def test_like_story_logIn(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().like_story(2)
        body = eval(result[0])
        code = result[1]
        self.assertEqual(body, {'stories': ['ID: 2'   
                                           , u'Story name: joke2'
                                           , u'Story body: Xa - Xa - Xa!!!'
                                           , 'Author: 1'
                                           , 'Rating: 1'
                                           ]})
        self.assertEqual(200, code)
        client.createURL().dislike_story(2)

    def test_like_story_noExist(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().like_story(999)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'this story does not exist'}, body)
        self.assertEqual(200, code)

    def test_dislike_story_logIn(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().dislike_story(2)
        body = eval(result[0])
        code = result[1]
        self.assertEqual(body, {'stories': ['ID: 2'   
                                           , u'Story name: joke2'
                                           , u'Story body: Xa - Xa - Xa!!!'
                                           , 'Author: 1'
                                           , 'Rating: -1'
                                           ]})
        self.assertEqual(200, code)
        client.createURL().like_story(2)


    def test_dislike_story_noExist(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().dislike_story(999)
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'this story does not exist'}, body)
        self.assertEqual(200, code)


    def test_list_author_story_login(self):
        client.createURL().log_in('userStory', 'pass')
        result = client.createURL().author_stories("userStory")
        body = eval(result[0])
        code = result[1]
        self.assertEqual(200, code)
        self.assertEqual(body, {'stories': [['ID: 1'   
                                            , u'Story name: joke1'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ],
                                            ['ID: 2'   
                                            , u'Story name: joke2'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'
                                            ]]})


    def test_list_author_story_out(self):
        client.createURL().log_in('userStory', 'pass')
        client.createURL().log_out()
        result = client.createURL().author_stories("userStory")
        body = eval(result[0])
        code = result[1]
        self.assertEqual(200, code)
        self.assertEqual(body, {'stories': [[ 'ID: 1'   
                                            , u'Story name: joke1'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0'],
                                            [ 'ID: 2'   
                                            , u'Story name: joke2'
                                            , u'Story body: Xa - Xa - Xa!!!'
                                            , 'Author: 1'
                                            , 'Rating: 0']
                                            ]})

    def test_list_no_reg_author_story(self):
        result = client.createURL().author_stories("unreg_userStory")
        body = eval(result[0])
        code = result[1]
        self.assertEqual({'error': 'the author does not exist'}, body)
        self.assertEqual(200, code)


if __name__ == "__main__":
    unittest2.main()
