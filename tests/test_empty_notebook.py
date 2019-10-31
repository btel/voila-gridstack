import os
import pytest
from conftest import BASE_DIR
from lxml import etree

@pytest.fixture
def voila_args():
    nb_path = os.path.join(BASE_DIR, 'nb_without_metadata.ipynb')
    return [nb_path, '--VoilaTest.config_file_paths=[]']

@pytest.mark.gen_test
def test_render_without_metadata(http_client, base_url):

    response = yield http_client.fetch(base_url)
    assert response.code == 200
    html_body = response.body.decode('utf-8')

    parser = etree.HTMLParser()
    tree = etree.fromstring(html_body, parser=parser)

    elem = tree.xpath("//pre[text()='Hi !\n']")
    assert elem

    elem = tree.xpath("//*[text()='This is a hidden cell.']")
    assert elem

    elem = tree.xpath("//pre[text()='2']")
    assert elem

    elem = tree.xpath("//h1[text()='This is markdown']")
    assert elem

    # check if the document is properly ended
    assert "</html>" in html_body
    assert False