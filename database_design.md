# تصميم قاعدة بيانات Code Aura

## 1. تحليل المتطلبات والكيانات الرئيسية

بناءً على المتطلبات المقدمة، يمكننا تحديد الكيانات الرئيسية التالية التي ستشكل أساس قاعدة بيانات موقع "Code Aura":

### الكيانات:

*   **المستخدمون (Users):** يمثلون المتعلمين وأعضاء المجتمع. سيحتاجون إلى ملفات شخصية، تسجيل دخول/تسجيل، وتتبع التقدم.
*   **الدورات (Courses):** المحتوى التعليمي الأساسي. كل دورة لها وصف، فيديوهات، مقالات نصية، ومستويات صعوبة.
*   **المقالات (Articles):** محتوى المدونة. مصنفة، قابلة للبحث، وتحتوي على تعليقات.
*   **الاختبارات (Quizzes):** أسئلة برمجية لتقييم المتعلمين. لها مستويات صعوبة، وتتبع الدرجات، ولوحة متصدرين.
*   **الألعاب (Games):** ألعاب برمجية تعليمية. نظام نقاط ومكافآت.
*   **أدوات الذكاء الاصطناعي (AI Tools):** أدوات مساعدة للمبرمجين. واجهة إدخال/إخراج ودعم API.
*   **التعليقات (Comments):** للمقالات ومنشورات المجتمع.
*   **الإعجابات (Likes):** لمنشورات المجتمع.
*   **المنتديات (Forums):** لمنتديات النقاش المجتمعية.
*   **التصنيفات (Categories):** لتصنيف الدورات والمقالات والمنتديات.
*   **التقدم (Progress):** لتتبع تقدم المستخدم في الدورات والاختبارات.
*   **لوحة المتصدرين (Leaderboard):** لتتبع درجات الاختبارات ونقاط الألعاب.
*   **المسؤولون (Admins):** لإدارة المحتوى والمستخدمين.

## 2. العلاقات بين الكيانات:

*   **المستخدمون والدورات:** علاقة متعدد لمتعدد (Many-to-Many) عبر جدول وسيط لتتبع الدورات المسجل بها المستخدم وتقدمه فيها.
*   **المستخدمون والمقالات:** علاقة واحد لمتعدد (One-to-Many) حيث يمكن للمستخدم كتابة عدة مقالات (إذا كان هناك نظام كتابة للمستخدمين) أو علاقة متعدد لمتعدد إذا كان هناك تفاعل مثل الإعجاب/التعليق.
*   **المستخدمون والاختبارات:** علاقة متعدد لمتعدد (Many-to-Many) لتتبع الاختبارات التي أجراها المستخدم ودرجاته.
*   **المستخدمون والألعاب:** علاقة متعدد لمتعدد (Many-to-Many) لتتبع الألعاب التي لعبها المستخدم ونقاطه.
*   **المستخدمون والتعليقات:** علاقة واحد لمتعدد (One-to-Many) حيث يمكن للمستخدم الواحد إضافة عدة تعليقات.
*   **المستخدمون والإعجابات:** علاقة واحد لمتعدد (One-to-Many) حيث يمكن للمستخدم الواحد إضافة عدة إعجابات.
*   **الدورات والتصنيفات:** علاقة متعدد لمتعدد (Many-to-Many) حيث يمكن للدورة الواحدة أن تنتمي لأكثر من تصنيف، والتصنيف الواحد يمكن أن يحتوي على عدة دورات.
*   **المقالات والتصنيفات:** علاقة متعدد لمتعدد (Many-to-Many) حيث يمكن للمقالة الواحدة أن تنتمي لأكثر من تصنيف، والتصنيف الواحد يمكن أن يحتوي على عدة مقالات.
*   **المنتديات والتصنيفات:** علاقة متعدد لمتعدد (Many-to-Many) حيث يمكن للمنتدى الواحد أن ينتمي لأكثر من تصنيف، والتصنيف الواحد يمكن أن يحتوي على عدة منتديات.
*   **المقالات والتعليقات:** علاقة واحد لمتعدد (One-to-Many) حيث يمكن للمقالة الواحدة أن تحتوي على عدة تعليقات.
*   **منشورات المجتمع والتعليقات/الإعجابات:** علاقة واحد لمتعدد (One-to-Many) لكل منهما.
*   **المسؤولون وجميع الكيانات:** علاقة واحد لمتعدد (One-to-Many) للإدارة (إنشاء، تعديل، حذف).

## 3. اختيار قاعدة البيانات

بناءً على المتطلبات التي تتضمن علاقات معقدة (متعدد لمتعدد) وتتبع للتقدم والدرجات، فإن قاعدة البيانات العلائقية (SQL) مثل **MySQL** ستكون خيارًا ممتازًا. توفر MySQL دعمًا قويًا للعلاقات، التكامل، والاستعلامات المعقدة، وهي مناسبة تمامًا لتخزين البيانات المنظمة مثل المستخدمين، الدورات، الاختبارات، والمقالات. كما أنها خيار شائع وموثوق به لتطبيقات الويب.

## 4. تصميم مخطط قاعدة البيانات (ERD - Entity-Relationship Diagram)

سأقوم الآن بتحديد الجداول والحقول الرئيسية لكل كيان، مع الإشارة إلى أنواع البيانات والعلاقات. هذا سيكون أساس مخطط ERD الذي سيتم إنشاؤه لاحقًا.

### الجداول المقترحة:

1.  **`users`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `username` (VARCHAR(50), UNIQUE, NOT NULL)
    *   `email` (VARCHAR(100), UNIQUE, NOT NULL)
    *   `password_hash` (VARCHAR(255), NOT NULL)
    *   `profile_picture_url` (VARCHAR(255))
    *   `bio` (TEXT)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `last_login` (DATETIME)
    *   `role` (ENUM('user', 'admin'), DEFAULT 'user')

2.  **`courses`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `title` (VARCHAR(255), NOT NULL)
    *   `description` (TEXT)
    *   `video_url` (VARCHAR(255)) - للفيديو الرئيسي للدورة
    *   `level` (ENUM('beginner', 'intermediate', 'advanced'), NOT NULL)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

3.  **`course_sections`** (لتقسيم الدورات إلى أجزاء)
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `course_id` (INT, FOREIGN KEY REFERENCES `courses`(`id`))
    *   `title` (VARCHAR(255), NOT NULL)
    *   `order_index` (INT, NOT NULL)

4.  **`course_lessons`** (الدروس داخل الأقسام)
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `section_id` (INT, FOREIGN KEY REFERENCES `course_sections`(`id`))
    *   `title` (VARCHAR(255), NOT NULL)
    *   `content_text` (LONGTEXT)
    *   `video_url` (VARCHAR(255))
    *   `order_index` (INT, NOT NULL)

5.  **`user_course_progress`** (جدول وسيط لتتبع تقدم المستخدم في الدورات)
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `course_id` (INT, FOREIGN KEY REFERENCES `courses`(`id`))
    *   `lesson_id` (INT, FOREIGN KEY REFERENCES `course_lessons`(`id`)) - آخر درس تم الوصول إليه
    *   `completed_lessons` (JSON) - لتخزين قائمة بالدروس المكتملة
    *   `status` (ENUM('not_started', 'in_progress', 'completed'), DEFAULT 'not_started')
    *   `started_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `completed_at` (DATETIME)
    *   PRIMARY KEY (`user_id`, `course_id`)

6.  **`categories`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `name` (VARCHAR(100), UNIQUE, NOT NULL)
    *   `description` (TEXT)

7.  **`course_categories`** (جدول وسيط لربط الدورات بالتصنيفات)
    *   `course_id` (INT, FOREIGN KEY REFERENCES `courses`(`id`))
    *   `category_id` (INT, FOREIGN KEY REFERENCES `categories`(`id`))
    *   PRIMARY KEY (`course_id`, `category_id`)

8.  **`articles`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `title` (VARCHAR(255), NOT NULL)
    *   `content` (LONGTEXT)
    *   `author_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
    *   `is_published` (BOOLEAN, DEFAULT TRUE)

9.  **`article_categories`** (جدول وسيط لربط المقالات بالتصنيفات)
    *   `article_id` (INT, FOREIGN KEY REFERENCES `articles`(`id`))
    *   `category_id` (INT, FOREIGN KEY REFERENCES `categories`(`id`))
    *   PRIMARY KEY (`article_id`, `category_id`)

10. **`quizzes`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `title` (VARCHAR(255), NOT NULL)
    *   `description` (TEXT)
    *   `level` (ENUM('easy', 'medium', 'hard'), NOT NULL)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

11. **`quiz_questions`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `quiz_id` (INT, FOREIGN KEY REFERENCES `quizzes`(`id`))
    *   `question_text` (TEXT, NOT NULL)
    *   `question_type` (ENUM('multiple_choice', 'code_challenge'), NOT NULL)
    *   `correct_answer` (TEXT) - يمكن أن يكون JSON للاختيار من متعدد أو نص للكود
    *   `options` (JSON) - للاختيار من متعدد

12. **`user_quiz_attempts`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `quiz_id` (INT, FOREIGN KEY REFERENCES `quizzes`(`id`))
    *   `score` (INT)
    *   `attempt_date` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `answers_submitted` (JSON) - لتخزين إجابات المستخدم

13. **`games`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `title` (VARCHAR(255), NOT NULL)
    *   `description` (TEXT)
    *   `game_url` (VARCHAR(255))
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

14. **`user_game_scores`**
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `game_id` (INT, FOREIGN KEY REFERENCES `games`(`id`))
    *   `score` (INT)
    *   `played_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   PRIMARY KEY (`user_id`, `game_id`)

15. **`ai_tools`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `name` (VARCHAR(255), NOT NULL)
    *   `description` (TEXT)
    *   `api_endpoint` (VARCHAR(255)) - إذا كانت الأداة تعتمد على API خارجي
    *   `tool_type` (ENUM('explain_code', 'generate_code', 'debug_code', 'convert_code'), NOT NULL)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

16. **`comments`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `content` (TEXT, NOT NULL)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `parent_comment_id` (INT, FOREIGN KEY REFERENCES `comments`(`id`)) - للردود
    *   `commentable_type` (VARCHAR(50)) - لتحديد نوع الكيان (مثال: 'article', 'community_post')
    *   `commentable_id` (INT) - لتحديد معرف الكيان

17. **`community_posts`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `title` (VARCHAR(255))
    *   `content` (TEXT, NOT NULL)
    *   `post_type` (ENUM('code', 'question', 'article_snippet'), NOT NULL)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

18. **`likes`**
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `likeable_type` (VARCHAR(50)) - لتحديد نوع الكيان (مثال: 'community_post', 'comment')
    *   `likeable_id` (INT) - لتحديد معرف الكيان
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   PRIMARY KEY (`user_id`, `likeable_type`, `likeable_id`)

19. **`forums`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `name` (VARCHAR(255), NOT NULL)
    *   `description` (TEXT)
    *   `category_id` (INT, FOREIGN KEY REFERENCES `categories`(`id`))
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

20. **`forum_posts`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `forum_id` (INT, FOREIGN KEY REFERENCES `forums`(`id`))
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `title` (VARCHAR(255))
    *   `content` (TEXT, NOT NULL)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `parent_post_id` (INT, FOREIGN KEY REFERENCES `forum_posts`(`id`)) - للردود

21. **`notifications`**
    *   `id` (PRIMARY KEY, INT, AUTO_INCREMENT)
    *   `user_id` (INT, FOREIGN KEY REFERENCES `users`(`id`))
    *   `message` (TEXT, NOT NULL)
    *   `is_read` (BOOLEAN, DEFAULT FALSE)
    *   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
    *   `related_entity_type` (VARCHAR(50))
    *   `related_entity_id` (INT)

## 5. ملاحظات إضافية على التصميم:

*   **التحقق من صحة البيانات:** يجب تطبيق قواعد التحقق من صحة البيانات على مستوى التطبيق وقاعدة البيانات لضمان سلامة البيانات.
*   **الفهرسة (Indexing):** سيتم إضافة فهارس على الحقول المستخدمة بشكل متكرر في الاستعلامات (مثل `user_id`, `course_id`, `category_id`) لتحسين أداء قاعدة البيانات.
*   **التعامل مع النصوص الطويلة:** استخدام `TEXT` أو `LONGTEXT` للحقول التي تحتوي على كميات كبيرة من النصوص مثل وصف الدورات، محتوى المقالات، وأسئلة الاختبارات.
*   **البيانات الوصفية (Metadata):** إضافة حقول `created_at` و `updated_at` لمعظم الجداول لتتبع وقت إنشاء وتعديل السجلات.
*   **المرونة:** تم تصميم بعض الجداول (مثل `comments` و `likes` و `notifications`) لتكون مرنة بما يكفي للتعامل مع أنواع مختلفة من الكيانات (polymorphic relations) باستخدام حقلي `_type` و `_id`.
*   **الأمان:** سيتم تخزين كلمات المرور كـ `password_hash` بدلاً من النص العادي لضمان الأمان.
*   **JSON Fields:** استخدام حقول JSON لتخزين البيانات المنظمة جزئيًا مثل `completed_lessons` في `user_course_progress` و `options` في `quiz_questions`، مما يوفر مرونة أكبر.

هذا التصميم يوفر بنية قوية ومرنة لقاعدة بيانات Code Aura، مع الأخذ في الاعتبار جميع المتطلبات المحددة.



## 6. مخطط علاقات الكيانات (ERD)

تم إنشاء مخطط علاقات الكيانات (ERD) التالي لتوضيح بنية قاعدة البيانات المقترحة وعلاقاتها:

![مخطط علاقات الكيانات Code Aura](code_aura_erd.png)




## 7. تحديثات على التصميم بناءً على ملاحظات المستخدم

### تحديثات جدول الدورات:

تم تحديث جدول `courses` ليشمل الحقول التالية:

```sql
courses:
- id (PRIMARY KEY, INT, AUTO_INCREMENT)
- title (VARCHAR(255), NOT NULL)
- description (TEXT)
- youtube_video_id (VARCHAR(50), NOT NULL) -- معرف فيديو اليوتيوب
- youtube_playlist_id (VARCHAR(50)) -- معرف قائمة التشغيل إذا كانت الدورة عبارة عن سلسلة
- language (ENUM('arabic', 'english', 'other'), NOT NULL, DEFAULT 'arabic')
- level (ENUM('beginner', 'intermediate', 'advanced'), NOT NULL)
- programming_language (VARCHAR(50)) -- لغة البرمجة المغطاة في الدورة
- duration_minutes (INT) -- مدة الدورة بالدقائق
- instructor_name (VARCHAR(255)) -- اسم المدرب
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- updated_at (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
```

### إضافة جدول تقييمات الدورات:

```sql
course_ratings:
- id (PRIMARY KEY, INT, AUTO_INCREMENT)
- user_id (INT, FOREIGN KEY REFERENCES users(id))
- course_id (INT, FOREIGN KEY REFERENCES courses(id))
- rating (INT, CHECK (rating >= 1 AND rating <= 5))
- review_text (TEXT)
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- UNIQUE KEY unique_user_course_rating (user_id, course_id)
```

### تحديثات جدول الاختبارات:

تم تحديث جدول `quizzes` ليشمل:

```sql
quizzes:
- id (PRIMARY KEY, INT, AUTO_INCREMENT)
- title (VARCHAR(255), NOT NULL)
- description (TEXT)
- programming_language (VARCHAR(50), NOT NULL) -- Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, etc.
- level (ENUM('easy', 'medium', 'hard'), NOT NULL)
- question_count (INT, DEFAULT 10)
- time_limit_minutes (INT, DEFAULT 30)
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
```

### تحديثات جدول أسئلة الاختبارات:

```sql
quiz_questions:
- id (PRIMARY KEY, INT, AUTO_INCREMENT)
- quiz_id (INT, FOREIGN KEY REFERENCES quizzes(id))
- question_text (TEXT, NOT NULL)
- question_type (ENUM('multiple_choice', 'code_output', 'code_completion', 'debugging'), NOT NULL)
- code_snippet (TEXT) -- الكود المرفق مع السؤال إن وجد
- correct_answer (TEXT)
- options (JSON) -- للاختيار من متعدد
- explanation (TEXT) -- شرح الإجابة الصحيحة
- difficulty_points (INT, DEFAULT 1) -- نقاط السؤال حسب الصعوبة
```

هذه التحديثات تضمن:
1. ربط جميع الدورات بفيديوهات اليوتيوب
2. تصنيف الدورات حسب اللغة مع التركيز على المحتوى العربي
3. نظام تقييم شامل للدورات
4. اختبارات متنوعة في لغات البرمجة المختلفة
5. أنواع أسئلة متعددة (اختيار من متعدد، توقع ناتج الكود، إكمال الكود، تصحيح الأخطاء)

