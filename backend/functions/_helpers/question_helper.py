from typing import Any, Dict, List, Callable
from firebase_admin import firestore
import logging
import traceback
from _utils.firestore_utils import get_firestore_client
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_turn_in_sections(transcript_id: str, turn_index: int) -> tuple[firestore.DocumentReference, firestore.DocumentReference]:
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    sections = transcript_ref.collection('sections').stream()
    
    logging.info(f"Searching for turn with index {turn_index} in transcript {transcript_id}")
    
    for section in sections:
        section_data = section.to_dict()
        start_turn = section_data.get('start_turn', 0)
        end_turn = section_data.get('end_turn', 0)
        
        if start_turn <= turn_index <= end_turn:
            logging.info(f"Turn index {turn_index} falls within section {section.id} (Start: {start_turn}, End: {end_turn})")
            turns = section.reference.collection('turns').where('index', '==', turn_index).limit(1).stream()
            turn = next(turns, None)
            if turn:
                logging.info(f"Found turn {turn.id} with index {turn_index} in section {section.id}")
                return section.reference, turn.reference
            else:
                logging.warning(f"Turn with index {turn_index} not found in section {section.id} despite being within range")
    
    logging.warning(f"Could not find turn with index {turn_index} in any section of transcript {transcript_id}")
    return None, None

def add_questions_to_turn(turn_ref, questions, question_type):
    questions_collection = turn_ref.collection('questions')
    
    for question in questions:
        question_data = question.dict()
        question_data['type'] = question_type
        
        # For reflective questions, handle perspectives separately
        if question_type == 'reflective' and 'perspectives' in question_data:
            perspectives = question_data.pop('perspectives')
            question_ref = questions_collection.add(question_data)[1]
            
            # Add perspectives as a subcollection
            perspectives_collection = question_ref.collection('perspectives')
            for perspective in perspectives:
                perspectives_collection.add({'name': perspective['name']})
        else:
            questions_collection.add(question_data)
    
    logging.info(f"Added {len(questions)} {question_type} questions to turn {turn_ref.id}")

def update_firestore_with_questions(transcript_id: str, questions: List[Any], question_type: str):
    logging.info(f"Processing {len(questions)} {question_type} question sets for transcript {transcript_id}")
    
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    for turn_questions in questions:
        logging.info(f"Processing questions for turn index {turn_questions.turn_index}")
        section_ref, turn_ref = find_turn_in_sections(transcript_id, turn_questions.turn_index)
        
        if not turn_ref:
            logging.warning(f"Could not find turn with index {turn_questions.turn_index} in transcript {transcript_id}")
            continue

        logging.info(f"Found turn with index {turn_questions.turn_index}")
        
        add_questions_to_turn(turn_ref, 
                              getattr(turn_questions, f'{question_type}_questions'), 
                              question_type)

    # Update the transcript document to indicate that questions have been generated
    transcript_ref.update({
        f'has_{question_type}_questions': True
    })

    logging.info(f"Updated transcript {transcript_id} with {question_type} question flag")
    logging.info(f"Completed adding {question_type} questions for transcript {transcript_id}")

def process_section(section: firestore.DocumentSnapshot, question_generator: Callable, question_type: str) -> List[Any]:
    """
    Process a single section to generate questions.

    Args:
        section (firestore.DocumentSnapshot): The Firestore document snapshot of the section.
        question_generator (Callable): The function to generate questions for the section.
        question_type (str): The type of questions being generated (e.g., "enrichment" or "reflective").

    Returns:
        List[Any]: A list of generated questions for the section.
    """
    try:
        section_data = section.to_dict()
        section_data['turns'] = [turn.to_dict() for turn in section.reference.collection('turns').stream()]
        
        section_questions = question_generator(section_data)
        logging.info(f"Generated {len(section_questions) if section_questions else 0} {question_type} questions for section {section.id}")
        
        return section_questions
    except Exception as e:
        logging.error(f"Error processing section {section.id}: {str(e)}")
        return []

def generate_questions(
    transcript_id: str,
    question_generator: Callable,
    question_type: str,
    test_mode: bool = False
) -> List[Any]:
    try:
        logging.info(f"Starting {question_type} question generation for transcript {transcript_id}")
        
        # Verify transcript structure
        verify_transcript_structure(transcript_id)
        
        db = get_firestore_client()
        transcript_ref = db.collection('transcripts').document(transcript_id)
        sections = list(transcript_ref.collection('sections').stream())
        
        all_questions = []
        
        # Process sections in pairs using two workers
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for i in range(0, len(sections), 2):
                section_pair = sections[i:i+2]
                for section in section_pair:
                    futures.append(executor.submit(process_section, section, question_generator, question_type))
                
                if test_mode:
                    break  # Only process the first pair in test mode
            
            for future in as_completed(futures):
                section_questions = future.result()
                if section_questions:
                    all_questions.extend(section_questions)
        
        logging.info(f"{question_type.capitalize()} questions generated for transcript {transcript_id}: {len(all_questions)} question sets")
        
        logging.info(f"Updating Firestore with {question_type} questions for transcript {transcript_id}")
        update_firestore_with_questions(transcript_id, all_questions, question_type=question_type)
        logging.info(f"{question_type.capitalize()} questions updated in Firestore for transcript {transcript_id}")
        
        return all_questions
    except Exception as e:
        error_message = f"Error generating transcript {question_type} questions: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise

def verify_transcript_structure(transcript_id: str):
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    logging.info(f"Verifying structure for transcript {transcript_id}")
    
    sections = transcript_ref.collection('sections').stream()
    section_count = 0
    total_turns = 0
    
    for section in sections:
        section_count += 1
        section_data = section.to_dict()
        logging.info(f"Section {section.id}:")
        logging.info(f"  Title: {section_data.get('title', 'N/A')}")
        logging.info(f"  Start Turn: {section_data.get('start_turn', 'N/A')}")
        logging.info(f"  End Turn: {section_data.get('end_turn', 'N/A')}")
        
        turns = section.reference.collection('turns').stream()
        turn_count = 0
        for turn in turns:
            turn_count += 1
            turn_data = turn.to_dict()
            logging.info(f"  Turn {turn.id}:")
            logging.info(f"    turn_index: {turn_data.get('index', 'N/A')}")
            logging.info(f"    role: {turn_data.get('role', 'N/A')}")
            logging.info(f"    speaker: {turn_data.get('speaker', 'N/A')}")
        
        logging.info(f"  Total turns in section: {turn_count}")
        total_turns += turn_count
    
    logging.info(f"Total sections in transcript: {section_count}")
    logging.info(f"Total turns across all sections: {total_turns}")
    logging.info("Transcript structure verification complete")

def format_section_for_questioning(section_data: Dict[str, Any]) -> str:
    formatted_turns = []
    for turn in section_data['turns']:
        index = turn['index']
        role = turn['role']
        speaker = turn['speaker']
        content = turn['content']
        formatted_turn = f"[Turn {index}] {role} ({speaker}): {content}"
        formatted_turns.append(formatted_turn)
    return "\n\n".join(formatted_turns)

def get_enrichment_questions(transcript_ref: firestore.DocumentReference) -> List[firestore.DocumentSnapshot]:
    questions = []
    sections = transcript_ref.collection('sections').stream()
    
    for section in sections:
        turns = section.reference.collection('turns').stream()
        for turn in turns:
            turn_questions = turn.reference.collection('questions').where('type', '==', 'enrichment').stream()
            questions.extend(turn_questions)
    
    return questions

def add_answer_to_question(question_ref: firestore.DocumentReference, answer: str):
    answer_collection = question_ref.collection('answers')
    answer_collection.add({
        'text': answer,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    logging.info(f"Added answer to question {question_ref.id}")