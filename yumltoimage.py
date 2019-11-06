#TODO push to github

import requests
import shutil
from lxml import html
import xml.etree.ElementTree as ET


# %% class for downloads:
class image_from_yuml():
    root = "http://yuml.me/"

    def __init__(self, yuml_str, scruffy=False):
        self.ommited = 0
        self.yuml = yuml_str
        self._scruffy = scruffy
        self._root_url = None
        self._short_code = None

    def __str__(self):
        att = {
            'yuml': self._yuml,
            'root': self._root_url,
            'code': self._short_code
        }
        return str(att)

    @property
    def yuml(self):
        return self._yuml

    @yuml.setter
    def yuml(self, yuml_str):
        newyuml = yuml_str.replace('?', '')
        while len(newyuml) > 2000:
            newyuml = ','.join(newyuml.split(",")[:-1])
            self.ommited += 1
        self._yuml = newyuml


    # @property
    # def short_code(self):
    #     if not self._short_code:
    #         response = requests.post(self.root_url + self.yuml)
    #         short_code = response.text.split('.')[0]
    #         self._short_code = short_code
    #     return self._short_code

    @property
    def short_code(self):
        if not self._short_code:
            print(self.root_url)
            session = requests.Session()
            # response = session.get(self.root_url + '[dummy]')
            # print(response)
            response = session.post(self.root_url, params={'dsl_text':'[test].png'})
            short_code = response.text.split('.')[0]
            self._short_code = short_code
        return self._short_code

    @property
    def root_url(self):
        if not self._root_url:
            self._root_url = self.root + "diagram/class/"
            if self._scruffy:
                self._root_url = self.root + "diagram/scruffy/class/"
        return self._root_url

    def download_jpg(self):
        image_url = self.root + self.short_code + '.jpg'
        resp = requests.get(image_url, stream=True)
        local_file = open('local_image.jpg', 'wb')
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, local_file)
        del resp

    def download_svg(self):
        image_url = self.root + self.short_code + '.svg'
        response = requests.get(image_url, stream=True)
        response.raw.decode_content = True
        tree = html.parse(response.raw)
        svg = tree.xpath('//svg')
        if svg:
            svg_text = html.tostring(svg[0])
            with open("image_svg.svg", "wb") as fp:
                fp.write(svg_text)
        else:
            print('no svg image at adress: ' + image_url)


# %%
if __name__ == "__main__":
    myImage = image_from_yuml(
        "[helloèw], [https://www.carisiolas.com/contact/]-[https://www.carisiolas.com/]")
    print(myImage.__str__())
    myImage.root_url
    print(myImage.__str__())
    myImage.short_code
    print(myImage.__str__())
    # myImage.download_svg()
    # print(myImage.__str__())


# %%
