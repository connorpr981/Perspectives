import { collection, getDocs, query, orderBy, doc, getDoc } from "firebase/firestore";
import { firestore } from "./firebase";

export const fetchTranscriptData = async (transcriptId: string) => {
  try {
    const transcriptRef = doc(firestore, "transcripts", transcriptId);
    const transcriptDoc = await getDoc(transcriptRef);

    if (!transcriptDoc.exists()) {
      throw new Error("Transcript not found");
    }

    const sectionsQuery = query(collection(transcriptRef, "sections"), orderBy("start_turn"));
    const sectionsSnapshot = await getDocs(sectionsQuery);
    
    const sections = await Promise.all(sectionsSnapshot.docs.map(async (sectionDoc) => {
      const sectionData = sectionDoc.data();

      const turnsQuery = query(collection(sectionDoc.ref, "turns"), orderBy("index"));
      const turnsSnapshot = await getDocs(turnsQuery);
      
      const turns = await Promise.all(turnsSnapshot.docs.map(async (turnDoc) => {
        const turnData = turnDoc.data();
        
        const questionsQuery = query(collection(turnDoc.ref, "questions"));
        const questionsSnapshot = await getDocs(questionsQuery);
        const questions = await Promise.all(questionsSnapshot.docs.map(async (questionDoc) => {
          const questionData = questionDoc.data();
          
          if (questionData.type === 'reflective') {
            const perspectivesQuery = query(collection(questionDoc.ref, "perspectives"));
            const perspectivesSnapshot = await getDocs(perspectivesQuery);
            const perspectives = perspectivesSnapshot.docs.map(perspectiveDoc => perspectiveDoc.data());
            return { ...questionData, perspectives };
          }
          
          return questionData;
        }));

        return { ...turnData, questions };
      }));

      return { ...sectionData, turns };
    }));

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