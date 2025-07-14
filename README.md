
<body>

  <h1>📘 Rest Blog API - Django Project</h1>

  <div class="section">
    <h2>🛠 Technologies Used</h2>
    <ul>
      <li>Django & Django REST Framework</li>
      <li>PostgreSQL (via Docker)</li>
      <li>JWT Authentication</li>
      <li>Swagger (drf-spectacular)</li>
      <li>SMTP4Dev (email testing)</li>
      <li>Docker & Docker Compose</li>
    </ul>
  </div>

  <div class="section">
    <h2>🚀 How to Run</h2>
    <ol>
      <li>Clone the repo</li>
      <li>Build containers:
        <pre><code>docker-compose build</code></pre>
      </li>
      <li>Run containers:
        <pre><code>docker-compose up</code></pre>
      </li>
      <li>Access:
        <ul>
          <li>API: <code>http://127.0.0.1:8000</code></li>
          <li>SMTP4Dev: <code>http://127.0.0.1:5000</code></li>
        </ul>
      </li>
    </ol>
  </div>

  <div class="section">
    <h2>🔐 Authentication Endpoints (Accounts App)</h2>
    <ul>
      <li><code>POST /accounts/api/v1/register/</code> – Register user</li>
      <li><code>GET /accounts/api/v1/activation/confirm/&lt;token&gt;/</code> – Email activation</li>
      <li><code>POST /accounts/api/v1/activation/resend/</code> – Resend activation</li>
      <li><code>POST /accounts/api/v1/jwt/create/</code> – Login (get token)</li>
      <li><code>POST /accounts/api/v1/jwt/refresh/</code> – Refresh token</li>
      <li><code>PUT /accounts/api/v1/change-password/</code> – Change password</li>
      <li><code>POST /accounts/api/v1/password-reset/</code> – Request reset</li>
      <li><code>POST /accounts/api/v1/password/reset/confirm/&lt;token&gt;/</code> – Confirm reset</li>
      <li><code>GET/PUT/PATCH /accounts/api/v1/profile/</code> – Manage profile</li>
    </ul>
  </div>

  <div class="section">
    <h2>📝 Blog App Endpoints</h2>
    <ul>
      <li><code>GET/POST /blog/api/v1/posts/</code> – List & create posts</li>
      <li><code>GET/PUT/PATCH /blog/api/v1/posts/&lt;slug&gt;/</code> – Detail & edit</li>
      <li><code>GET/POST /blog/api/v1/comments/</code> – Manage comments</li>
      <li><code>POST /blog/api/v1/comments/&lt;id&gt;/approve/</code> – Approve comment</li>
      <li><code>GET/POST /blog/api/v1/category/</code> – Manage categories</li>
    </ul>
  </div>

  <div class="section">
    <h2>📚 Swagger UI</h2>
    <p>You can access full API documentation via Swagger at:</p>
    <p><code>http://127.0.0.1:8000/</code></p>
  </div>

  <div class="section">
    <h2>📦 Admin Panel</h2>
    <ul>
      <li>Fake admin for honeypot: <code>/admin/</code></li>
      <li>Real admin path is secret – hidden for security</li>
    </ul>
  </div>

</body>
</html>
