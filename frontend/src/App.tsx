import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import { AuthProvider } from './context/AuthContext';
import { LoadingProvider } from './context/LoadingContext';
import { TranscriptProvider } from './context/TranscriptContext'; // Add this import
import { useAuth } from './hooks/useAuth';
import { useLoading } from './context/LoadingContext';
import LandingPage from './pages/LandingPage';
import PathBasedLayoutPage from './pages/PathBasedLayoutPage';
import FirebaseAuth from './components/auth/FirebaseAuth';
import LoadingSpinner from './components/LoadingSpinner';
import './styles/transitions.css';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();
  const { isLoading, setIsLoading } = useLoading();

  React.useEffect(() => {
    setIsLoading(loading);
  }, [loading, setIsLoading]);

  if (loading || isLoading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    <TransitionGroup>
      <CSSTransition key={location.pathname} classNames="fade" timeout={300}>
        <Routes location={location}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<FirebaseAuth />} />
          <Route
            path="/explore"
            element={
              <ProtectedRoute>
                <TranscriptProvider>
                  <PathBasedLayoutPage />
                </TranscriptProvider>
              </ProtectedRoute>
            }
          />
        </Routes>
      </CSSTransition>
    </TransitionGroup>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <LoadingProvider>
        <Router>
          <AnimatedRoutes />
        </Router>
      </LoadingProvider>
    </AuthProvider>
  );
};

export default App;