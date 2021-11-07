# -*- coding: utf-8 -*-
import logging

from ..core.processor_class import Processer

logger = logging.getLogger("INCA")


class should_include(Processer):
    def process(self, document_field, **kwargs):
        """Indicate whether the document should be included for further analysis.

        If any of these boolean conditions is True, the document should be excluded.
            - is_missing_text    added by processors in usrightmedia_missing_text_processing.py
            - is_ap_syndicated   Media Cloud indicates that the article is likely AP press copy
            - is_fetch_error     urlExpander failed to retrieve the content for the target URL
            - is_generic_url     urlExpander indicates that the content is likely from a homepage

        Args:
            document_field (str): the value of the "article_maintext_*" key
            extra_fields (list): ["ap_syndicated", "fetch_error", "is_generic_url"]


        Returns:
            should_include (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """

        is_missing_text = document_field

        for k, v in kwargs["extra_fields"].items():
            if k == "ap_syndicated":
                is_ap_syndicated = v
            elif k == "fetch_error":
                is_fetch_error = v
            elif k == "is_generic_url":
                is_generic_url = v

        if any([is_missing_text, is_ap_syndicated, is_fetch_error, is_generic_url]):
            should_include = False
        else:
            should_include = True

        logger.info(f"is_missing_text: {is_missing_text}")
        logger.info(f"is_ap_syndicated: {is_ap_syndicated}")
        logger.info(f"is_fetch_error: {is_fetch_error}")
        logger.info(f"is_generic_url: {is_generic_url}")
        logger.info(f"should_include: {should_include}")

        return should_include
