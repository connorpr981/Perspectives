import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { logOut } from '../../services/firebase';
import { fetchInterviewersAndGuests, InterviewerData } from '../../services/firestoreService';
import styles from '../../styles/sidePane.module.css';
import { FaSignOutAlt, FaQuestionCircle, FaTimes, FaSun, FaMoon, FaChevronRight } from 'react-icons/fa';

interface SidePaneProps {
  isExpanded: boolean;
  onClose: () => void;
  theme: string;
  toggleTheme: () => void;
}

interface InterviewerProps {
  name: string;
  guests: string[];
  transcriptIds: string[]; // Add this line
  onGuestSelect: (interviewer: string, guest: string, transcriptId: string) => void;
  selectedGuest: string | null;
}

const Interviewer: React.FC<InterviewerProps> = ({ name, guests, transcriptIds, onGuestSelect, selectedGuest }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={styles.interviewerSection}>
      <button
        className={`${styles.sidebarButton} ${styles.interviewerButton}`}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <FaChevronRight className={`${styles.buttonIcon} ${isExpanded ? styles.expanded : ''}`} />
        <span>{name}</span>
      </button>
      <div className={`${styles.guestList} ${isExpanded ? styles.expanded : ''}`}>
        {guests.map((guest, index) => (
          <button
            key={guest}
            className={`${styles.guestButton} ${selectedGuest === guest ? styles.selected : ''}`}
            onClick={() => onGuestSelect(name, guest, transcriptIds[index])}
          >
            {guest}
          </button>
        ))}
      </div>
    </div>
  );
};

export const SidePane: React.FC<SidePaneProps> = ({ isExpanded, onClose, theme, toggleTheme }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [selectedInterview, setSelectedInterview] = useState<{ interviewer: string, guest: string, transcriptId: string } | null>(null);
  const [interviewers, setInterviewers] = useState<InterviewerData[]>([]);

  useEffect(() => {
    const loadInterviewersAndGuests = async () => {
      try {
        const data = await fetchInterviewersAndGuests();
        setInterviewers(data);
      } catch (error) {
        console.error("Failed to load interviewers and guests:", error);
      }
    };

    loadInterviewersAndGuests();
  }, []);

  const handleSignOut = async () => {
    try {
      await logOut();
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const handleGuestSelect = (interviewer: string, guest: string, transcriptId: string) => {
    setSelectedInterview({ interviewer, guest, transcriptId });
    // You might want to add logic here to load the selected transcript
  };

  return (
    <div className={`${styles.sidePane} ${isExpanded ? styles.sidePaneExpanded : ''}`}>
      <div className={styles.userSection}>
        <img src={user?.photoURL || ''} alt={user?.displayName || ''} className={styles.userAvatar} />
        <div className={styles.userInfo}>
          <span className={styles.userName}>{user?.displayName}</span>
          <span className={styles.userEmail}>{user?.email}</span>
        </div>
        <div className={styles.userActions}>
          <button 
            className={styles.actionButton} 
            onClick={handleSignOut} 
            aria-label="Sign Out"
            title="Sign Out"
          >
            <FaSignOutAlt />
          </button>
          <button className={styles.actionButton} onClick={onClose} aria-label="Close Side Pane">
            <FaTimes />
          </button>
        </div>
      </div>
      <div className={styles.sidePaneContent}>
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Interviewers</h3>
          {interviewers.map((interviewer) => (
            <Interviewer
              key={interviewer.name}
              name={interviewer.name}
              guests={interviewer.guests}
              transcriptIds={interviewer.transcriptIds}
              onGuestSelect={handleGuestSelect}
              selectedGuest={selectedInterview?.interviewer === interviewer.name ? selectedInterview.guest : null}
            />
          ))}
        </div>
      </div>
      <div className={styles.settingsSection}>
        <h3 className={styles.sectionTitle}>Settings</h3>
        <button
          className={styles.sidebarButton}
          onClick={toggleTheme}
        >
          {theme === 'light' ? <FaMoon className={styles.buttonIcon} /> : <FaSun className={styles.buttonIcon} />}
          <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
        </button>
        <button
          className={styles.sidebarButton}
          onClick={() => {/* TODO: Implement help functionality */}}
        >
          <FaQuestionCircle className={styles.buttonIcon} />
          <span>Help</span>
        </button>
      </div>
    </div>
  );
};