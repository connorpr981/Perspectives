import nltk
from nltk.tokenize import PunktSentenceTokenizer
import re
import os
import json
from typing import List, Dict

# Add this at the beginning of the file, after the imports
nltk.download('punkt', quiet=True)

class TranscriptProcessor:
    def __init__(self, host_name: str = "Dwarkesh Patel"):
        self.host_name = host_name
        self.tokenizer = PunktSentenceTokenizer()

    def process_directory(self, input_dir: str, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in os.listdir(input_dir):
            if filename.endswith('.md'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
                
                with open(input_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                structured_data = self.parse_markdown(content)
                
                with open(output_path, 'w', encoding='utf-8') as file:
                    json.dump(structured_data, file, indent=2, ensure_ascii=False)
                
                print(f"Processed {filename} -> {os.path.basename(output_path)}")

    def parse_markdown(self, content: str) -> List[Dict]:
        entries = re.split(r'\n(?=\*\*.*?\*\*\s+_(.*?)_\n(.*))', content)
        structured_data = []
        turn_index = 0

        for entry in entries:
            match = re.match(r'\*\*(.*?)\*\*\s+_(.*?)_\n(.*)', entry, re.DOTALL)
            if match:
                speaker, timestamp, text = match.groups()
                turn_data = self.process_turn(turn_index, speaker, timestamp, text)
                structured_data.append(turn_data)
                turn_index += 1

        return structured_data

    def process_turn(self, index: int, speaker: str, timestamp: str, text: str) -> Dict:
        role = "Host" if speaker.strip() == self.host_name else "Guest"
        start_time = self.parse_timestamp(timestamp.strip())
        
        sentences = []
        original_sentences = self.tokenize(text)
        content = text.strip()  # Keep the original content with newlines, titles, and links
        
        for i, sent in enumerate(original_sentences):
            sentence = self.process_sentence(sent, i)
            sentences.append(sentence)

        return {
            "index": index,
            "role": role,
            "speaker": speaker.strip(),
            "start_time": start_time,
            "content": content,  # Use the original content
            "sentences": sentences
        }

    @staticmethod
    def parse_timestamp(timestamp: str) -> str:
        return timestamp.strip()

    def tokenize(self, text: str) -> List[str]:
        return self.tokenizer.tokenize(text)

    def process_sentence(self, sentence: str, index: int) -> Dict:
        clean_text = self.clean_sentence(sentence)
        extracted_info = self.extract_information(sentence)  # Use original sentence for extraction
        return {
            'index': index,
            'original_text': sentence,
            'clean_text': clean_text,
            'extracted_information': extracted_info
        }

    @staticmethod
    def clean_sentence(text: str) -> str:
        cleaned = text.strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)
        cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
        return cleaned

    def extract_information(self, sentence: str) -> Dict:
        links = self.extract_links(sentence)
        titles = self.extract_titles(sentence)
        return {
            'links': links,
            'titles': titles
        }

    @staticmethod
    def extract_links(text: str) -> Dict[str, str]:
        links = {}
        def replace_link(match):
            term, url = match.groups()
            links[term] = url
            return term
        re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)
        return links

    @staticmethod
    def extract_titles(text: str) -> List[str]:
        titles = []
        def extract_title(match):
            title = match.group(1)
            titles.append(title)
            return title
        re.sub(r'_([^_]+)_', extract_title, text)
        return titles

if __name__ == "__main__":
    processor = TranscriptProcessor()
    processor.process_directory("sample", "sample_json")