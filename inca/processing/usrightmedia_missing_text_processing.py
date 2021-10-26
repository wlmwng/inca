# -*- coding: utf-8 -*-
import logging
from datetime import datetime
import re

from ..core.basic_utils import dotkeys
from ..core.processor_class import Processer

logger = logging.getLogger("INCA")


class missing_text_americanrenaissance(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_generic = any(
            [
                text
                == "AmRen is America's foremost white advocacy publication. To keep up with our latest, follow us on Telegram Gab , and BitChute",
                text
                == "These content recommendations are provided by AdStyle and may be paid by the advertiser whose ad you clicked on. Ad.Style recognizes interest based on how you and other visitors interact with content suggestions.",
            ]
        )

        # evaluate the conditions
        missing_ind = any([text_is_empty, text_is_generic])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_generic: {text_is_generic}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_breitbart(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False

        # evaluate the conditions
        missing_ind = any([text_is_empty])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_dailycaller(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False

        # evaluate the conditions
        missing_ind = any([text_is_empty])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_dailystormer(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_generic = any(
            [
                text
                == "We here at the Daily Stormer are opposed to violence. We seek revolution through the education of the masses. When the information is available to the people, systemic change will be inevitable and unavoidable.\nAnyone suggesting or promoting violence in the comments section will be immediately banned, permanently."
            ]
        )

        # evaluate the conditions
        missing_ind = any([text_is_empty, text_is_generic])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_generic: {text_is_generic}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_foxnews(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_generic = any(
            [
                text
                == "By using this site, you agree to our Privacy Policy and our Terms of Use",
                text
                == "This material may not be published, broadcast, rewritten, or redistributed. ©2021 FOX News Network, LLC. All rights reserved. Quotes displayed in real-time or delayed by at least 15 minutes. Market data provided by Factset. Powered and implemented by FactSet Digital Solutions. Legal Statement. Mutual Fund and ETF data provided by Refinitiv Lipper.",
            ]
        )

        # evaluate the conditions
        missing_ind = any([text_is_empty, text_is_generic])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_generic: {text_is_generic}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_gatewaypundit(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_generic = any(
            [
                text
                == "The page you are looking for no longer exists. Perhaps you can return back to the site's homepage and see if you can find what you are looking for. Or, you can try finding it with the information below."
            ]
        )

        # evaluate the conditions
        missing_ind = any([text_is_empty, text_is_generic])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_generic: {text_is_generic}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_infowars(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_generic = any(
            [
                text
                == "Keep up to date with our latest:\nHave an important tip? Let us know. Email us here."
            ]
        )

        # evaluate the conditions
        missing_ind = any([text_is_empty, text_is_generic])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_generic: {text_is_generic}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_newsmax(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(text) == 0 else False

        # evaluate the conditions
        missing_ind = any([text_is_empty])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_oneamericanews(Processer):
    def is_likely_unrelated_preview(text):  # redirects
        is_short = len(text) < 200
        is_preview = True if text.find("\nRead More") != -1 else False
        if is_short and is_preview:
            ind = True
        else:
            ind = False
        return ind

    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_generic = any(
            [
                text
                == "It seems we can’t find what you’re looking for. Perhaps searching can help.\nSearch for:",
                text
                == "We use cookies and other tracking technologies to improve your browsing experience on our website, to show you personalized content and targeted ads, to analyze our website traffic, and to understand where our visitors are coming from.",
            ]
        )
        text_is_likely_unrelated_preview = self.is_likely_unrelated_preview(text)

        # evaluate the conditions
        missing_ind = any(
            [text_is_empty, text_is_generic, text_is_likely_unrelated_preview]
        )
        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_generic: {text_is_generic}")
        logger.debug(
            f"text_is_likely_unrelated_preview: {text_is_likely_unrelated_preview}"
        )
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_rushlimbaugh(Processer):
    def is_date_only(text):
        try:
            datetime.strptime(text, "%b %d, %Y")
            ind = True
        except:
            ind = False
        return ind

    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False
        text_is_date_only = self.is_date_only(text)

        # evaluate the conditions
        missing_ind = any([text_is_empty, text_is_date_only])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"text_is_date_only: {text_is_date_only}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_seanhannity(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False

        # evaluate the conditions
        missing_ind = any([text_is_empty])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_vdare(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False

        # evaluate the conditions
        missing_ind = any([text_is_empty])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind


class missing_text_washingtonexaminer(Processer):
    def process(self, document_field):
        """Check if the the scraped text is missing.

        This indicator is used as a filter before further analysis.

        Args:
            document_field (str):
                - this argument should be the value of the "article_maintext" key

        Returns:
            missing_ind (bool):
                - this indicator should be written to the same new_key for all outlets' documents

        """
        text = document_field

        # strip out ASCII/Unicode whitespaces
        stripped_text = re.sub(r"\s+", "", text)

        # conditions for marking indicator as true
        text_is_empty = True if len(stripped_text) == 0 else False

        # evaluate the conditions
        missing_ind = any([text_is_empty])

        logger.debug(f"text_is_empty: {text_is_empty}")
        logger.debug(f"missing_ind: {missing_ind}")

        return missing_ind
