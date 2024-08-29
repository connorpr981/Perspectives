import { collection, getDocs, query, orderBy, doc, getDoc } from "firebase/firestore";
import { firestore } from "./firebase";

export const fetchTranscriptData = async (transcriptId: string) => {
  try {
    console.log('Fetching transcript:', transcriptId);
    const transcriptRef = doc(firestore, "transcripts", transcriptId);
    const transcriptDoc = await getDoc(transcriptRef);

    if (!transcriptDoc.exists()) {
      console.log('Transcript not found');
      throw new Error("Transcript not found");
    }

    console.log('Transcript data:', transcriptDoc.data());

    const sectionsQuery = query(collection(transcriptRef, "sections"), orderBy("start_turn"));
    const sectionsSnapshot = await getDocs(sectionsQuery);
    
    const sections = await Promise.all(sectionsSnapshot.docs.map(async (sectionDoc) => {
      const sectionData = sectionDoc.data();
      console.log('Section data:', sectionData);

      const turnsQuery = query(collection(sectionDoc.ref, "turns"), orderBy("index"));
      const turnsSnapshot = await getDocs(turnsQuery);
      
      const turns = await Promise.all(turnsSnapshot.docs.map(async (turnDoc) => {
        const turnData = turnDoc.data();
        
        // Fetch questions for each turn
        const questionsQuery = query(collection(turnDoc.ref, "questions"));
        const questionsSnapshot = await getDocs(questionsQuery);
        const questions = questionsSnapshot.docs.map(questionDoc => questionDoc.data());

        return { ...turnData, questions };
      }));

      return { ...sectionData, turns };
    }));

    console.log('Sections with turns and questions:', sections);

    return { transcript: transcriptDoc.data(), sections };
  } catch (error) {
    console.error("Error fetching transcript data:", error);
    throw error;
  }
};

export interface InterviewerData {
  name: string;
  guests: string[];
}

export const fetchInterviewersAndGuests = async (transcriptId: string): Promise<InterviewerData[]> => {
  try {
    const transcriptRef = doc(firestore, "transcripts", transcriptId);
    const transcriptDoc = await getDoc(transcriptRef);

    if (!transcriptDoc.exists()) {
      throw new Error("Transcript not found");
    }

    const fileName = transcriptDoc.data().filename;
    if (!fileName) {
      throw new Error("Filename not found in transcript data");
    }

    const [interviewer, guest] = fileName.split('_').map(name => name.split('.')[0]);
    if (!interviewer || !guest) {
      throw new Error("Invalid filename format");
    }

    return [{
      name: interviewer,
      guests: [guest]
    }];
  } catch (error) {
    console.error("Error fetching interviewer and guest:", error);
    throw error;
  }
};