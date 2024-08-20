from typing import List, Literal, Dict
from pydantic import BaseModel
import textwrap

RoleLiteral = Literal["user", "assistant", "system"]

class Message(BaseModel):
    """Represents a single message in a conversation."""
    role: RoleLiteral
    content: str

    def __str__(self):
        return f"[{self.role.upper()}]\n{textwrap.indent(self.content, '  ')}"

class Messages(BaseModel):
    """Represents a collection of messages in a conversation."""
    messages: List[Message] = []

    def add_message(self, role: RoleLiteral, content: str) -> 'Messages':
        if role == "system":
            self.messages = [msg for msg in self.messages if msg.role != "system"]
            self.messages.insert(0, Message(role=role, content=content))
        else:
            self.messages.append(Message(role=role, content=content))
        return self

    def add_user_message(self, content: str) -> 'Messages':
        return self.add_message("user", content)

    def add_assistant_message(self, content: str) -> 'Messages':
        return self.add_message("assistant", content)

    def add_system_message(self, content: str) -> 'Messages':
        return self.add_message("system", content)

    def clear(self) -> 'Messages':
        self.messages.clear()
        return self

    def to_api_format(self) -> List[Dict[str, str]]:
        return [msg.model_dump() for msg in self.messages]

    def __str__(self):
        if not self.messages:
            return "Messages: Empty"
        return "Messages:\n" + "\n".join(f"  {i+1}. {textwrap.indent(str(msg), '     ').strip()}" 
                                         for i, msg in enumerate(self.messages))