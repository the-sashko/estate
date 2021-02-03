import re

from typing import Union

class Content:
    def getSubstrings(self, text: str, pattern: str) -> Union[list, None]:
        substring = None
        pattern   = re.compile(pattern)

        entries = pattern.findall(text)

        if len(entries) < 1:
            return None

        return list(set(entries))

    def getSubstring(self, text: str, pattern: str) -> Union[str, None]:
        substring = self.getSubstrings(text, pattern)

        if not substring is None:
            substring = list(substring).pop(0)

        return substring
