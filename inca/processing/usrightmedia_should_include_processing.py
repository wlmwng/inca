# -*- coding: utf-8 -*-
import logging
import re
from ..core.processor_class import Processer

logger = logging.getLogger("INCA")


class is_true_ind(Processer):
    def process(self, document_field, **kwargs):
        """Set the new_key value to True.

        Args:
            document_field (str): not used

        Returns:
            True

        """
        return True


class is_false_ind(Processer):
    def process(self, document_field, **kwargs):
        """Set the new_key value to False.

        Args:
            document_field (str): not used

        Returns:
            False

        """
        return False


class is_empty_text(Processer):
    def process(self, document_field, **kwargs):
        """Check if the text field is empty.

        Args:
            document_field (str)

        Returns:
            is_empty_text (bool)

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)
        is_empty_text = True if len(stripped_text) == 0 else False
        logger.debug(f"is_empty_text: {is_empty_text}")
        return is_empty_text


class should_include(Processer):
    def process(self, document_field, **kwargs):
        """Indicate whether the document should be included for further analysis.

        If any of these boolean conditions is True, the document should be excluded.
            - is_ap_syndicated          Media Cloud indicates that the article is likely AP press copy
            - is_fetch_error            urlExpander failed to retrieve the content for the target URL
            - is_generic_url            urlExpander indicates that the content is likely from a homepage
            - is_empty_text             the text is an empty string
            - is_valid_dupe_text        the text is a duplicate of an older article by the same outlet
            - is_generic_dupe_text      the text is likely generic boilerplate text
            - is_misc_dupe_text         the text is a duplicate, but it's uncertain if it's a "valid" or "generic" dupe

        Args:
            document_field (str): dummy field (not used by the processor)
            extra_fields (list): ["ap_syndicated",
                                  "fetch_error",
                                  "is_generic_url",
                                  "article_maintext_4_is_empty",
                                  "article_maintext_4_is_valid_dupe",
                                  "article_maintext_4_is_generic_dupe"
                                  "article_maintext_4_is_misc_dupe",
                                  ]

        Returns:
            should_include (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """

        for k, v in kwargs["extra_fields"].items():
            if k == "ap_syndicated":
                is_ap_syndicated = v
            elif k == "fetch_error":
                is_fetch_error = v
            elif k == "is_generic_url":
                is_generic_url = v
            elif k == "article_maintext_4_is_empty":
                is_empty_text = v
            elif k == "article_maintext_4_is_valid_dupe":
                is_valid_dupe_text = v
            elif k == "article_maintext_4_is_generic_dupe":
                is_generic_dupe_text = v
            elif k == "article_maintext_4_is_misc_dupe":
                is_misc_dupe_text = v

        if any(
            [
                is_ap_syndicated,
                is_fetch_error,
                is_generic_url,
                is_empty_text,
                is_valid_dupe_text,
                is_generic_dupe_text,
                is_misc_dupe_text,
            ]
        ):
            should_include = False
        else:
            should_include = True

        logger.info(f"is_ap_syndicated: {is_ap_syndicated}")
        logger.info(f"is_fetch_error: {is_fetch_error}")
        logger.info(f"is_generic_url: {is_generic_url}")
        logger.info(f"is_empty_text: {is_empty_text}")
        logger.info(f"is_valid_dupe_text: {is_valid_dupe_text}")
        logger.info(f"is_generic_dupe_text: {is_generic_dupe_text}")
        logger.info(f"is_misc_dupe_text: {is_misc_dupe_text}")
        logger.info(f"should_include: {should_include}")

        return should_include
