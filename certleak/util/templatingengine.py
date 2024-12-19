import logging
import re
from collections.abc import MutableMapping
from string import Template

from certleak.util import DictWrapper


class TemplatingEngine:
    """Wrapper class around the python templating feature"""

    @staticmethod
    def fill_template(update, analyzer_name, template_string, matches=None, **kwargs):
        """
        Returns a templated text with update contents inserted into the template string
        Use ${key_name} in the template_string to insert update contents into it
        :param update: A update which serves as the source for template filling
        :param analyzer_name: Name of the analyzer
        :param template_string: A template string describing how the variables should be filled in
        :param matches: A list of matches that was returned from the analyzer
        :return: Filled template
        """
        if update is None:
            logging.error("Update is None!")
            return None

        update_dict = update.to_dict()
        update_dict["analyzer_name"] = analyzer_name

        if matches is None:
            update_dict["matches"] = ""
        elif not isinstance(matches, list):
            logging.error("Matches object passed to fill_template is not of type 'list'!")
        else:
            # When there are elements in the matches object, we want them to be formatted as single string
            matches_str = "\n".join(matches)
            update_dict["matches"] = matches_str

        # Possibility to insert own/custom values into the update_dict thus gives more control over the template string
        for name, value in kwargs.items():
            update_dict[name] = value

        # Fallback if the template string is empty or non existent
        if template_string is None or template_string == "":
            template_string = "New update matched by analyzer '${analyzer_name}' - Domains: ${data.leaf_cert.subject.CN}\n\nMatches:\n${matches}"

        template_string = TemplatingEngine._normalize_placeholders(template_string)
        template = Template(template_string)

        flattened_dict = TemplatingEngine._flatten_update_dict(update_dict)

        text = template.safe_substitute(DictWrapper(flattened_dict))
        return text

    @staticmethod
    def _flatten_update_dict(d, parent_key="", sep="__"):
        """
        Flattens and returns any given dict
        :param d: The dictionary to be flattened
        :param parent_key: The key of the parent object
        :param sep: The separator element to separate original keys from each other
        :return:
        """
        # https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
        items = []
        for key, value in d.items():
            new_key = parent_key + sep + key if parent_key else key
            if isinstance(value, MutableMapping):
                items.extend(TemplatingEngine._flatten_update_dict(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)

    @staticmethod
    def _normalize_placeholders(template_string, sep="__"):
        """
        Normalizes placeholders from "dot-form" (data.element1.element2) into the flat dict format (keys joined with "__")
        :param template_string: The original template string to normalize
        :param sep: The separator string
        :return:
        """
        pattern = re.compile(r"(\${[a-zA-Z0-9_.]+})")
        matches = pattern.findall(template_string)
        for placeholder in matches:
            normalized_placeholder = placeholder.replace(".", sep)
            template_string = template_string.replace(placeholder, normalized_placeholder)
        return template_string
