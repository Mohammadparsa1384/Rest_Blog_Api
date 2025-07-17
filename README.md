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
      <li>Clone the repository:
        <pre><code>git clone https://github.com/Mohammadparsa1384/Rest_Blog_Api.git</code></pre>
      </li>
      <li>Navigate to the project directory:
        <pre><code>cd Rest_Blog_Api</code></pre>
      </li>
      <li>Build the Docker containers:
        <pre><code>docker-compose build .</code></pre>
      </li>
      <li>Start the containers:
        <pre><code>docker-compose up</code></pre>
      </li>
      <li>Access the application:
        <ul>
          <li><strong>API root</strong>: <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a></li>
          <li><strong>Swagger UI</strong>: <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a></li>
          <li><strong>SMTP4Dev</strong>: <a href="http://127.0.0.1:5000" target="_blank">http://127.0.0.1:5000</a></li>
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
      <li>Real admin path is <code>/admin-panel-VcZ712sR/</code> for security</li>
    </ul>
  </div>

  <div class="section">
    <h2>✅ Testing</h2>
    <p>This project uses <code>pytest</code> and <code>pytest-django</code> for automated testing.</p>
    <p>To run tests inside the Docker container, use:</p>
    <pre><code>docker-compose exec web pytest</code></pre>
    <p>The test coverage includes:</p>
    <ul>
      <li>Authentication (register, login, activation, password reset)</li>
      <li>Post and comment creation/editing</li>
      <li>Profile management</li>
      <li>Admin-only actions like approving comments</li>
    </ul>
  </div>

  <div class="section">
    <h2>🌐 Deployment</h2>
    <p>The project is deployed and publicly accessible via the following URL:</p>
    <p><strong>🔗 Live API:</strong> <a href="https://dev-api-server.liara.run" target="_blank">https://dev-api-server.liara.run</a></p>
    <p>All API endpoints and Swagger documentation are available at this address.</p>
  </div>

</body>
