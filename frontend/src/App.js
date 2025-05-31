import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth Context
const AuthContext = React.createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [merchant, setMerchant] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userType, setUserType] = useState(localStorage.getItem('userType') || 'user');

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      if (userType === 'merchant') {
        fetchCurrentMerchant();
      } else {
        fetchCurrentUser();
      }
    }
  }, [token, userType]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`);
      setUser(response.data);
      setMerchant(null);
    } catch (error) {
      console.error('Error fetching user:', error);
      logout();
    }
  };

  const fetchCurrentMerchant = async () => {
    try {
      const response = await axios.get(`${API}/merchants/me`);
      setMerchant(response.data);
      setUser(null);
    } catch (error) {
      console.error('Error fetching merchant:', error);
      logout();
    }
  };

  const login = (token, userData, type = 'user') => {
    localStorage.setItem('token', token);
    localStorage.setItem('userType', type);
    setToken(token);
    setUserType(type);
    if (type === 'merchant') {
      setMerchant(userData);
      setUser(null);
    } else {
      setUser(userData);
      setMerchant(null);
    }
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userType');
    setToken(null);
    setUser(null);
    setMerchant(null);
    setUserType('user');
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      merchant, 
      userType, 
      login, 
      logout, 
      isAuthenticated: !!(user || merchant) 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => React.useContext(AuthContext);

// Components
const Header = () => {
  const { user, merchant, logout, userType } = useAuth();
  const currentEntity = user || merchant;

  return (
    <header className="bg-white shadow-lg border-b border-gray-200 fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-4">
            <h1 className="text-3xl font-bold text-indigo-600">FindBuddy</h1>
            <p className="text-gray-500 hidden sm:block">
              {userType === 'merchant' ? 'Business Partner Dashboard' : 'Find your activity companions'}
            </p>
          </div>
          {currentEntity && (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">
                Welcome, {userType === 'merchant' ? merchant?.business_name : user?.name}!
              </span>
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

const UserProfileSidebar = ({ user, onCreateActivity }) => {
  const [myActivities, setMyActivities] = useState({ created: [], joined: [] });
  const [loadingActivities, setLoadingActivities] = useState(false);

  useEffect(() => {
    fetchMyActivities();
  }, []);

  const fetchMyActivities = async () => {
    setLoadingActivities(true);
    try {
      const response = await axios.get(`${API}/activities/my`);
      setMyActivities({
        created: response.data.created_activities,
        joined: response.data.joined_activities
      });
    } catch (error) {
      console.error('Error fetching my activities:', error);
    } finally {
      setLoadingActivities(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* User Profile Card */}
      <div className="bg-white rounded-lg shadow-md p-6 sticky top-24">
        <div className="text-center mb-6">
          <div className="w-20 h-20 bg-indigo-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
            {user.name.charAt(0)}
          </div>
          <h2 className="text-xl font-bold text-gray-900">{user.name}</h2>
          <p className="text-gray-600">{user.city}</p>
          {user.bio && <p className="text-gray-600 text-sm mt-2">{user.bio}</p>}
        </div>

        {user.interests && user.interests.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-2">Interests</h3>
            <div className="flex flex-wrap gap-1">
              {user.interests.map((interest, index) => (
                <span key={index} className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-xs">
                  {interest}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-3">
          <button
            onClick={onCreateActivity}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <span>➕</span>
            <span>Create Activity</span>
          </button>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-gray-900 mb-2">Quick Stats</h4>
            <div className="space-y-1 text-sm text-gray-600">
              <div className="flex justify-between">
                <span>Member since:</span>
                <span>{new Date(user.created_at).toLocaleDateString()}</span>
              </div>
              <div className="flex justify-between">
                <span>City:</span>
                <span>{user.city}</span>
              </div>
              <div className="flex justify-between">
                <span>Activities Created:</span>
                <span>{myActivities.created.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Activities Joined:</span>
                <span>{myActivities.joined.length}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* My Activities Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
          <span className="mr-2">📅</span>
          My Activities
        </h3>
        
        {loadingActivities ? (
          <div className="text-center py-4">
            <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600"></div>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Created Activities */}
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2">
                Organizing ({myActivities.created.length})
              </h4>
              {myActivities.created.length === 0 ? (
                <p className="text-xs text-gray-500">No activities created yet</p>
              ) : (
                <div className="space-y-2">
                  {myActivities.created.slice(0, 3).map((activity) => (
                    <div key={activity.id} className="bg-blue-50 p-3 rounded border-l-4 border-blue-400">
                      <h5 className="text-sm font-medium text-blue-900 leading-tight">
                        {activity.title.length > 50 ? activity.title.substring(0, 50) + '...' : activity.title}
                      </h5>
                      <p className="text-xs text-blue-600 mt-1">
                        {new Date(activity.date).toLocaleDateString()} • {activity.participants.length} attending
                      </p>
                    </div>
                  ))}
                  {myActivities.created.length > 3 && (
                    <p className="text-xs text-gray-500">+{myActivities.created.length - 3} more</p>
                  )}
                </div>
              )}
            </div>

            {/* Joined Activities */}
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2">
                Attending ({myActivities.joined.length})
              </h4>
              {myActivities.joined.length === 0 ? (
                <p className="text-xs text-gray-500">No activities joined yet</p>
              ) : (
                <div className="space-y-2">
                  {myActivities.joined.slice(0, 3).map((activity) => (
                    <div key={activity.id} className="bg-green-50 p-3 rounded border-l-4 border-green-400">
                      <h5 className="text-sm font-medium text-green-900 leading-tight">
                        {activity.title.length > 50 ? activity.title.substring(0, 50) + '...' : activity.title}
                      </h5>
                      <p className="text-xs text-green-600 mt-1">
                        {new Date(activity.date).toLocaleDateString()} • by {activity.creator_name}
                      </p>
                    </div>
                  ))}
                  {myActivities.joined.length > 3 && (
                    <p className="text-xs text-gray-500">+{myActivities.joined.length - 3} more</p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [userType, setUserType] = useState('user');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    city: '',
    phone: '',
    bio: '',
    interests: '',
    // Merchant fields
    business_name: '',
    business_type: '',
    address: '',
    description: '',
    website: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = userType === 'merchant' 
        ? (isLogin ? '/merchants/login' : '/merchants/register')
        : (isLogin ? '/auth/login' : '/auth/register');

      let payload;
      if (isLogin) {
        payload = { email: formData.email, password: formData.password };
      } else {
        if (userType === 'merchant') {
          payload = {
            business_name: formData.business_name,
            email: formData.email,
            password: formData.password,
            business_type: formData.business_type,
            address: formData.address,
            city: formData.city,
            phone: formData.phone,
            description: formData.description,
            website: formData.website
          };
        } else {
          payload = {
            ...formData,
            interests: formData.interests.split(',').map(i => i.trim()).filter(i => i)
          };
        }
      }

      const response = await axios.post(`${API}${endpoint}`, payload);
      const userData = userType === 'merchant' ? response.data.merchant : response.data.user;
      login(response.data.token, userData, userType);
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
          {/* User Type Toggle */}
          <div className="mb-6">
            <div className="flex rounded-lg bg-gray-100 p-1">
              <button
                type="button"
                onClick={() => setUserType('user')}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  userType === 'user' ? 'bg-white text-indigo-600 shadow' : 'text-gray-500'
                }`}
              >
                User
              </button>
              <button
                type="button"
                onClick={() => setUserType('merchant')}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  userType === 'merchant' ? 'bg-white text-indigo-600 shadow' : 'text-gray-500'
                }`}
              >
                Business
              </button>
            </div>
          </div>

          {/* Login/Register Toggle */}
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
                {userType === 'user' ? (
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
                ) : (
                  <>
                    <input
                      type="text"
                      name="business_name"
                      placeholder="Business Name"
                      value={formData.business_name}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <select
                      name="business_type"
                      value={formData.business_type}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="">Select Business Type</option>
                      <option value="restaurant">Restaurant</option>
                      <option value="entertainment">Entertainment</option>
                      <option value="sports">Sports & Recreation</option>
                      <option value="events">Events & Venues</option>
                      <option value="retail">Retail</option>
                      <option value="services">Services</option>
                      <option value="other">Other</option>
                    </select>
                    <input
                      type="text"
                      name="address"
                      placeholder="Business Address"
                      value={formData.address}
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
                      placeholder="Business Phone"
                      value={formData.phone}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <textarea
                      name="description"
                      placeholder="Business Description"
                      value={formData.description}
                      onChange={handleChange}
                      required
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <input
                      type="url"
                      name="website"
                      placeholder="Website (optional)"
                      value={formData.website}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </>
                )}
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
              {loading ? 'Please wait...' : (isLogin ? 'Login' : `Create ${userType === 'merchant' ? 'Business' : 'User'} Account`)}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

// User Components
const ActivityCard = ({ activity, onJoin, showJoinButton = true, isOwn = false }) => {
  const [showComments, setShowComments] = useState(false);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [likes, setLikes] = useState({ count: 0, liked: false });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLikes();
  }, [activity.id]);

  const fetchLikes = async () => {
    try {
      const response = await axios.get(`${API}/activities/${activity.id}/likes`);
      setLikes({
        count: response.data.like_count,
        liked: false // We'll check this properly in a real implementation
      });
    } catch (error) {
      console.error('Error fetching likes:', error);
    }
  };

  const fetchComments = async () => {
    if (showComments && comments.length === 0) {
      try {
        const response = await axios.get(`${API}/activities/${activity.id}/comments`);
        setComments(response.data.comments);
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    }
  };

  const handleLike = async () => {
    try {
      const response = await axios.post(`${API}/activities/${activity.id}/like`);
      setLikes({
        count: response.data.like_count,
        liked: response.data.liked
      });
    } catch (error) {
      console.error('Error toggling like:', error);
    }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API}/activities/${activity.id}/comment`, {
        activity_id: activity.id,
        content: newComment
      });
      setComments([...comments, response.data.comment]);
      setNewComment('');
    } catch (error) {
      console.error('Error adding comment:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
      return `${diffDays}d ago`;
    } else if (diffHours > 0) {
      return `${diffHours}h ago`;
    } else {
      return 'Just now';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-200 mb-6">
      {/* Header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-indigo-500 rounded-full flex items-center justify-center text-white font-semibold">
            {activity.creator_name.charAt(0)}
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">{activity.creator_name}</h4>
            <p className="text-sm text-gray-500">{formatTimeAgo(activity.created_at)}</p>
          </div>
          <span className="ml-auto bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-xs font-medium">
            {activity.category}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">{activity.title}</h3>
        <p className="text-gray-700 mb-4 leading-relaxed">{activity.description}</p>
        
        <div className="space-y-2 text-sm text-gray-600 mb-4">
          <div className="flex items-center">
            <span className="font-medium">📅</span>
            <span className="ml-2">{formatDate(activity.date)}</span>
          </div>
          <div className="flex items-center">
            <span className="font-medium">📍</span>
            <span className="ml-2">{activity.location}, {activity.city}</span>
          </div>
          <div className="flex items-center">
            <span className="font-medium">👥</span>
            <span className="ml-2">{activity.participants.length} attending</span>
            {activity.max_participants && (
              <span> • {activity.max_participants} max</span>
            )}
          </div>
        </div>

        {activity.interests && activity.interests.length > 0 && (
          <div className="mb-4">
            <div className="flex flex-wrap gap-1">
              {activity.interests.map((interest, index) => (
                <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                  #{interest}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Social Actions */}
      <div className="px-4 py-3 border-t border-gray-100">
        <div className="flex items-center space-x-6">
          <button
            onClick={handleLike}
            className={`flex items-center space-x-1 ${
              likes.liked ? 'text-red-500' : 'text-gray-500 hover:text-red-500'
            } transition-colors`}
          >
            <span>{likes.liked ? '❤️' : '🤍'}</span>
            <span className="text-sm">{likes.count}</span>
          </button>
          
          <button
            onClick={() => {
              setShowComments(!showComments);
              fetchComments();
            }}
            className="flex items-center space-x-1 text-gray-500 hover:text-blue-500 transition-colors"
          >
            <span>💬</span>
            <span className="text-sm">{comments.length}</span>
          </button>

          {showJoinButton && !isOwn && (
            <button
              onClick={() => onJoin(activity.id)}
              className="ml-auto bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors"
            >
              Join Activity
            </button>
          )}
        </div>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="border-t border-gray-100">
          {/* Comments List */}
          {comments.length > 0 && (
            <div className="px-4 py-3 max-h-60 overflow-y-auto">
              {comments.map((comment, index) => (
                <div key={index} className="mb-3 last:mb-0">
                  <div className="flex items-start space-x-2">
                    <div className="w-6 h-6 bg-gray-300 rounded-full flex items-center justify-center text-xs font-semibold">
                      {comment.user_name.charAt(0)}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm">
                        <span className="font-semibold">{comment.user_name}</span>
                        <span className="text-gray-700 ml-2">{comment.content}</span>
                      </p>
                      <p className="text-xs text-gray-500 mt-1">{formatTimeAgo(comment.created_at)}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Add Comment */}
          <div className="px-4 py-3 border-t border-gray-100">
            <form onSubmit={handleComment} className="flex space-x-2">
              <input
                type="text"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add a comment..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                disabled={loading || !newComment.trim()}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
              >
                {loading ? '...' : 'Post'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

const MerchantCard = ({ merchantData }) => {
  const { merchant, active_offers, offers_count } = merchantData;

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-200 mb-6">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-semibold text-gray-900">{merchant.business_name}</h3>
        <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-medium">
          {merchant.business_type}
        </span>
      </div>
      
      <p className="text-gray-600 mb-3">{merchant.description}</p>
      
      <div className="space-y-2 text-sm text-gray-500 mb-4">
        <div className="flex items-center">
          <span className="font-medium">📍 Location:</span>
          <span className="ml-2">{merchant.address}, {merchant.city}</span>
        </div>
        <div className="flex items-center">
          <span className="font-medium">📞 Phone:</span>
          <span className="ml-2">{merchant.phone}</span>
        </div>
        {merchant.website && (
          <div className="flex items-center">
            <span className="font-medium">🌐 Website:</span>
            <a href={merchant.website} target="_blank" rel="noopener noreferrer" className="ml-2 text-indigo-600 hover:underline">
              {merchant.website}
            </a>
          </div>
        )}
      </div>

      {offers_count > 0 && (
        <div className="border-t pt-4">
          <h4 className="font-semibold text-gray-900 mb-2">🎁 Buddy Discounts ({offers_count})</h4>
          <div className="space-y-2">
            {active_offers.slice(0, 2).map((offer, index) => (
              <div key={index} className="bg-yellow-50 border border-yellow-200 rounded p-3">
                <h5 className="font-medium text-yellow-800">{offer.title}</h5>
                <p className="text-sm text-yellow-700">{offer.description}</p>
                <div className="flex justify-between items-center mt-2">
                  <span className="font-bold text-yellow-800">
                    {offer.discount_percentage > 0 ? `${offer.discount_percentage}% OFF` : 'Special Offer'}
                  </span>
                  <span className="text-xs text-yellow-600">Min {offer.minimum_buddies} people</span>
                </div>
              </div>
            ))}
            {offers_count > 2 && (
              <p className="text-sm text-gray-500">+{offers_count - 2} more offers</p>
            )}
          </div>
        </div>
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
            <button onClick={onClose} className="text-gray-400 hover:text-gray-600">✕</button>
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

const UserDashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('around-me');
  const [activitiesAroundMe, setActivitiesAroundMe] = useState([]);
  const [merchants, setMerchants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    if (activeTab === 'around-me') {
      fetchActivitiesAroundMe();
    } else if (activeTab === 'merchants') {
      fetchMerchants();
    }
  }, [activeTab]);

  const fetchActivitiesAroundMe = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/activities/around-me`);
      setActivitiesAroundMe(response.data.activities);
    } catch (error) {
      console.error('Error fetching activities around me:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMerchants = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/merchants/near-me`);
      setMerchants(response.data.merchants);
    } catch (error) {
      console.error('Error fetching merchants:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleJoinActivity = async (activityId) => {
    try {
      await axios.post(`${API}/activities/join`, { activity_id: activityId });
      alert('Successfully joined activity!');
      fetchActivitiesAroundMe();
    } catch (error) {
      alert(error.response?.data?.detail || 'Error joining activity');
    }
  };

  const handleCreateActivity = () => {
    setShowCreateModal(false);
    // Refresh the appropriate tab data
    if (activeTab === 'around-me') {
      fetchActivitiesAroundMe();
    }
    // Show success message
    alert('Activity created successfully!');
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-80 flex-shrink-0">
            <UserProfileSidebar user={user} onCreateActivity={() => setShowCreateModal(true)} />
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Navigation Tabs */}
            <div className="bg-white rounded-lg shadow-md mb-8 sticky top-24 z-10">
              <div className="border-b border-gray-200">
                <nav className="flex">
                  <button
                    onClick={() => setActiveTab('around-me')}
                    className={`flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors ${
                      activeTab === 'around-me'
                        ? 'border-indigo-500 text-indigo-600 bg-indigo-50'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-center space-x-2">
                      <span>🌍</span>
                      <span>Activities Around Me</span>
                    </div>
                  </button>
                  <button
                    onClick={() => setActiveTab('merchants')}
                    className={`flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors ${
                      activeTab === 'merchants'
                        ? 'border-indigo-500 text-indigo-600 bg-indigo-50'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-center space-x-2">
                      <span>🏪</span>
                      <span>Merchants</span>
                    </div>
                  </button>
                </nav>
              </div>
            </div>

            {/* Merchant Banner */}
            {activeTab === 'merchants' && (
              <div className="mb-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg p-6 text-white shadow-lg">
                <div className="text-center">
                  <h2 className="text-2xl font-bold mb-2">🎉 Bring Your Buddy & Save!</h2>
                  <p className="text-lg opacity-90">
                    Enjoy exclusive discounts when you visit with friends. The more buddies, the bigger the savings!
                  </p>
                  <div className="flex justify-center items-center mt-4 space-x-4">
                    <div className="flex items-center">
                      <span className="text-3xl mr-2">👥</span>
                      <span className="text-sm">Group Discounts</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-3xl mr-2">💰</span>
                      <span className="text-sm">Special Offers</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-3xl mr-2">🎁</span>
                      <span className="text-sm">Buddy Rewards</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Content */}
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                <p className="mt-4 text-gray-600">Loading...</p>
              </div>
            ) : (
              <div>
                {activeTab === 'around-me' && (
                  <div>
                    <div className="flex justify-between items-center mb-6">
                      <h3 className="text-2xl font-bold text-gray-900">Professional Network Activities</h3>
                      <span className="text-sm text-gray-500">{activitiesAroundMe.length} activities found</span>
                    </div>
                    {activitiesAroundMe.length === 0 ? (
                      <div className="text-center py-12 bg-white rounded-lg shadow-md">
                        <p className="text-gray-600 text-lg">No activities found in your area.</p>
                        <p className="text-gray-500">Be the first to create a professional networking activity!</p>
                      </div>
                    ) : (
                      <div className="space-y-6">
                        {activitiesAroundMe.map((activity) => (
                          <ActivityCard
                            key={activity.id}
                            activity={activity}
                            onJoin={handleJoinActivity}
                            isOwn={activity.creator_id === user.id}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'merchants' && (
                  <div>
                    <div className="flex justify-between items-center mb-6">
                      <h3 className="text-2xl font-bold text-gray-900">Buddy Discounts in {user.city}</h3>
                      <span className="text-sm text-gray-500">{merchants.length} businesses found</span>
                    </div>
                    {merchants.length === 0 ? (
                      <div className="text-center py-12 bg-white rounded-lg shadow-md">
                        <p className="text-gray-600 text-lg">No merchant partners found in your area.</p>
                        <p className="text-gray-500">Check back soon for buddy discounts!</p>
                      </div>
                    ) : (
                      <div className="space-y-6">
                        {merchants.map((merchantData, index) => (
                          <MerchantCard key={index} merchantData={merchantData} />
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      <CreateActivityModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreateActivity}
      />
    </div>
  );
};

// Merchant Dashboard (placeholder)
const MerchantDashboard = () => {
  const { merchant } = useAuth();
  
  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      <Header />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Welcome, {merchant?.business_name}!</h2>
          <p className="text-gray-600">Merchant dashboard coming soon...</p>
          <p className="text-gray-500">Manage your buddy discounts and track redemptions.</p>
        </div>
      </div>
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
  const { isAuthenticated, userType } = useAuth();

  if (!isAuthenticated) {
    return <AuthForm />;
  }

  return userType === 'merchant' ? <MerchantDashboard /> : <UserDashboard />;
};

export default App;
