import axios from 'axios';

// تكوين الإعدادات الأساسية لـ axios
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://api.codeaura.com/api' 
  : 'http://localhost:5000/api';

// إنشاء نسخة من axios مع الإعدادات الافتراضية
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة معترض للطلبات لإضافة رمز المصادقة إذا كان متاحاً
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// إضافة معترض للاستجابات للتعامل مع أخطاء المصادقة
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // تسجيل الخروج إذا انتهت صلاحية الرمز
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// خدمات المصادقة
export const authService = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  
  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
  
  googleLogin: async (tokenId) => {
    const response = await api.post('/auth/google', { token_id: tokenId });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  
  facebookLogin: async (accessToken) => {
    const response = await api.post('/auth/facebook', { access_token: accessToken });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  
  githubLogin: async (code) => {
    const response = await api.post('/auth/github', { code });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  }
};

// خدمات الدورات
export const courseService = {
  getAllCourses: async (params = {}) => {
    const response = await api.get('/courses', { params });
    return response.data;
  },
  
  getCourseById: async (id) => {
    const response = await api.get(`/courses/${id}`);
    return response.data;
  },
  
  getCoursesByCategory: async (categoryId, params = {}) => {
    const response = await api.get(`/categories/${categoryId}/courses`, { params });
    return response.data;
  },
  
  getPopularCourses: async (limit = 6) => {
    const response = await api.get('/courses/popular', { params: { limit } });
    return response.data;
  },
  
  searchCourses: async (query, params = {}) => {
    const response = await api.get('/courses/search', { params: { query, ...params } });
    return response.data;
  },
  
  rateCourse: async (courseId, rating, reviewText = '') => {
    const response = await api.post(`/courses/${courseId}/rate`, { rating, review_text: reviewText });
    return response.data;
  },
  
  updateProgress: async (courseId, lessonId) => {
    const response = await api.post(`/courses/${courseId}/progress`, { lesson_id: lessonId });
    return response.data;
  },
  
  getUserCourses: async () => {
    const response = await api.get('/user/courses');
    return response.data;
  }
};

// خدمات الاختبارات
export const quizService = {
  getAllQuizzes: async (params = {}) => {
    const response = await api.get('/quizzes', { params });
    return response.data;
  },
  
  getQuizById: async (id) => {
    const response = await api.get(`/quizzes/${id}`);
    return response.data;
  },
  
  submitQuizAttempt: async (quizId, answers) => {
    const response = await api.post(`/quizzes/${quizId}/submit`, { answers });
    return response.data;
  },
  
  getUserQuizAttempts: async () => {
    const response = await api.get('/user/quiz-attempts');
    return response.data;
  }
};

// خدمات المقالات
export const articleService = {
  getAllArticles: async (params = {}) => {
    const response = await api.get('/articles', { params });
    return response.data;
  },
  
  getArticleById: async (id) => {
    const response = await api.get(`/articles/${id}`);
    return response.data;
  },
  
  getArticlesByCategory: async (categoryId, params = {}) => {
    const response = await api.get(`/categories/${categoryId}/articles`, { params });
    return response.data;
  }
};

// خدمات الألعاب
export const gameService = {
  getAllGames: async () => {
    const response = await api.get('/games');
    return response.data;
  },
  
  getGameById: async (id) => {
    const response = await api.get(`/games/${id}`);
    return response.data;
  },
  
  submitGameScore: async (gameId, score) => {
    const response = await api.post(`/games/${gameId}/score`, { score });
    return response.data;
  },
  
  getLeaderboard: async (gameId) => {
    const response = await api.get(`/games/${gameId}/leaderboard`);
    return response.data;
  }
};

// خدمات أدوات الذكاء الاصطناعي
export const aiToolService = {
  getAllTools: async () => {
    const response = await api.get('/ai-tools');
    return response.data;
  },
  
  getToolById: async (id) => {
    const response = await api.get(`/ai-tools/${id}`);
    return response.data;
  },
  
  useAITool: async (toolId, data) => {
    const response = await api.post(`/ai-tools/${toolId}/use`, data);
    return response.data;
  }
};

// خدمات المنتديات
export const forumService = {
  getAllForums: async () => {
    const response = await api.get('/forums');
    return response.data;
  },
  
  getForumById: async (id) => {
    const response = await api.get(`/forums/${id}`);
    return response.data;
  },
  
  getForumPosts: async (forumId, params = {}) => {
    const response = await api.get(`/forums/${forumId}/posts`, { params });
    return response.data;
  },
  
  createForumPost: async (forumId, postData) => {
    const response = await api.post(`/forums/${forumId}/posts`, postData);
    return response.data;
  },
  
  replyToPost: async (postId, replyData) => {
    const response = await api.post(`/forum-posts/${postId}/replies`, replyData);
    return response.data;
  }
};

// خدمات التصنيفات
export const categoryService = {
  getAllCategories: async () => {
    const response = await api.get('/categories');
    return response.data;
  },
  
  getCategoryById: async (id) => {
    const response = await api.get(`/categories/${id}`);
    return response.data;
  }
};

// خدمات المستخدمين
export const userService = {
  getUserProfile: async () => {
    const response = await api.get('/user/profile');
    return response.data;
  },
  
  updateUserProfile: async (userData) => {
    const response = await api.put('/user/profile', userData);
    return response.data;
  },
  
  changePassword: async (currentPassword, newPassword) => {
    const response = await api.put('/user/change-password', { current_password: currentPassword, new_password: newPassword });
    return response.data;
  }
};

// خدمات لوحة تحكم الأدمن
export const adminService = {
  getDashboardStats: async () => {
    const response = await api.get('/admin/dashboard');
    return response.data;
  },
  
  // إدارة المستخدمين
  getUsers: async (params = {}) => {
    const response = await api.get('/admin/users', { params });
    return response.data;
  },
  
  updateUser: async (userId, userData) => {
    const response = await api.put(`/admin/users/${userId}`, userData);
    return response.data;
  },
  
  deleteUser: async (userId) => {
    const response = await api.delete(`/admin/users/${userId}`);
    return response.data;
  },
  
  // إدارة الدورات
  createCourse: async (courseData) => {
    const response = await api.post('/admin/courses', courseData);
    return response.data;
  },
  
  updateCourse: async (courseId, courseData) => {
    const response = await api.put(`/admin/courses/${courseId}`, courseData);
    return response.data;
  },
  
  deleteCourse: async (courseId) => {
    const response = await api.delete(`/admin/courses/${courseId}`);
    return response.data;
  },
  
  // إدارة الاختبارات
  createQuiz: async (quizData) => {
    const response = await api.post('/admin/quizzes', quizData);
    return response.data;
  },
  
  updateQuiz: async (quizId, quizData) => {
    const response = await api.put(`/admin/quizzes/${quizId}`, quizData);
    return response.data;
  },
  
  deleteQuiz: async (quizId) => {
    const response = await api.delete(`/admin/quizzes/${quizId}`);
    return response.data;
  },
  
  // إدارة المقالات
  createArticle: async (articleData) => {
    const response = await api.post('/admin/articles', articleData);
    return response.data;
  },
  
  updateArticle: async (articleId, articleData) => {
    const response = await api.put(`/admin/articles/${articleId}`, articleData);
    return response.data;
  },
  
  deleteArticle: async (articleId) => {
    const response = await api.delete(`/admin/articles/${articleId}`);
    return response.data;
  },
  
  // إدارة الألعاب
  createGame: async (gameData) => {
    const response = await api.post('/admin/games', gameData);
    return response.data;
  },
  
  updateGame: async (gameId, gameData) => {
    const response = await api.put(`/admin/games/${gameId}`, gameData);
    return response.data;
  },
  
  deleteGame: async (gameId) => {
    const response = await api.delete(`/admin/games/${gameId}`);
    return response.data;
  },
  
  // إدارة أدوات الذكاء الاصطناعي
  createAITool: async (toolData) => {
    const response = await api.post('/admin/ai-tools', toolData);
    return response.data;
  },
  
  updateAITool: async (toolId, toolData) => {
    const response = await api.put(`/admin/ai-tools/${toolId}`, toolData);
    return response.data;
  },
  
  deleteAITool: async (toolId) => {
    const response = await api.delete(`/admin/ai-tools/${toolId}`);
    return response.data;
  }
};

export default api;

