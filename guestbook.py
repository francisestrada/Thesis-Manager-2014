import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1 = 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2 = 'default_guestbook2'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name =DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('guestbook-HTML.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class Guestbook1(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/1?')


class Guestbook2(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/2?')

class MemberOnePage(webapp2.RequestHandler):
    
    def get(self):
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)

        # Ancestor Queries, as shown here, are strongly consistent with the High
        # Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be
        # a slight chance that Greeting that had just been written would not
        # show up in a query.
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('MemberOne.html')
        self.response.write(template.render(template_values))


class MemberTwoPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)

        # Ancestor Queries, as shown here, are strongly consistent with the High
        # Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be
        # a slight chance that Greeting that had just been written would not
        # show up in a query.
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('MemberTwo.html')
        self.response.write(template.render(template_values))


class Thesis(ndb.Model):
    title=ndb.StringProperty(indexed=False)
    author=ndb.StringProperty(indexed=False)
    year=ndb.StringProperty(indexed=False)
    status=ndb.StringProperty(indexed=False)
    description=ndb.StringProperty(indexed=False)

class SuccessPageHandlerThesis(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('success.html')
        self.response.write(template.render())

class SuccessPageHandlerStudent(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successDent.html')
        self.response.write(template.render())    

class SuccessPageHandlerAdviser(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successAd.html')
        self.response.write(template.render())    

class ThesisNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_new.html')
        self.response.write(template.render(template_values))
    def post(self):
        thesis = Thesis() 
        thesis.title = self.request.get('title')
        thesis.author= self.request.get('author')
        thesis.year = self.request.get('year')
        thesis.status = self.request.get('status')
        thesis.description = self.request.get('description')
        thesis.put()
        self.redirect('/thesis/success') 

class ThesisDescriptionHandler(webapp2.RequestHandler):
        def get(self, thesis_id):
                thesis_all=Thesis.query().fetch()
                thesis_id = int(thesis_id)
                template_values={
                        'id': thesis_id,
                        'thesis_all': thesis_all
                }
                template = JINJA_ENVIRONMENT.get_template('thesis_description.html')
                self.response.write(template.render(template_values))
 
class ThesisListHandler(webapp2.RequestHandler):
        
        def get(self):

                thesis_all=Thesis.query().fetch()
                template_values={
                        'thesis_all': thesis_all
                }
 
                template = JINJA_ENVIRONMENT.get_template('thesis_list.html')
                self.response.write(template.render(template_values))


class Adviser(ndb.Model):
    title=ndb.StringProperty(indexed=False)
    first_name=ndb.StringProperty(indexed=False)
    last_name=ndb.StringProperty(indexed=False)
    email=ndb.StringProperty(indexed=False)
    phone_number=ndb.StringProperty(indexed=False)
    department=ndb.StringProperty(indexed=False)

class SuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successAd.html')
        self.response.write(template.render())

class AdviserNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }

        template = JINJA_ENVIRONMENT.get_template('adviserNew.html')
        self.response.write(template.render(template_values))

    def post(self):
        adviser = Adviser() 
        adviser.title = self.request.get('title')
        adviser.first_name= self.request.get('first_name')
        adviser.last_name = self.request.get('last_name')
        adviser.email = self.request.get('email')
        adviser.phone_number = self.request.get('phone_number')
        adviser.department = self.request.get('department')
        adviser.put()
        self.redirect('/adviser/success')

class AdviserDescriptionHandler(webapp2.RequestHandler):
        def get(self, adviser_id):
                adviser_all=Adviser.query().fetch()
                adviser_id = int(adviser_id)
                template_values={
                        'id': adviser_id,
                        'adviser_all': adviser_all
                }
                template = JINJA_ENVIRONMENT.get_template('adviserView.html')
                self.response.write(template.render(template_values))
 
class AdviserListHandler(webapp2.RequestHandler):
        def get(self):
                adviser_all=Adviser.query().fetch()
                template_values={
                        'adviser_all': adviser_all
                }
 
                template = JINJA_ENVIRONMENT.get_template('adviserList.html')
                self.response.write(template.render(template_values))

        
class AdviserEditHandler(webapp2.RequestHandler):
        def get(self, adviser_id):
                adviser_all=Adviser.query().fetch()
                adviser_id = int(adviser_id)
                if users.get_current_user():
                    url = users.create_logout_url(self.request.uri)
                    url_linktext = 'Logout'
                else:
                    url = users.create_login_url(self.request.uri)
                    url_linktext = 'Login'
                template_values={
                        'id': adviser_id,
                        'adviser_all': adviser_all,
                        'url': url,
                        'url_linktext': url_linktext,
                        'user_name': users.get_current_user()
                }
                template = JINJA_ENVIRONMENT.get_template('adviserEdit.html')
                self.response.write(template.render(template_values))
        def post(self, adviser_id):

            adviser_id = int(adviser_id)
            adviser = Adviser.get_by_id(adviser_id)
            adviser.title = self.request.get('title')
            adviser.first_name= self.request.get('first_name')
            adviser.last_name = self.request.get('last_name')
            adviser.email = self.request.get('email')
            adviser.phone_number = self.request.get('phone_number')
            adviser.department = self.request.get('department')
            adviser.put()

            self.redirect('/adviser/list')

class Student(ndb.Model):
    student_number=ndb.StringProperty(indexed=False)
    first_name=ndb.StringProperty(indexed=False)
    last_name=ndb.StringProperty(indexed=False)
    email=ndb.StringProperty(indexed=False)
    phone_number=ndb.StringProperty(indexed=False)
    course=ndb.StringProperty(indexed=False)

class SuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successDent.html')
        self.response.write(template.render())

class StudentNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }

        template = JINJA_ENVIRONMENT.get_template('studentNew.html')
        self.response.write(template.render(template_values))

    def post(self):
        student = Student() 
        student.student_number = self.request.get('student_number')
        student.first_name= self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.phone_number = self.request.get('phone_number')
        student.course = self.request.get('course')
        student.put()
        self.redirect('/student/success')

class StudentDescriptionHandler(webapp2.RequestHandler):
    def get(self, student_id):
                student_all=Student.query().fetch()
                student_id = int(student_id)
                template_values={
                        'id': student_id,
                        'student_all': student_all
                }
                template = JINJA_ENVIRONMENT.get_template('studentView.html')
                self.response.write(template.render(template_values))
 
class StudentListHandler(webapp2.RequestHandler):
    def get(self):
                student_all=Student.query().fetch()
                template_values={
                        'student_all': student_all
                }
 
                template = JINJA_ENVIRONMENT.get_template('studentList.html')
                self.response.write(template.render(template_values))

class StudentEditHandler(webapp2.RequestHandler):
        def get(self, student_id):
                student_all=Student.query().fetch()
                student_id = int(student_id)
                
                if users.get_current_user():
                    url = users.create_logout_url(self.request.uri)
                    url_linktext = 'Logout'
                else:
                    url = users.create_login_url(self.request.uri)
                    url_linktext = 'Login'

                template_values = {
                    'url': url,
                    'url_linktext': url_linktext,
                    'user_name': users.get_current_user(),
                    'id': student_id,
                    'student_all': student_all
                }
                template = JINJA_ENVIRONMENT.get_template('studentEdit.html')
                self.response.write(template.render(template_values))
        def post(self, student_id):

            student_id = int(student_id)
            student = Student.get_by_id(student_id)
            student.student_number = self.request.get('student_number')
            student.first_name= self.request.get('first_name')
            student.last_name = self.request.get('last_name')
            student.email = self.request.get('email')
            student.phone_number = self.request.get('phone_number')
            student.course = self.request.get('course')
            student.put()

            self.redirect('/student/list')

class ThesisEditHandler(webapp2.RequestHandler):
        def get(self, thesis_id):
                thesis_all=Thesis.query().fetch()
                thesis_id = int(thesis_id)
              
                if users.get_current_user():
                    url = users.create_logout_url(self.request.uri)
                    url_linktext = 'Logout'
                else:
                    url = users.create_login_url(self.request.uri)
                    url_linktext = 'Login'

                template_values={
                    'id': thesis_id,
                    'thesis_all': thesis_all,
                    'url': url,
                    'url_linktext': url_linktext,
                    'user_name': users.get_current_user()
            }
                template = JINJA_ENVIRONMENT.get_template('thesisEdit.html')
                self.response.write(template.render(template_values))

        def post(self, thesis_id):
            thesis_id = int(thesis_id)
            thesis = Thesis.get_by_id(thesis_id)
            thesis.title = self.request.get('title')
            thesis.author= self.request.get('author')
            thesis.year = self.request.get('year')
            thesis.status = self.request.get('status')
            thesis.description = self.request.get('description')
            thesis.put()

            self.redirect('/thesis/list')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/sign1', Guestbook1),
    ('/sign2', Guestbook2),
    ('/module-1/1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),
    ('/thesis/new', ThesisNewHandler),
    ('/adviser/success', SuccessPageHandlerAdviser),
    ('/student/success', SuccessPageHandlerStudent),
    ('/thesis/success', SuccessPageHandlerThesis),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/description/(\d+)', ThesisDescriptionHandler),
    ('/adviser/new', AdviserNewHandler),
    ('/successAd', SuccessPageHandler),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/view/(\d+)', AdviserDescriptionHandler),
    ('/adviser/edit/(\d+)', AdviserEditHandler),
    ('/student/new', StudentNewHandler),
    ('/success', SuccessPageHandler),
    ('/success', SuccessPageHandler),
    ('/success', SuccessPageHandler),
    ('/student/list', StudentListHandler),
    ('/student/view/(\d+)', StudentDescriptionHandler),
    ('/student/edit/(\d+)', StudentEditHandler),
    ('/thesis/edit/(\d+)', ThesisEditHandler)
], debug=True)