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
  transcriptIds: string[]; // Add this line to store transcript IDs
}

export const fetchInterviewersAndGuests = async (): Promise<InterviewerData[]> => {
  try {
    const transcriptsRef = collection(firestore, "transcripts");
    const transcriptsSnapshot = await getDocs(transcriptsRef);

    const interviewersMap: { [key: string]: InterviewerData } = {};

    transcriptsSnapshot.forEach((doc) => {
      const transcriptData = doc.data();
      const fileName = transcriptData.filename;
      
      if (!fileName) {
        console.warn(`Transcript ${doc.id} has no filename`);
        return;
      }

      const [interviewer, guest] = fileName.split('_').map((name: string) => name.split('.')[0]);
      
      if (!interviewer || !guest) {
        console.warn(`Invalid filename format for transcript ${doc.id}`);
        return;
      }

      if (!interviewersMap[interviewer]) {
        interviewersMap[interviewer] = {
          name: interviewer,
          guests: [],
          transcriptIds: []
        };
      }

      if (!interviewersMap[interviewer].guests.includes(guest)) {
        interviewersMap[interviewer].guests.push(guest);
      }
      interviewersMap[interviewer].transcriptIds.push(doc.id);
    });

    return Object.values(interviewersMap).sort((a, b) => a.name.localeCompare(b.name));
  } catch (error) {
    console.error("Error fetching interviewers and guests:", error);
    throw error;
  }
};