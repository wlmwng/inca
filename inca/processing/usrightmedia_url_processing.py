# -*- coding: utf-8 -*-
import logging
import urlexpander

from ..core.processor_class import Processer

logger = logging.getLogger("INCA")


class standardize_url(Processer):
    """standardize a URL"""

    def process(self, document_field, **kwargs):
        """standardize a URL

        Args:
            document_field (str): the URL scraped from the server

        Returns:
            standardized_url (str): the URL standardized by urlExpander

        """

        standardized_url = urlexpander.url_utils.standardize_url(
            url=document_field,
            remove_scheme=True,
            replace_netloc_with_domain=False,
            remove_path=False,
            remove_query=False,
            remove_fragment=True,
            to_lowercase=True,
        )

        return standardized_url
