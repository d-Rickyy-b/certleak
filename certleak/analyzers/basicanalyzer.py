import logging

from certleak.actions import BasicAction
from certleak.errors import InvalidActionError
from certleak.util import listify


class BasicAnalyzer:
    """Basic analyzer class."""

    name = "BasicAnalyzer"

    def __init__(self, actions, identifier=None):
        """Basic analyzer which is extended to create other analyzer subclasses.

        :param actions: A single action or a list of actions to be executed on every update
        :param identifier: The name or unique identifier for this specific analyzer.
        """
        self.logger = logging.getLogger(__name__)
        self.actions = listify(actions)
        self.identifier = identifier or self.name

        # Check if passed action is an instance of an analyzer and not a class
        # Raises an error if any action is not an object inheriting from BasicAaction
        for action in self.actions:
            self._check_action(action)

    def add_action(self, action):
        """Add a new action to the already present actions.

        :param action: New action to add to the present actions
        :return: None
        """
        self._check_action(action)
        self.actions.append(action)

    def match(self, update):
        """Check if a certain update is matched by the conditions set for this analyzer.

        :param update: A :class:`certleak.core.certstreamdata.update` object which should be matched
        :return: :obj:`bool` if the update has been matched
        """
        msg = "Your analyzer must implement the match method!"
        raise NotImplementedError(msg)

    def _check_action(self, action):
        """Check if a passed action is a subclass of BasicAction."""
        if not isinstance(action, BasicAction):
            if isinstance(action, type):
                error_msg = f"You passed a class as action for '{self.identifier}' but an instance of an action was expected!"
            else:
                error_msg = f"You did not pass an action object - inheriting from BasicAction - to '{self.identifier}'"

            self.logger.error(error_msg)
            raise InvalidActionError(error_msg)

    def __and__(self, other):
        """Return a new analyzer which is the logical AND of the current one and another one."""
        return MergedAnalyzer(self, and_analyzer=other)

    def __or__(self, other):
        """Return a new analyzer which is the logical OR of the current one and another one."""
        return MergedAnalyzer(self, or_analyzer=other)

    def __invert__(self):
        """Return a new analyzer which is the negation of the current one."""
        return MergedAnalyzer(base_analyzer=None, not_analyzer=self)

    def __repr__(self):
        """Return a string representation of the analyzer."""
        if self.identifier is None:
            self.identifier = self.__class__.__name__
        return self.identifier


class MergedAnalyzer(BasicAnalyzer):
    """Merged analyzer class."""

    name = "MergedAnalyzer"

    def __init__(self, base_analyzer, and_analyzer=None, or_analyzer=None, not_analyzer=None):
        self._base_analyzer = base_analyzer
        self._and_analyzer = and_analyzer
        self._or_analyzer = or_analyzer
        self._not_analyzer = not_analyzer

        if self._and_analyzer:
            actions = base_analyzer.actions + self._and_analyzer.actions
            identifier = f"({base_analyzer.identifier} && {self._and_analyzer})"
        elif self._or_analyzer:
            actions = base_analyzer.actions + self._or_analyzer.actions
            identifier = f"({base_analyzer.identifier} || {self._or_analyzer})"
        elif self._not_analyzer:
            actions = self._not_analyzer.actions
            identifier = f"~({self._not_analyzer})"
        else:
            msg = "Neither and_analyzer, or_analyzer nor not_analyzer are set!"
            raise ValueError(msg)

        super().__init__(actions, identifier=identifier)

    def match(self, update):
        """Checks if a certain update is matched by the conditions set for this analyzer.

        :param update: A :class:`certleak.core.certstreamdata.update` object which should be matched
        :return: :obj:`bool` if the update has been matched
        """
        if self._and_analyzer:
            return bool(self._base_analyzer.match(update)) and bool(self._and_analyzer.match(update))
        elif self._or_analyzer:
            return bool(self._base_analyzer.match(update)) or bool(self._or_analyzer.match(update))
        elif self._not_analyzer:
            return not bool(self._not_analyzer.match(update))

        return False
