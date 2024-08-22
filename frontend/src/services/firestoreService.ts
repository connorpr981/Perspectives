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
        console.log('Turn data:', turnData);

        const sentencesQuery = query(collection(turnDoc.ref, "sentences"), orderBy("index"));
        const sentencesSnapshot = await getDocs(sentencesQuery);
        const sentences = sentencesSnapshot.docs.map(sentenceDoc => sentenceDoc.data());

        return { ...turnData, sentences };
      }));

      return { ...sectionData, turns };
    }));

    console.log('Sections with turns and sentences:', sections);

    return { transcript: transcriptDoc.data(), sections };
  } catch (error) {
    console.error("Error fetching transcript data:", error);
    throw error;
  }
};