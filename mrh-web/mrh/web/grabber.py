# -*- coding: utf-8 -*-

import yaml
from selenium.webdriver.common.by import By

from . import Mrh


class Grabber(Mrh):
    
    FORBIDDEN_FIELDS = [
        'CSPToken',
        'CSPHD',
        'sessaoId',
    ]

    def get_fields(self):
        fields = []
        for tag in ['input', 'select']:
            for el in self.driver.find_elements(By.TAG_NAME, tag):
                attrs = dict(tag=tag)
                for attr in ['type', 'id', 'name', 'class', 'value']:
                    attrs[attr] = el.get_attribute(attr)
                attrs['text'] = el.text
                field = dict(tipo=el.tag_name, attrs=attrs)
                if not (attrs.get('id', '') in self.FORBIDDEN_FIELDS or attrs.get('name', '') in self.FORBIDDEN_FIELDS):
                    fields.append(field)
        return fields

    def graball(self, usuario, senha):

        self.login(usuario=usuario, senha=senha)
        for go_page in ('go_resumo_geral', 'go_rubricas_calculadas'):
            func = getattr(self, go_page)
            func()
            fields = self.get_fields()
            print(yaml.dump({'page': go_page, 'fields': fields}))

if __name__ == '__main__':
    import os
    g = Grabber()
    g.graball(os.getenv('MRH_USUARIO'), os.getenv('MRH_SENHA'))
    g.close()
