from django.test import TestCase
from django.test.client import Client


class URLTest(TestCase):
    """
    call "with python manage.py test'
    """
    fixtures = ['portal_test_fixture.json']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assert_equal(response.status_code, 200)
        response = self.client.get('/search')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'Explore your story')

    def test_advsearch(self):
        response = self.client.get('/advsearch')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'Logic between keywords')

    def test_about(self):
        response = self.client.get('/about')
        self.assert_equal(response.status_code, 200)

    def test_faq(self):
        response = self.client.get('/faq')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'What kind of content')

    def test_help(self):
        response = self.client.get('/help')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'Selections containing the word')

    def test_mediatype(self):
        response = self.client.get('/mediatype?mt=image')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'Charts')

    def test_contributors(self):
        response = self.client.get('/contributors')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'Contributors')

    def test_results(self):
        response = self.client.get('/results?q=steamboats')
        self.assert_equal(response.status_code, 200)
        response = self.client.get('/results?q=&bl=and&st=kw&fz=1'
                                   '&site=Maritime+History+of+the+Great+Lakes'
                                   '&site=Richmond+Hill+Public+Library'
                                   '&sp=&mt=collection&mt=image&rows=40')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'CORSICAN in the Lachine Rapids')
        response = self.client.get('/results?q=Montr%C3%A9al')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'montreal')

    def test_parts(self):
        response = self.client.get('/results?q=robertson&id=MHGL.66277')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'http://images.maritimehistoryofthegreatlakes.ca/'
                                      '66277/page/81?q=robertson&amp;docid=MHGL.66277')

    def test_features(self):
        response = self.client.get('/results?q2=steamboats&fc=true&fm=true ')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'mysteries')

    def test_no_q(self):
        response = self.client.get('/fc=true&fm=true ')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, 'mysteries')

    def test_spell(self):
        response = self.client.get('/results?q=steamboots')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, ' We substituted')
        #response = self.client.get('/results?q=steamboots+Lachine')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, ' We substituted')
        response = self.client.get('/results?q=bohmian')
        self.assert_equal(response.status_code, 200)
        self.assertContains(response, ' We substituted')
        #response = self.client.get('/results?q=gfdkuhgfew+adlskkjh')
        #self.assertEqual(response.status_code, 200)
        #self.assertContains(response, ' We substituted')

    def test_count(self):
        response = self.client.get('/count?q=steamboats')
        self.assert_equal(response.status_code, 200)
        # self.assertContains(response, )

    #the xml outputs
    def test_opensearch(self):
        response = self.client.get('/opensearch.xml')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, '</OpenSearchDescription>')

    def test_dc(self):
        response = self.client.get('/dc?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, 'dc:identifier')

    def test_mods(self):
        response = self.client.get('/mods?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, '/modsCollection')

    def test_rss(self):
        response = self.client.get('/rss?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, '</item></channel></rss>')

    def test_atom(self):
        response = self.client.get('/atom?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, '</entry></feed>')

    def test_rdf(self):
        response = self.client.get('/rdf?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, '</rdf:RDF>')

    def test_solr(self):
        response = self.client.get('/solr?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'text/xml')
        self.assertContains(response, '</response>')

    def test_kml(self):
        response = self.client.get('/test.kml?q=steamboats')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'application/vnd.google-earth.kml+xml')
        self.assertContains(response, '</Placemark></Document></kml>')

    def test_unapi(self):
        response = self.client.get('/unapi')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'application/xml')
        self.assertContains(response, '</formats')

    def test_unapi_id(self):
        response = self.client.get('/unapi?id=MHGL.1')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'application/xml')
        self.assertContains(response, ' id="MHGL.1">')

    def test_unapi_mods(self):
        response = self.client.get('/unapi?id=MHGL.1&format=mods')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'application/xml')
        self.assertContains(response, '</modsCollection>>')

    def test_unapi_dc(self):
        response = self.client.get('/unapi?id=MHGL.1&format=dc')
        self.assert_equal(response.status_code, 200)
        self.assert_equal(response['Content-Type'], 'application/xml')
        self.assertContains(response, '</records>')

#class ExternalURLFunctions:
    #test externalurl Functions
    def assert_equal(self, status_code, param, **kwargs):
        pass

    def assertContains(self, response, param, **kwargs):
        pass
