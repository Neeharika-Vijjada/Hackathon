import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth Context
const AuthContext = React.createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchCurrentUser();
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`);
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user:', error);
      logout();
    }
  };

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    setToken(token);
    setUser(userData);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => React.useContext(AuthContext);

// Components
const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-4">
            <h1 className="text-3xl font-bold text-indigo-600">FindBuddy</h1>
            <p className="text-gray-500 hidden sm:block">Find your activity companions</p>
          </div>
          {user && (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user.name}!</span>
              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    city: '',
    phone: '',
    bio: '',
    interests: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const payload = isLogin 
        ? { email: formData.email, password: formData.password }
        : {
            ...formData,
            interests: formData.interests.split(',').map(i => i.trim()).filter(i => i)
          };

      const response = await axios.post(`${API}${endpoint}`, payload);
      login(response.data.token, response.data.user);
    } catch (error) {
      setError(error.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">FindBuddy</h2>
          <p className="text-gray-600">Connect with like-minded people for amazing activities</p>
        </div>

        {/* Hero Image */}
        <div className="rounded-lg overflow-hidden">
          <img 
            src="https://images.unsplash.com/photo-1455734729978-db1ae4f687fc" 
            alt="Friends enjoying activities together"
            className="w-full h-48 object-cover"
          />
        </div>

        <div className="bg-white py-8 px-6 shadow-xl rounded-lg">
          <div className="mb-6">
            <div className="flex rounded-lg bg-gray-100 p-1">
              <button
                type="button"
                onClick={() => setIsLogin(true)}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  isLogin ? 'bg-white text-indigo-600 shadow' : 'text-gray-500'
                }`}
              >
                Login
              </button>
              <button
                type="button"
                onClick={() => setIsLogin(false)}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  !isLogin ? 'bg-white text-indigo-600 shadow' : 'text-gray-500'
                }`}
              >
                Sign Up
              </button>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <>
                <input
                  type="text"
                  name="name"
                  placeholder="Full Name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <input
                  type="text"
                  name="city"
                  placeholder="City"
                  value={formData.city}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <input
                  type="tel"
                  name="phone"
                  placeholder="Phone Number"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <textarea
                  name="bio"
                  placeholder="Brief bio (optional)"
                  value={formData.bio}
                  onChange={handleChange}
                  rows="2"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <input
                  type="text"
                  name="interests"
                  placeholder="Interests (comma separated: hiking, coffee, music)"
                  value={formData.interests}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </>
            )}
            
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors disabled:opacity-50"
            >
              {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Create Account')}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

const ActivityCard = ({ activity, onJoin, showJoinButton = true }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-200">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-semibold text-gray-900">{activity.title}</h3>
        <span className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-sm font-medium">
          {activity.category}
        </span>
      </div>
      
      <p className="text-gray-600 mb-3">{activity.description}</p>
      
      <div className="space-y-2 text-sm text-gray-500 mb-4">
        <div className="flex items-center">
          <span className="font-medium">📅 Date:</span>
          <span className="ml-2">{formatDate(activity.date)}</span>
        </div>
        <div className="flex items-center">
          <span className="font-medium">📍 Location:</span>
          <span className="ml-2">{activity.location}, {activity.city}</span>
        </div>
        <div className="flex items-center">
          <span className="font-medium">👤 Organizer:</span>
          <span className="ml-2">{activity.creator_name}</span>
        </div>
        <div className="flex items-center">
          <span className="font-medium">👥 Participants:</span>
          <span className="ml-2">{activity.participants.length}</span>
          {activity.max_participants && (
            <span>/{activity.max_participants}</span>
          )}
        </div>
      </div>

      {activity.interests && activity.interests.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-1">
            {activity.interests.map((interest, index) => (
              <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                {interest}
              </span>
            ))}
          </div>
        </div>
      )}

      {showJoinButton && (
        <button
          onClick={() => onJoin(activity.id)}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          Join Activity
        </button>
      )}
    </div>
  );
};

const CreateActivityModal = ({ isOpen, onClose, onCreate }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date: '',
    location: '',
    city: '',
    max_participants: '',
    category: '',
    interests: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        ...formData,
        date: new Date(formData.date).toISOString(),
        max_participants: formData.max_participants ? parseInt(formData.max_participants) : null,
        interests: formData.interests.split(',').map(i => i.trim()).filter(i => i)
      };

      await axios.post(`${API}/activities`, payload);
      onCreate();
      onClose();
      setFormData({
        title: '',
        description: '',
        date: '',
        location: '',
        city: '',
        max_participants: '',
        category: '',
        interests: ''
      });
    } catch (error) {
      console.error('Error creating activity:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-900">Create New Activity</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              name="title"
              placeholder="Activity Title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <textarea
              name="description"
              placeholder="Activity Description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="3"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="datetime-local"
              name="date"
              value={formData.date}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="text"
              name="location"
              placeholder="Location/Venue"
              value={formData.location}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="text"
              name="city"
              placeholder="City"
              value={formData.city}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="text"
              name="category"
              placeholder="Category (e.g., Sports, Food, Music)"
              value={formData.category}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="number"
              name="max_participants"
              placeholder="Max Participants (optional)"
              value={formData.max_participants}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="text"
              name="interests"
              placeholder="Related Interests (comma separated)"
              value={formData.interests}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 font-medium py-2 px-4 rounded-md transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Activity'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('feed');
  const [activities, setActivities] = useState([]);
  const [myActivities, setMyActivities] = useState({ created: [], joined: [] });
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    if (activeTab === 'feed') {
      fetchActivityFeed();
    } else if (activeTab === 'my-activities') {
      fetchMyActivities();
    }
  }, [activeTab]);

  const fetchActivityFeed = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/activities/feed`);
      setActivities(response.data.activities);
    } catch (error) {
      console.error('Error fetching activity feed:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMyActivities = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/activities/my`);
      setMyActivities({
        created: response.data.created_activities,
        joined: response.data.joined_activities
      });
    } catch (error) {
      console.error('Error fetching my activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleJoinActivity = async (activityId) => {
    try {
      await axios.post(`${API}/activities/join`, { activity_id: activityId });
      alert('Successfully joined activity!');
      fetchActivityFeed(); // Refresh the feed
    } catch (error) {
      alert(error.response?.data?.detail || 'Error joining activity');
    }
  };

  const handleCreateActivity = () => {
    setShowCreateModal(false);
    if (activeTab === 'feed') {
      fetchActivityFeed();
    } else if (activeTab === 'my-activities') {
      fetchMyActivities();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Profile Summary */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{user.name}</h2>
              <p className="text-gray-600">{user.city}</p>
              <p className="text-gray-600">{user.bio}</p>
              {user.interests && user.interests.length > 0 && (
                <div className="mt-2">
                  <span className="text-sm text-gray-500">Interests: </span>
                  {user.interests.map((interest, index) => (
                    <span key={index} className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-xs mr-1">
                      {interest}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
            >
              Create Activity
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-md mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex">
              <button
                onClick={() => setActiveTab('feed')}
                className={`py-3 px-6 border-b-2 font-medium text-sm ${
                  activeTab === 'feed'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Activity Feed
              </button>
              <button
                onClick={() => setActiveTab('my-activities')}
                className={`py-3 px-6 border-b-2 font-medium text-sm ${
                  activeTab === 'my-activities'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                My Activities
              </button>
            </nav>
          </div>
        </div>

        {/* Content */}
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            <p className="mt-2 text-gray-600">Loading activities...</p>
          </div>
        ) : (
          <div>
            {activeTab === 'feed' && (
              <div>
                {activities.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-gray-600">No activities found matching your interests.</p>
                    <p className="text-gray-500">Try creating an activity or updating your interests!</p>
                  </div>
                ) : (
                  <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {activities.map((activity) => (
                      <ActivityCard
                        key={activity.id}
                        activity={activity}
                        onJoin={handleJoinActivity}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'my-activities' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Created by You</h3>
                  {myActivities.created.length === 0 ? (
                    <p className="text-gray-600">You haven't created any activities yet.</p>
                  ) : (
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                      {myActivities.created.map((activity) => (
                        <ActivityCard
                          key={activity.id}
                          activity={activity}
                          showJoinButton={false}
                        />
                      ))}
                    </div>
                  )}
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Joined Activities</h3>
                  {myActivities.joined.length === 0 ? (
                    <p className="text-gray-600">You haven't joined any activities yet.</p>
                  ) : (
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                      {myActivities.joined.map((activity) => (
                        <ActivityCard
                          key={activity.id}
                          activity={activity}
                          showJoinButton={false}
                        />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <CreateActivityModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreateActivity}
      />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <AuthApp />
      </div>
    </AuthProvider>
  );
}

const AuthApp = () => {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? <Dashboard /> : <AuthForm />;
};

export default App;
