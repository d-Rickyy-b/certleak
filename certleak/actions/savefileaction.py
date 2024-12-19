import pathlib

from certleak.util import TemplatingEngine

from .basicaction import BasicAction


class SaveFileAction(BasicAction):
    """Action to save each certificate update as a file named '<update.cert_index>.txt'."""

    name = "SaveFileAction"

    def __init__(self, path, file_ending=".txt", template=None):
        """Action to save each update as a file named '<update.cert_index>.txt'.

        If you want to store metadata within the file, use template strings (https://github.com/d-Rickyy-b/certleak/wiki/Templating-in-actions).

        :param path: The directory in which the file(s) should be stored
        :param template: A template string describing how the update variables should be filled in
        """
        super().__init__()
        self.path = pathlib.Path(path)
        self.file_ending = file_ending
        self.template = template or "${data}"

    @staticmethod
    def _remove_prefix(input_string, prefix):
        """Remove a prefix from a certain string (e.g. remove '.' as prefix from '.txt')."""
        if input_string.startswith(prefix):
            return input_string[len(prefix) :]
        return input_string

    def get_file_content(self, update, analyzer_name, matches):
        """Return the content to be written to the file."""
        return TemplatingEngine.fill_template(update, analyzer_name, template_string=self.template, matches=matches)

    def perform(self, update, analyzer_name=None, matches=None):
        """Store the update as a file.

        :param update: The cert update passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the update
        :param matches: List of matches returned by the analyzer
        :return: None
        """
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)

        self.file_ending = self._remove_prefix(self.file_ending, ".")

        file_name = str(update.cert_index) if self.file_ending == "" else f"{update.cert_index}.{self.file_ending}"

        file_path = self.path / file_name
        content = self.get_file_content(update, analyzer_name, matches)

        self.logger.debug("Writing file at '%s'", file_path)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
