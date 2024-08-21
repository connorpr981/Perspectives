from typing import Type, TypeVar, Tuple, Union
from anthropic import Anthropic
from openai import OpenAI
import instructor
from pydantic import BaseModel

# Update these imports to use the new models folder
from .models.message_models import Messages
from .models.base_models import AIResponse
from .models import PROVIDER_RESPONSE_MAP

T = TypeVar('T', bound=BaseModel)

class AIProviderClient:
    def __init__(self, provider: str, model: Union[str, None] = None):
        self.provider = provider
        if provider == "anthropic":
            self.client = instructor.from_anthropic(Anthropic())
            self.model_name = model or "claude-3-5-sonnet-20240620"
        elif provider == "openai":
            self.client = instructor.from_openai(OpenAI())
            self.model_name = model or "gpt-4o"
        else:
            raise ValueError(f"Invalid provider: {provider}")

    def get_response(
        self,
        messages: Messages,
        response_model: Type[T],
        max_tokens: int = 4000,
    ) -> Tuple[T, AIResponse]:
        try:
            response, completion = self.client.chat.completions.create_with_completion(
                model=self.model_name,
                max_tokens=max_tokens,
                messages=messages.to_api_format(),
                response_model=response_model,
            )

            wrapper_response = PROVIDER_RESPONSE_MAP[self.provider].from_completion(
                completion, self.provider, self.model_name
            )

            return response, wrapper_response
        except Exception as e:
            # Handle all errors
            raise ValueError(f"Error generating response with {self.provider}: {str(e)}")

def get_response(
    provider: str, 
    messages: Messages,
    response_model: Type[T],
    model: Union[str, None] = None,
    max_tokens: int = 4000,
) -> Tuple[T, AIResponse]:
    if not messages.messages:
        raise ValueError("Messages cannot be empty")
    client = AIProviderClient(provider, model)
    response, wrapper_response = client.get_response(messages, response_model, max_tokens)
    
    # Add the response_model_dump to the wrapper_response
    wrapper_response.response_model_dump = response.model_dump()
    
    return response, wrapper_response