import pytest
import os
from datetime import datetime
from pydantic import BaseModel
from .llm_processing import get_response
from .models.message_models import Messages
from .models.base_models import BaseResponseMetadata, AIResponse
from typing import List
from hypothesis import given, strategies as st
from dotenv import load_dotenv

load_dotenv()

# Pydantic models for testing
class User(BaseModel):
    name: str
    age: int

class UserList(BaseModel):
    users: List[User]

class WeatherInfo(BaseModel):
    temperature: float
    conditions: str

class BookRecommendation(BaseModel):
    title: str
    author: str
    genre: str
    
# Fixtures
@pytest.fixture(scope="module")
def api_keys():
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    cohere_key = os.getenv("COHERE_API_KEY")
    assert anthropic_key is not None, "ANTHROPIC_API_KEY is not set"
    assert openai_key is not None, "OPENAI_API_KEY is not set"
    assert cohere_key is not None, "COHERE_API_KEY is not set"
    return {"anthropic": anthropic_key, "openai": openai_key, "cohere": cohere_key}

@pytest.fixture(scope="module")
def messages():
    return Messages()

# Tests
def test_messages(messages):
    messages.add_user_message("Hello, AI!")
    messages.add_assistant_message("Hello, human!")
    messages.add_system_message("This is a test conversation.")

    assert len(messages.messages) == 3
    assert messages.messages[0].role == "system"
    assert messages.messages[1].role == "user"
    assert messages.messages[2].role == "assistant"

    messages.add_system_message("This is an updated system message.")
    assert len(messages.messages) == 3
    assert messages.messages[0].role == "system"
    assert messages.messages[0].content == "This is an updated system message."

    api_format = messages.to_api_format()
    assert len(api_format) == 3
    assert isinstance(api_format[0], dict)
    assert api_format[0]['role'] == "system"
    assert api_format[0]['content'] == "This is an updated system message."

    messages.clear()
    assert len(messages.messages) == 0

@pytest.mark.parametrize("provider", ["anthropic", "openai", "cohere"])
def test_ai_response(messages, provider):
    # Test 1: User information extraction
    messages.add_user_message("Extract the following: Jason is 25 years old.")
    response, wrapper = get_response(provider, messages, User)
    assert isinstance(response, User)
    assert response.name == "Jason"
    assert response.age == 25

    # Test 2: Weather information extraction
    messages.clear()
    messages.add_user_message("What's the weather like in New York? Temperature is 72.5°F and it's sunny.")
    response, wrapper = get_response(provider, messages, WeatherInfo)
    assert isinstance(response, WeatherInfo)
    assert isinstance(response.temperature, float)
    assert isinstance(response.conditions, str)

    # Test 3: Book recommendation
    messages.clear()
    messages.add_user_message("Recommend a science fiction book.")
    response, wrapper = get_response(provider, messages, BookRecommendation)
    assert isinstance(response, BookRecommendation)
    assert response.title
    assert response.author
    assert response.genre.lower() == "science fiction"

    # Add assertions for new metadata fields
    assert isinstance(wrapper.created_at, datetime)
    assert wrapper.total_tokens > 0
    assert wrapper.prompt_tokens > 0
    assert wrapper.completion_tokens > 0
    assert wrapper.provider == provider
    assert wrapper.model

def test_extract_metadata(messages):
    messages.clear()
    messages.add_user_message("This is a test message.")
    _, wrapper = get_response("anthropic", messages, User)
    
    metadata = AIResponse.extract_metadata(wrapper)
    assert isinstance(metadata, BaseResponseMetadata)
    assert metadata.provider == wrapper.provider
    assert metadata.model == wrapper.model
    assert metadata.created_at == wrapper.created_at
    assert metadata.total_tokens == wrapper.total_tokens
    assert metadata.prompt_tokens == wrapper.prompt_tokens
    assert metadata.completion_tokens == wrapper.completion_tokens

def test_extract_multiple_users(messages):
    # Approach 1: Multiple users in a single message
    messages.clear()
    messages.add_user_message("Extract the following users: Alice is 30 years old, Bob is 25 years old, and Charlie is 35 years old.")
    response, _ = get_response("anthropic", messages, UserList)
    
    assert isinstance(response, UserList)
    assert len(response.users) == 3
    assert all(isinstance(user, User) for user in response.users)
    
    names = [user.name for user in response.users]
    ages = [user.age for user in response.users]
    assert set(names) == {"Alice", "Bob", "Charlie"}
    assert set(ages) == {30, 25, 35}

    # Approach 2: Extract users over multiple messages
    messages.clear()
    messages.add_system_message("You are a helpful assistant that extracts user information one at a time.")
    user_data = [
        "Alice is 30 years old",
        "Bob is 25 years old",
        "Charlie is 35 years old"
    ]
    extracted_users = []

    for user_info in user_data:
        messages.add_user_message(f"Extract the following user: {user_info}")
        response, wrapper = get_response("anthropic", messages, User)
        
        assert isinstance(response, User)
        extracted_users.append(response)
        messages.add_assistant_message(wrapper.get_message_content())

    assert len(extracted_users) == 3
    names = [user.name for user in extracted_users]
    ages = [user.age for user in extracted_users]
    assert set(names) == {"Alice", "Bob", "Charlie"}
    assert set(ages) == {30, 25, 35}

@given(st.lists(st.tuples(
    st.sampled_from(["user", "assistant", "system"]),
    st.text(min_size=1, max_size=100)
), min_size=1, max_size=50))
def test_messages_consolidation(message_data):
    messages = Messages()
    expected_messages = []
    system_message = None
    for role, content in message_data:
        if role == "user":
            messages.add_user_message(content)
            expected_messages.append({"role": "user", "content": content})
        elif role == "assistant":
            messages.add_assistant_message(content)
            expected_messages.append({"role": "assistant", "content": content})
        else:  # system
            messages.add_system_message(content)
            system_message = {"role": "system", "content": content}
    
    if system_message:
        expected_messages.insert(0, system_message)
    
    api_format = messages.to_api_format()
    assert len(api_format) == len(expected_messages)
    for i, msg in enumerate(api_format):
        assert msg['role'] == expected_messages[i]['role']
        assert msg['content'] == expected_messages[i]['content']

def test_large_message_performance():
    large_message = "This is a very long message. " * 1000
    messages = Messages()
    
    import time
    start_time = time.time()
    messages.add_user_message(large_message)
    end_time = time.time()
    
    assert len(messages.messages) == 1
    assert end_time - start_time < 1  # Assuming it should process within 1 second

@pytest.mark.parametrize("provider", ["anthropic", "openai", "cohere"])
def test_error_handling(messages, provider):
    # Test with invalid API key
    with pytest.raises(Exception):  # Replace with specific exception if known
        invalid_keys = {provider: "invalid_key"}
        get_response(provider, messages, User, api_keys=invalid_keys)
    
    # Test with empty messages
    empty_messages = Messages()
    with pytest.raises(ValueError, match="Messages cannot be empty"):
        get_response(provider, empty_messages, User)
    
    # Test with invalid model type
    with pytest.raises(Exception):  # Replace with specific exception if known
        get_response(provider, messages, int)  # Using 'int' as an invalid model type

@pytest.mark.parametrize("provider", ["anthropic", "openai", "cohere"])
def test_cross_provider_consistency(messages, provider):
    messages.clear()
    messages.add_user_message("What is the capital of France?")
    
    class CapitalInfo(BaseModel):
        country: str
        capital: str

    response, _ = get_response(provider, messages, CapitalInfo)
    
    assert response.country.lower() == "france"
    assert response.capital.lower() == "paris"

def test_complex_nested_models(messages):
    messages.clear()
    messages.add_user_message("Provide information about a space mission with a crew of 3 astronauts.")
    
    class Astronaut(BaseModel):
        name: str
        age: int
        specialty: str

    class Spacecraft(BaseModel):
        name: str
        type: str
        crew_capacity: int

    class SpaceMission(BaseModel):
        mission_name: str
        duration_days: int
        crew: List[Astronaut]
        spacecraft: Spacecraft

    response, _ = get_response("anthropic", messages, SpaceMission)
    
    assert isinstance(response, SpaceMission)
    assert len(response.crew) == 3
    assert all(isinstance(astronaut, Astronaut) for astronaut in response.crew)
    assert isinstance(response.spacecraft, Spacecraft)

def test_metadata_extraction(messages):
    messages.clear()
    messages.add_user_message("Extract metadata from this response.")
    _, wrapper = get_response("anthropic", messages, User)
    
    metadata = AIResponse.extract_metadata(wrapper)
    assert isinstance(metadata, BaseResponseMetadata)
    assert metadata.provider == wrapper.provider
    assert metadata.model == wrapper.model
    assert abs((metadata.created_at - wrapper.created_at).total_seconds()) < 1  # Allow 1 second difference
    assert metadata.total_tokens == wrapper.total_tokens
    assert metadata.prompt_tokens == wrapper.prompt_tokens
    assert metadata.completion_tokens == wrapper.completion_tokens

def test_cohere_specific_functionality(messages):
    messages.clear()
    messages.add_user_message("Extract the following: Jason is 25 years old.")
    response, wrapper = get_response("cohere", messages, User)
    
    assert isinstance(response, User)
    assert response.name == "Jason"
    assert response.age == 25
    assert wrapper.provider == "cohere"
    assert wrapper.model.startswith("command")  # Assuming the default model is used