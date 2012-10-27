from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from django.core.urlresolvers import reverse

from cellcounter.main.models import CellCountInstance, CellType

class TestSubmitPageContext(TestCase):
    fixtures = ['test_user.json', 'test_count.json']

    POST_DATA = {u'bonemarrow-haemodilution': [u'Mild'], u'band_forms-cell': [u'3'], u'granulopoiesis-dysplasia': [u'None'], u'granulopoiesis-comment': [u''], u'erythroid-abnormal_count': [u'4'], u'myelocytes-normal_count': [u'11'], u'lymphocytes-cell': [u'8'], u'blasts-normal_count': [u'0'], u'megakaryocyte-relative_count': [u'Absent'], u'erythropoiesis-comment': [u''], u'basophils-normal_count': [u'1'], u'plasma_cells-abnormal_count': [u'7'], u'histiocytes-normal_count': [u'8'], u'neutrophils-normal_count': [u'9'], u'blasts-cell': [u'5'], u'blasts-abnormal_count': [u'4'], u'megakaryocyte-dysplasia': [u'None'], u'eosinophils-normal_count': [u'5'], u'megakaryocyte-comment': [u''], u'promyelocytes-normal_count': [u'9'], u'promyelocytes-abnormal_count': [u'6'], u'histiocytes-abnormal_count': [u'6'], u'bonemarrow-site': [u'Iliac Crest'], u'lymphocytes-normal_count': [u'6'], u'other-normal_count': [u'0'], u'bonemarrow-trail_cellularity': [u'Hypo'], u'csrfmiddlewaretoken': [u'3FUNtetaJt2SF9W11RYd6SxvMnqaTXzG'], u'monocytes-normal_count': [u'2'], u'cellcount-tissue_type': [u'Bone marrow'], u'myelocytes-abnormal_count': [u'7'], u'basophils-abnormal_count': [u'5'], u'eosinophils-cell': [u'6'], u'histiocytes-cell': [u'11'], u'monocytes-cell': [u'10'], u'erythroid-cell': [u'7'], u'eosinophils-abnormal_count': [u'6'], u'neutrophils-cell': [u'1'], u'monocytes-abnormal_count': [u'3'], u'bonemarrow-ease_of_aspiration': [u'Dry'], u'band_forms-normal_count': [u'14'], u'bonemarrow-particle_cellularity': [u'Hypo'], u'band_forms-abnormal_count': [u'8'], u'basophils-cell': [u'12'], u'erythropoiesis-dysplasia': [u'None'], u'other-cell': [u'13'], u'erythroid-normal_count': [u'3'], u'plasma_cells-normal_count': [u'5'], u'promyelocytes-cell': [u'4'], u'cellcount-overall_comment': [u''], u'other-abnormal_count': [u'0'], u'myelocytes-cell': [u'2'], u'bonemarrow-particulate': [u'No particles'], u'neutrophils-abnormal_count': [u'6'], u'lymphocytes-abnormal_count': [u'6'], u'plasma_cells-cell': [u'9'], u'ironstain-stain_performed': [u'on'], u'ironstain-comment': [u''], u'ironstain-iron_content': [u'2'], u'ironstain-ringed_sideroblasts': [u'on']}

    def test_get_submit_page_loggedout(self):
        client = Client()
        response = client.get(reverse('new_count'), follow=True)
        self.assertRedirects(response, 
                "%s?next=%s" %(reverse('login'),
                               reverse('new_count')))

    def test_get_submit_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('new_count'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/submit.html')
        self.assertIn('cellcount', response.context)
        self.assertIn('bonemarrowbackground', response.context)
        self.assertIn('erythropoiesis_form', response.context)
        self.assertIn('granulopoiesis_form', response.context)
        self.assertIn('megakaryocyte_form', response.context)
        self.assertIn('ironstain_form', response.context)
        self.assertIn('cellcountformslist', response.context)

    def test_post_submit_page_redirects(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.post(reverse('new_count'), self.POST_DATA)

        self.assertRedirects(response, reverse('edit_count', kwargs={'count_id': 3}))

    def test_post_submit_page_creates_count(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.post(reverse('new_count'), self.POST_DATA)

        cell_count = CellCountInstance.objects.get(id=3)
        self.assertEqual(3, cell_count.id)

class TestViewCount(TestCase):

    fixtures = ['test_user.json', 'test_count.json']

    def test_view_nonexistent_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 25}))
        self.assertEqual(response.status_code, 404)
    
    def test_view_nonexistent_page_loggedout(self):
        client = Client()
        response = client.get(reverse('view_count', kwargs={'count_id': 25}), follow=True)
        self.assertRedirects(response, 
                "%s?next=%s" %(reverse('login'),
                               reverse('view_count', kwargs={'count_id': 25})))

    def test_view_existing_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 1}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_existing_page_loggedout(self):
        client = Client()
        response = client.get(reverse('view_count', kwargs={'count_id': 1}), follow=True)
        self.assertRedirects(response, 
                "%s?next=%s" %(reverse('login'),
                               reverse('view_count', kwargs={'count_id': 1})))

    def test_view_own_page(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/report.html')
        self.assertIn('cellcount', response.context)
        self.assertIn('bonemarrowbackground', response.context)
        self.assertIn('erythropoiesis', response.context)
        self.assertIn('granulopoiesis', response.context)
        self.assertIn('megakaryocytes', response.context)
        self.assertIn('ironstain', response.context)
        self.assertIn('cellcount_list', response.context)

    def test_view_other_page(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 2}))
        self.assertEqual(response.status_code, 403)

class TestViewMyCount(TestCase):

    fixtures = ['test_user.json', 'test_count.json']

    def test_view_my_count_loggedout(self):
        client = Client()
        response = client.get(reverse('my_counts'), follow=True)
        self.assertRedirects(response, 
                "%s?next=%s" %(reverse('login'),
                               reverse('my_counts')))

    def test_view_my_count_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('my_counts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/count_list.html')
        self.assertIn('count_list', response.context)

class TestEditCount(TestCase):
    fixtures = ['test_user.json', 'test_count.json']

    def test_edit_nonexistent_count_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('edit_count', kwargs={'count_id': 25}))
        self.assertEqual(response.status_code, 404)
    
    def test_edit_nonexistent_page_loggedout(self):
        client = Client()
        response = client.get(reverse('edit_count', kwargs={'count_id': 25}), follow=True)
        self.assertRedirects(response, 
                "%s?next=%s" %(reverse('login'),
                               reverse('edit_count', kwargs={'count_id': 25})))
    
    def test_edit_existing_page_loggedout(self):
        client = Client()
        response = client.get(reverse('edit_count', kwargs={'count_id': 1}), follow=True)
        self.assertRedirects(response, 
                "%s?next=%s" %(reverse('login'),
                               reverse('edit_count', kwargs={'count_id': 1})))

    def test_edit_own_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('edit_count', kwargs={'count_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cellcountinstance_form', response.context)
        self.assertIn('bonemarrowbackground_form', response.context)
        self.assertIn('erythropoiesis_form', response.context)
        self.assertIn('granulopoiesis_form', response.context)
        self.assertIn('megakaryocyte_form', response.context)
        self.assertIn('ironstain_form', response.context)
        self.assertIn('cellcount_form_list', response.context)
    
    def test_edit_other_page(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('edit_count', kwargs={'count_id': 2}))
        self.assertEqual(response.status_code, 403)

class TestCellCount(TestCase):
    fixtures = ['test_user.json', 'test_count.json']

    def test_percentage_count(self):
        cellcount = CellCountInstance.objects.get(id=1)
        cellcount_set = cellcount.cellcount_set.all()

        self.assertEqual(cellcount_set[0].cell.machine_name, 'neutrophils')
        self.assertEqual(cellcount_set[0].percentage(), 12.0)

class TestCellCountInstance(TestCase):
    fixtures = ['test_user.json', 'test_count.json']

    def test_total_count(self):
        cellcount = CellCountInstance.objects.get(id=1)
        self.assertEqual(125, cellcount.total_cellcount())

    def test_erythroid_count(self):
        cellcount = CellCountInstance.objects.get(id=1)
        self.assertEqual(6, cellcount.erythroid_cellcount())

    def test_myeloid_count(self):
        cellcount = CellCountInstance.objects.get(id=1)
        self.assertEqual(119, cellcount.myeloid_cellcount())

    def test_me_ratio(self):
        cellcount = CellCountInstance.objects.get(id=1)
        self.assertEqual(19.833333333333332, cellcount.myeloid_erythroid_ratio())

    def test_me_ratio_erythroids_0(self):
        cellcount = CellCountInstance.objects.get(id=2)
        self.assertEqual('Unable to calculate, erythroid count = 0', cellcount.myeloid_erythroid_ratio())
