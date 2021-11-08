# -*- coding: utf-8 -*-
import logging
import urlexpander

from ..core.database import client, elastic_index
from ..core.processor_class import Processer

logger = logging.getLogger("INCA")


class match_outlet_articles_to_tweets2_urls(Processer):
    """list of IDs: match the standardized URL from an outlet's document to the standardized URL from (re-)tweeted URL documents"""

    def process(self, document_field, **kwargs):
        """Find the IDs of tweet2_url documents which match an outlet's URL.
        Only documents from outlets should use this processor.

        Args:
            document_field (str): value of "standardized_url_2" key; outlet URL to find matches for among (re-)tweeted URL docs.
                                  "standardized_url_2" used the public fork of urlExpander.
                                  "standardized_url" used a dev version of urlExpander which is outdated.

        Returns:
            matched_ids (list): [] or [matched_id_1, matched_id_2, ... ]; stored in new_key "tweets2_url_ids"


            example ID = "1270090263629791237_0"; the "0" means that the matched URL is the first (zero-indexed) URL
            shared in the (re-)tweet which has tweet_id="1270090263629791237"

            "Any field can contain zero or more values by default, however, all values in the array must be of the same datatype."
            https://www.elastic.co/guide/en/elasticsearch/reference/6.8/array.html

            If no matches are found, an empty array is stored by Elasticsearch.
            "A null value cannot be indexed or searched. When a field is set to null,
            (or an empty array or an array of null values) it is treated as though that field has no values."
            https://www.elastic.co/guide/en/elasticsearch/reference/6.8/null-value.html

        Query:
            "_source": fields to return
            "size": max number of matched documents
                - default is 10, max is 10000
                - https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-from-size.html
            "query": match documents which are of the "tweets2_url" doctype and which exactly match the url


        """
        url_to_match = document_field
        logger.info(f"url to match: {url_to_match}")

        search_param = {
            "_source": ["_id", "standardized_url_2"],
            "size": 10000,
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"doctype": "tweets2_url"}},
                        {"term": {"standardized_url_2.keyword": url_to_match}},
                    ]
                }
            },
        }

        res = client.search(index=elastic_index, body=search_param)
        hits = res["hits"]["hits"]
        matched_ids = [d["_id"] for d in hits]
        logger.info(f"matched_ids: {matched_ids}")
        return matched_ids


class match_outlet_articles_to_tweets2_urls_count(Processer):
    """Count of tweets2_url documents which match the outlet document."""

    def process(self, document_field, **kwargs):
        """Count of tweets2_url documents which match the outlet document.
        Only documents from outlets should use this processor.
        It should be run after the 'match_outlet_articles_to_tweets2_urls' processor.

        Args:
            document_field (str): value of "tweets2_url_ids" key

        Returns:
            matched_ind (int): number of matches

        """
        matched_ids = document_field
        matched_count = len(matched_ids)
        logger.info(f"matched_ids: {matched_ids}, matched_count: {matched_count}")
        return matched_count


class match_outlet_articles_to_tweets2_urls_ind(Processer):
    """Indicate if outlet document matches 1+ tweets2_url documents."""

    def process(self, document_field, **kwargs):
        """Boolean indicator if outlet document matches 1+ tweets2_url documents.
        Only documents from outlets should use this processor.
        It should be run after the 'match_outlet_articles_to_tweets2_urls' processor.

        Args:
            document_field (str): value of "tweets2_url_ids" key

        Returns:
            matched_ind (bool): True if 1+ matches, False if 0 matches.

        """
        matched_ids = document_field
        matched_ind = True if len(matched_ids) > 0 else False
        logger.info(f"matched_ids: {matched_ids}, matched_ind: {matched_ind}")
        return matched_ind
