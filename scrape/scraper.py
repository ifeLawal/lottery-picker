from typing import List

import requests
from lxml import etree, html


class Scraper:
    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.current_root = ""
        self.parser = etree.XMLParser(remove_blank_text=True)

    def get_data_using_a_request(
        self, endpoint, postPayload, headers={}, request_type="GET"
    ):
        full_url = self.base_url + endpoint
        if request_type == "GET":
            return requests.get(full_url, headers=headers).json()
        elif request_type == "POST":
            return requests.post(full_url, json=postPayload, headers=headers).json()

    def print_simple_page_content(self, endpoint):
        print(etree.tostring(self.get_page(endpoint=endpoint)))

    def print_section_content(self, endpoint, xpath) -> str:
        page = requests.get(self.base_url + endpoint)
        tree = html.fromstring(page.content)
        full_html_text = tree.xpath(xpath + "//descendant::*")
        print(
            "".join(
                [
                    str(etree.tostring(elem, pretty_print=True))
                    for elem in full_html_text
                ]
            )
        )

    def select_section(self, endpoint, xpath, position=0) -> etree:
        if endpoint == "":
            page = requests.get(self.base_url)
        else:
            page = requests.get(self.base_url + endpoint)
        tree = html.fromstring(page.content)
        section = tree.xpath(xpath)[position]
        section_html_string = etree.tostring(section, pretty_print=True)
        section_root = html.fromstring(section_html_string)
        return section_root

    def get_page(self, endpoint) -> etree:
        page = requests.get(self.base_url + endpoint)
        tree = html.fromstring(page.content)
        return tree.xpath("//body")[0]

    def get_website_endpoints_from_page(self, endpoint, inner_tag) -> List[str]:
        page = self.get_page(endpoint=endpoint)
        endpoints = []
        for link in self.get_links_from_root(etree=page, inner_tag=inner_tag):
            if self.base_url in link:
                endpoint_start = len(self.base_url)
                endpoints.append(link[endpoint_start:])
        return endpoints

    def get_links_from_root(self, etree, inner_tag="") -> List[str]:
        return etree.xpath(f"{inner_tag}//@href")

    def get_all_links_from_endpoint(self, endpoint, inner_tag="") -> List[str]:
        page = self.get_page(endpoint=endpoint)
        return page.xpath(f"{inner_tag}//@href")

    def get_page_content(self, endpoint, inner_tag, include_html=False) -> str:
        page = self.get_page(endpoint=endpoint)
        if include_html:
            full_html_text = page.xpath(f"{inner_tag}")
            return bytes.decode(etree.tostring(full_html_text[0]))
        full_html_text = page.xpath(f"{inner_tag}//text()")
        return "".join([str(elem) for elem in full_html_text])

    def select_all_sections(self, endpoint, xpath) -> list:
        page = self.get_page(endpoint=endpoint)
        return page.xpath(f"{xpath}")

    def get_direct_text(self, endpoint, inner_tag) -> str:
        page = self.get_page(endpoint=endpoint)
        print(page.xpath("//mat-tab-body"))
        return page.xpath(f"{inner_tag}/text()")[0]

    def get_direct_text_from_element(self, element, inner_tag) -> str:
        return element.xpath(f"{inner_tag}//text()")[0]
