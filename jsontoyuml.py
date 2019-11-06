# %% 
import json
import requests
import shutil
from collections import Counter
from lxml import html
from yumltoimage import image_from_yuml

with open('pages.json') as fp:
    pages = json.load(fp)

# %%
class yuml_from_json:

    def __init__(self, spider_output):
        self.pages = self.remove_url_begin(spider_output)
        self.attributes_to_show = ['title']

    def remove_url_begin(self, spider_output):
        for page in spider_output:
            page['links'] = [link.split('://www.')[-1] for link in page.get('links')]
            page['url'] = page.get('url','').split('://www.')[-1]
        return pages

    def detailled_pages_yuml(self):
        detailled_pages = []
        for page in self.pages:
            url = str(page.get('url','')) # strip the domain
            attributes = [str(page.get(a,'')) for a in self.attributes_to_show]
            str_class = '[' + url + '|' + ';'.join(attributes) + ']'
            detailled_pages.append(str_class)
        return detailled_pages
    
    def all_links(self):
        urls = set()
        for page in self.pages:
            urls.update(page.get('links',[]))
        return urls

    def associations_yuml(self):
        pages_associations = []
        pages_link_counter = {page.get('url'): Counter(page.get('links',[])) for page in self.pages}
        for page_url, counter_link in pages_link_counter.items():
            for link, count in counter_link.items():
                pages_associations.append('[' + page_url + ']->' + str(count) + '[' + link + ']')
        return ','.join((a for a in pages_associations))
    

#%% test class yuml
YtoJ = yuml_from_json(pages)
associations = YtoJ.associations_yuml()
yuml_pages_with_details = YtoJ.detailled_pages_yuml()
yuml_details_and_associations = ','.join(yuml_pages_with_details) + ',' + associations

#%%
myImage = image_from_yuml(yuml_details_and_associations)
myImage.download_jpg()
myImage.download_svg()
#%%
test_yuml = "[Customer|-forname:string;surname:string|doShiz()]<>-orders*>[Order], [Order]++-0..*>[LineItem], [Order]-[note:Aggregate root]"


# %%
page_attributes = ['body_length','title']
def yuml_class_with_details(page, attributes=page_attributes):
    url = str(page.get('url','')) # strip the domain
    attibutes = [str(page.get(a,'')) for a in attributes]
    str_class = '[' + url + '|' + ';'.join(attibutes) + ']'
    return str_class
    
#print(pages[0])
page = YtoJ.pages[0]
str_class = yuml_class_with_details(page)
print(str_class)


# %%    
def get_image_yUML(yuml):
    yuml_url = "https://yuml.me/diagram/class/"
    image_url = yuml_url + yuml.replace('?','') + ",[https://www.carisiolas.com/contact/]-[https://www.carisiolas.com/]"
    print(image_url)
    resp = requests.get(image_url, stream=True)
    local_file = open('local_image.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp

get_image_yUML(test_yuml)

#%% get svg
def get_svg_yUML(yuml):
    yuml_url = "https://yuml.me/diagram/class/"
    image_url = yuml_url + yuml.replace('?','') + ",[https://www.carisiolas.com/contact/]-[https://www.carisiolas.com/]"    
    response = requests.get(image_url, stream=True)
    response.raw.decode_content = True
    tree = html.parse(response.raw)
    svg = tree.xpath('//svg')
    print(svg)
    if svg:
        svg_text = html.tostring(svg[0])
        with open("image_svg.svg","wb") as fp:
            fp.write(svg_text)

get_svg_yUML(test_yuml)
# %%
yuml_pages_with_details = ','.join([yuml_class_with_details(page) for page in pages])
yuml_pages_with_details