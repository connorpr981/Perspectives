import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { logOut } from '../../services/firebase';
import styles from '../../styles/sidePane.module.css';
import { FaSignOutAlt, FaLightbulb, FaQuestionCircle, FaTimes, FaChevronDown, FaSun, FaMoon, FaUser, FaChevronRight, FaMicrophone } from 'react-icons/fa';

interface InterviewLink {
  label: string;
  url: string;
}

interface Interview {
  interviewer: string;
  guest: string;
  podcastSeries?: string;
  episodeInfo?: string;
  duration?: string;
  topics?: string[];
  description?: string;
  tags?: string[];
  links?: InterviewLink[];
}

interface CurrentInterviewProps {
  interview: Interview;
  isExpanded: boolean;
  onToggle: () => void;
  maxTopics?: number;
  maxTags?: number;
  maxDescriptionLength?: number;
}

const CurrentInterview: React.FC<CurrentInterviewProps> = ({
  interview,
  isExpanded,
  onToggle,
  maxTopics = 5,
  maxTags = 5,
  maxDescriptionLength = 150
}) => {
  const detailsRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState<number | undefined>(undefined);

  useEffect(() => {
    if (detailsRef.current) {
      const newHeight = isExpanded ? detailsRef.current.scrollHeight : 0;
      setHeight(newHeight);
    }
  }, [isExpanded]);

  const {
    interviewer,
    guest,
    podcastSeries,
    episodeInfo,
    duration,
    topics,
    description,
    tags,
    links
  } = interview;

  const truncateText = (text: string, maxLength: number) =>
    text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;

  return (
    <div 
      className={`${styles.currentInterview} ${isExpanded ? styles.expanded : ''}`}
      onClick={onToggle}
      aria-expanded={isExpanded}
    >
      <div className={styles.interviewHeader}>
        <div className={styles.interviewInfo}>
          <FaMicrophone className={styles.podcastIcon} />
          <div className={styles.interviewText}>
            <div className={styles.interviewTitle}>
              <span className={styles.interviewerName}>{interviewer}</span>
              <span className={styles.interviewSeparator}>with</span>
              <span className={styles.guestName}>{guest}</span>
            </div>
            {!isExpanded && podcastSeries && (
              <div className={styles.podcastSeriesCollapsed}>{podcastSeries}</div>
            )}
          </div>
        </div>
        <FaChevronDown className={`${styles.expandIcon} ${isExpanded ? styles.expanded : ''}`} />
      </div>
      <div 
        className={styles.interviewDetails} 
        ref={detailsRef}
        style={{ height: height !== undefined ? `${height}px` : undefined }}
      >
        {podcastSeries && <p className={styles.podcastSeries}>{podcastSeries}</p>}
        {(episodeInfo || duration) && (
          <p className={styles.episodeInfo}>
            {episodeInfo} {duration && `• ${duration}`}
          </p>
        )}
        {topics && topics.length > 0 && (
          <div className={styles.topicsContainer}>
            {topics.slice(0, maxTopics).map((topic, index) => (
              <span key={index} className={styles.topic}>{topic}</span>
            ))}
            {topics.length > maxTopics && <span className={styles.topic}>+{topics.length - maxTopics}</span>}
          </div>
        )}
        {description && (
          <p className={styles.interviewDescription}>
            {truncateText(description, maxDescriptionLength)}
          </p>
        )}
        {tags && tags.length > 0 && (
          <div className={styles.tagsContainer}>
            {tags.slice(0, maxTags).map((tag, index) => (
              <span key={index} className={styles.tag}>{tag}</span>
            ))}
            {tags.length > maxTags && <span className={styles.tag}>+{tags.length - maxTags}</span>}
          </div>
        )}
        {links && links.length > 0 && (
          <div className={styles.links}>
            {links.map((link, index) => (
              <a key={index} href={link.url} target="_blank" rel="noopener noreferrer" className={styles.link}>
                {link.label}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

interface SidePaneProps {
  isExpanded: boolean;
  onClose: () => void;
  theme: string;
  toggleTheme: () => void;
}

interface InterviewerProps {
  name: string;
  guests: string[];
  onGuestSelect: (interviewer: string, guest: string) => void;
  selectedGuest: string | null;
}

const Interviewer: React.FC<InterviewerProps> = ({ name, guests, onGuestSelect, selectedGuest }) => {
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
        {guests.map((guest) => (
          <button
            key={guest}
            className={`${styles.guestButton} ${selectedGuest === guest ? styles.selected : ''}`}
            onClick={() => onGuestSelect(name, guest)}
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
  const [activeSection, setActiveSection] = useState<string>('explore');
  const [isInterviewExpanded, setIsInterviewExpanded] = useState(false);
  const [currentInterview, setCurrentInterview] = useState<Interview>({
    interviewer: "John Doe",
    guest: "Guest 1",
    podcastSeries: "Tech Talks",
    episodeInfo: "Episode 42",
    duration: "1h 30min",
    topics: ["AI", "Machine Learning", "Ethics in Technology"],
    description: "In this episode, we explore the latest advancements in AI and machine learning, discussing their potential impact on society and the ethical considerations that come with these technologies.",
    tags: ["technology", "artificial intelligence", "ethics"],
    links: [
      { label: "Interviewer Profile", url: "https://example.com/johndoe" },
      { label: "Guest Profile", url: "https://example.com/guest1" },
      { label: "Full Episode", url: "https://example.com/episode42" }
    ]
  });
  const [selectedInterview, setSelectedInterview] = useState<{ interviewer: string, guest: string } | null>(null);

  const handleSignOut = async () => {
    try {
      await logOut();
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const handleGuestSelect = (interviewer: string, guest: string) => {
    setSelectedInterview({ interviewer, guest });
    setCurrentInterview({
      interviewer,
      guest,
      podcastSeries: "Tech Talks",
      episodeInfo: "Episode 42",
      duration: "1h 30min",
      topics: ["AI", "Machine Learning", "Ethics in Technology"],
      description: "In this episode, we explore the latest advancements in AI and machine learning, discussing their potential impact on society and the ethical considerations that come with these technologies.",
      tags: ["technology", "artificial intelligence", "ethics"],
      links: [
        { label: "Interviewer Profile", url: `https://example.com/${interviewer.toLowerCase().replace(' ', '')}` },
        { label: "Guest Profile", url: `https://example.com/${guest.toLowerCase().replace(' ', '')}` },
        { label: "Full Episode", url: "https://example.com/episode42" }
      ]
    });
    setIsInterviewExpanded(true);
  };

  const interviewers = [
    { name: "John Doe", guests: ["Guest 1", "Guest 2", "Guest 3"] },
    { name: "Jane Smith", guests: ["Guest A", "Guest B", "Guest C"] },
    { name: "Alice Johnson", guests: ["Guest X", "Guest Y", "Guest Z"] },
  ];

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
        <CurrentInterview 
          interview={currentInterview}
          isExpanded={isInterviewExpanded}
          onToggle={() => setIsInterviewExpanded(!isInterviewExpanded)}
          maxTopics={3}
          maxTags={3}
          maxDescriptionLength={100}
        />
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Main</h3>
          <button
            className={`${styles.sidebarButton} ${activeSection === 'explore' ? styles.active : ''}`}
            onClick={() => setActiveSection('explore')}
          >
            <FaLightbulb className={styles.buttonIcon} />
            <span>Explore</span>
          </button>
        </div>
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Interviewers</h3>
          {interviewers.map((interviewer) => (
            <Interviewer
              key={interviewer.name}
              name={interviewer.name}
              guests={interviewer.guests}
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
          onClick={() => setActiveSection('help')}
        >
          <FaQuestionCircle className={styles.buttonIcon} />
          <span>Help</span>
        </button>
      </div>
    </div>
  );
};