import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { adminService } from '../../services/api';
import './AdminUsers.css';

const AdminUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [usersPerPage] = useState(10);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: 'id', direction: 'ascending' });
  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // في الإنتاج، استخدم API حقيقي
      // const response = await adminService.getUsers();
      
      // بيانات تجريبية للعرض
      const mockUsers = [
        { id: 1, username: 'أحمد محمد', email: 'ahmed@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-20', last_login: '2023-09-25' },
        { id: 2, username: 'سارة علي', email: 'sara@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-19', last_login: '2023-09-24' },
        { id: 3, username: 'محمد خالد', email: 'mohamed@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-18', last_login: '2023-09-23' },
        { id: 4, username: 'فاطمة أحمد', email: 'fatima@example.com', role: 'مستخدم', status: 'غير نشط', created_at: '2023-09-17', last_login: '2023-09-20' },
        { id: 5, username: 'عمر حسن', email: 'omar@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-16', last_login: '2023-09-22' },
        { id: 6, username: 'نور محمد', email: 'noor@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-15', last_login: '2023-09-21' },
        { id: 7, username: 'خالد عبدالله', email: 'khaled@example.com', role: 'مستخدم', status: 'محظور', created_at: '2023-09-14', last_login: '2023-09-19' },
        { id: 8, username: 'ليلى سعيد', email: 'layla@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-13', last_login: '2023-09-18' },
        { id: 9, username: 'يوسف أحمد', email: 'yousef@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-12', last_login: '2023-09-17' },
        { id: 10, username: 'هدى علي', email: 'huda@example.com', role: 'مستخدم', status: 'غير نشط', created_at: '2023-09-11', last_login: '2023-09-15' },
        { id: 11, username: 'زياد محمد', email: 'ziad@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-10', last_login: '2023-09-16' },
        { id: 12, username: 'رنا خالد', email: 'rana@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-09', last_login: '2023-09-14' },
        { id: 13, username: 'كريم سامي', email: 'kareem@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-08', last_login: '2023-09-13' },
        { id: 14, username: 'سلمى حسن', email: 'salma@example.com', role: 'مستخدم', status: 'محظور', created_at: '2023-09-07', last_login: '2023-09-12' },
        { id: 15, username: 'طارق محمود', email: 'tarek@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-06', last_login: '2023-09-11' },
        { id: 16, username: 'منى سعيد', email: 'mona@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-05', last_login: '2023-09-10' },
        { id: 17, username: 'باسم أحمد', email: 'bassem@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-04', last_login: '2023-09-09' },
        { id: 18, username: 'دينا محمد', email: 'dina@example.com', role: 'مستخدم', status: 'غير نشط', created_at: '2023-09-03', last_login: '2023-09-08' },
        { id: 19, username: 'أمير علي', email: 'amir@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-02', last_login: '2023-09-07' },
        { id: 20, username: 'ياسمين خالد', email: 'yasmin@example.com', role: 'مستخدم', status: 'نشط', created_at: '2023-09-01', last_login: '2023-09-06' },
        { id: 21, username: 'محمد قاسم', email: 'qaseemmohammad60@gmail.com', role: 'أدمن', status: 'نشط', created_at: '2023-08-30', last_login: '2023-09-25' }
      ];
      
      setUsers(mockUsers);
      
    } catch (err) {
      console.error('Error fetching users:', err);
      setError('حدث خطأ أثناء تحميل بيانات المستخدمين');
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedUsers = [...users].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) {
      return sortConfig.direction === 'ascending' ? -1 : 1;
    }
    if (a[sortConfig.key] > b[sortConfig.key]) {
      return sortConfig.direction === 'ascending' ? 1 : -1;
    }
    return 0;
  });

  const filteredUsers = sortedUsers.filter(user => {
    return (
      user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.status.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  // الصفحات
  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const currentUsers = filteredUsers.slice(indexOfFirstUser, indexOfLastUser);
  const totalPages = Math.ceil(filteredUsers.length / usersPerPage);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedUsers(currentUsers.map(user => user.id));
    } else {
      setSelectedUsers([]);
    }
  };

  const handleSelectUser = (userId) => {
    if (selectedUsers.includes(userId)) {
      setSelectedUsers(selectedUsers.filter(id => id !== userId));
    } else {
      setSelectedUsers([...selectedUsers, userId]);
    }
  };

  const handleDeleteSelected = () => {
    if (window.confirm(`هل أنت متأكد من حذف ${selectedUsers.length} مستخدم؟`)) {
      // في الإنتاج، استخدم API حقيقي
      // await adminService.deleteUsers(selectedUsers);
      
      setUsers(users.filter(user => !selectedUsers.includes(user.id)));
      setSelectedUsers([]);
    }
  };

  const handleStatusChange = (userId, newStatus) => {
    // في الإنتاج، استخدم API حقيقي
    // await adminService.updateUserStatus(userId, newStatus);
    
    setUsers(users.map(user => {
      if (user.id === userId) {
        return { ...user, status: newStatus };
      }
      return user;
    }));
  };

  const handleAddUser = () => {
    navigate('/admin/users/add');
  };

  const handleEditUser = (userId) => {
    navigate(`/admin/users/edit/${userId}`);
  };

  const handleDeleteUser = (userId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
      // في الإنتاج، استخدم API حقيقي
      // await adminService.deleteUser(userId);
      
      setUsers(users.filter(user => user.id !== userId));
    }
  };

  const UsersList = () => {
    if (loading) {
      return <div className="users-loading">جاري تحميل بيانات المستخدمين...</div>;
    }
  
    if (error) {
      return <div className="users-error">{error}</div>;
    }
  
    return (
      <div className="users-list">
        <div className="users-header">
          <h2>إدارة المستخدمين</h2>
          
          <div className="users-actions">
            <div className="search-box">
              <input
                type="text"
                placeholder="بحث عن مستخدم..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <i className="fas fa-search"></i>
            </div>
            
            <button className="add-button" onClick={handleAddUser}>
              <i className="fas fa-user-plus"></i>
              إضافة مستخدم
            </button>
          </div>
        </div>
        
        {selectedUsers.length > 0 && (
          <div className="bulk-actions">
            <span>{selectedUsers.length} مستخدم محدد</span>
            <div className="bulk-buttons">
              <button className="bulk-action-button status-active" onClick={() => handleBulkStatusChange('نشط')}>
                تنشيط
              </button>
              <button className="bulk-action-button status-inactive" onClick={() => handleBulkStatusChange('غير نشط')}>
                تعطيل
              </button>
              <button className="bulk-action-button status-banned" onClick={() => handleBulkStatusChange('محظور')}>
                حظر
              </button>
              <button className="bulk-action-button delete" onClick={handleDeleteSelected}>
                حذف
              </button>
            </div>
          </div>
        )}
        
        <div className="users-table-container">
          <table className="users-table">
            <thead>
              <tr>
                <th className="checkbox-column">
                  <input
                    type="checkbox"
                    onChange={handleSelectAll}
                    checked={selectedUsers.length === currentUsers.length && currentUsers.length > 0}
                  />
                </th>
                <th className="id-column" onClick={() => handleSort('id')}>
                  #
                  {sortConfig.key === 'id' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th onClick={() => handleSort('username')}>
                  اسم المستخدم
                  {sortConfig.key === 'username' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th onClick={() => handleSort('email')}>
                  البريد الإلكتروني
                  {sortConfig.key === 'email' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th onClick={() => handleSort('role')}>
                  الدور
                  {sortConfig.key === 'role' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th onClick={() => handleSort('status')}>
                  الحالة
                  {sortConfig.key === 'status' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th onClick={() => handleSort('created_at')}>
                  تاريخ التسجيل
                  {sortConfig.key === 'created_at' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th onClick={() => handleSort('last_login')}>
                  آخر تسجيل دخول
                  {sortConfig.key === 'last_login' && (
                    <i className={`fas fa-sort-${sortConfig.direction === 'ascending' ? 'up' : 'down'}`}></i>
                  )}
                </th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              {currentUsers.length === 0 ? (
                <tr>
                  <td colSpan="9" className="no-data">لا توجد بيانات للعرض</td>
                </tr>
              ) : (
                currentUsers.map(user => (
                  <tr key={user.id}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedUsers.includes(user.id)}
                        onChange={() => handleSelectUser(user.id)}
                      />
                    </td>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>
                      <span className={`role-badge ${user.role === 'أدمن' ? 'admin' : 'user'}`}>
                        {user.role}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${user.status === 'نشط' ? 'active' : user.status === 'غير نشط' ? 'inactive' : 'banned'}`}>
                        {user.status}
                      </span>
                    </td>
                    <td>{user.created_at}</td>
                    <td>{user.last_login}</td>
                    <td>
                      <div className="action-buttons">
                        <button className="action-button view" onClick={() => navigate(`/admin/users/view/${user.id}`)}>
                          <i className="fas fa-eye"></i>
                        </button>
                        <button className="action-button edit" onClick={() => handleEditUser(user.id)}>
                          <i className="fas fa-edit"></i>
                        </button>
                        <button className="action-button delete" onClick={() => handleDeleteUser(user.id)}>
                          <i className="fas fa-trash-alt"></i>
                        </button>
                        <div className="action-dropdown">
                          <button className="action-button dropdown-toggle">
                            <i className="fas fa-ellipsis-v"></i>
                          </button>
                          <div className="dropdown-menu">
                            <button onClick={() => handleStatusChange(user.id, 'نشط')}>تنشيط</button>
                            <button onClick={() => handleStatusChange(user.id, 'غير نشط')}>تعطيل</button>
                            <button onClick={() => handleStatusChange(user.id, 'محظور')}>حظر</button>
                            <button onClick={() => navigate(`/admin/users/reset-password/${user.id}`)}>إعادة تعيين كلمة المرور</button>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        
        {totalPages > 1 && (
          <div className="pagination">
            <button
              className="pagination-button"
              onClick={() => paginate(currentPage - 1)}
              disabled={currentPage === 1}
            >
              <i className="fas fa-chevron-right"></i>
            </button>
            
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(number => (
              <button
                key={number}
                className={`pagination-button ${currentPage === number ? 'active' : ''}`}
                onClick={() => paginate(number)}
              >
                {number}
              </button>
            ))}
            
            <button
              className="pagination-button"
              onClick={() => paginate(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              <i className="fas fa-chevron-left"></i>
            </button>
          </div>
        )}
      </div>
    );
  };

  const AddUser = () => {
    return (
      <div className="user-form">
        <h2>إضافة مستخدم جديد</h2>
        <form>
          <div className="form-group">
            <label htmlFor="username">اسم المستخدم</label>
            <input type="text" id="username" name="username" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <input type="email" id="email" name="email" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">كلمة المرور</label>
            <input type="password" id="password" name="password" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="role">الدور</label>
            <select id="role" name="role">
              <option value="مستخدم">مستخدم</option>
              <option value="أدمن">أدمن</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="status">الحالة</label>
            <select id="status" name="status">
              <option value="نشط">نشط</option>
              <option value="غير نشط">غير نشط</option>
              <option value="محظور">محظور</option>
            </select>
          </div>
          
          <div className="form-actions">
            <button type="submit" className="submit-button">إضافة المستخدم</button>
            <button type="button" className="cancel-button" onClick={() => navigate('/admin/users')}>إلغاء</button>
          </div>
        </form>
      </div>
    );
  };

  const EditUser = () => {
    return (
      <div className="user-form">
        <h2>تعديل بيانات المستخدم</h2>
        <form>
          <div className="form-group">
            <label htmlFor="username">اسم المستخدم</label>
            <input type="text" id="username" name="username" defaultValue="اسم المستخدم" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <input type="email" id="email" name="email" defaultValue="user@example.com" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="role">الدور</label>
            <select id="role" name="role" defaultValue="مستخدم">
              <option value="مستخدم">مستخدم</option>
              <option value="أدمن">أدمن</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="status">الحالة</label>
            <select id="status" name="status" defaultValue="نشط">
              <option value="نشط">نشط</option>
              <option value="غير نشط">غير نشط</option>
              <option value="محظور">محظور</option>
            </select>
          </div>
          
          <div className="form-actions">
            <button type="submit" className="submit-button">حفظ التغييرات</button>
            <button type="button" className="cancel-button" onClick={() => navigate('/admin/users')}>إلغاء</button>
          </div>
        </form>
      </div>
    );
  };

  const ViewUser = () => {
    return (
      <div className="user-view">
        <h2>عرض بيانات المستخدم</h2>
        
        <div className="user-profile">
          <div className="user-avatar">
            <i className="fas fa-user"></i>
          </div>
          
          <div className="user-details">
            <h3>أحمد محمد</h3>
            <p className="user-email">ahmed@example.com</p>
            <div className="user-meta">
              <span className="role-badge user">مستخدم</span>
              <span className="status-badge active">نشط</span>
            </div>
          </div>
        </div>
        
        <div className="user-info-grid">
          <div className="info-item">
            <span className="info-label">تاريخ التسجيل</span>
            <span className="info-value">2023-09-20</span>
          </div>
          
          <div className="info-item">
            <span className="info-label">آخر تسجيل دخول</span>
            <span className="info-value">2023-09-25</span>
          </div>
          
          <div className="info-item">
            <span className="info-label">عدد الدورات المسجلة</span>
            <span className="info-value">3</span>
          </div>
          
          <div className="info-item">
            <span className="info-label">عدد الاختبارات المكتملة</span>
            <span className="info-value">5</span>
          </div>
          
          <div className="info-item">
            <span className="info-label">المنشورات في المنتدى</span>
            <span className="info-value">12</span>
          </div>
          
          <div className="info-item">
            <span className="info-label">التقييمات</span>
            <span className="info-value">7</span>
          </div>
        </div>
        
        <div className="user-actions">
          <button className="edit-button" onClick={() => navigate('/admin/users/edit/1')}>
            <i className="fas fa-edit"></i>
            تعديل البيانات
          </button>
          
          <button className="reset-password-button">
            <i className="fas fa-key"></i>
            إعادة تعيين كلمة المرور
          </button>
          
          <button className="delete-button" onClick={() => handleDeleteUser(1)}>
            <i className="fas fa-trash-alt"></i>
            حذف المستخدم
          </button>
        </div>
        
        <div className="back-link">
          <Link to="/admin/users">
            <i className="fas fa-arrow-right"></i>
            العودة إلى قائمة المستخدمين
          </Link>
        </div>
      </div>
    );
  };

  return (
    <Routes>
      <Route path="/" element={<UsersList />} />
      <Route path="/add" element={<AddUser />} />
      <Route path="/edit/:id" element={<EditUser />} />
      <Route path="/view/:id" element={<ViewUser />} />
    </Routes>
  );
};

export default AdminUsers;

