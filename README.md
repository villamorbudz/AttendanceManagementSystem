<h1 align="center">
    <img src="AMSystem/static/images/AMSystemlogo-dark.png#gh-light-mode-only" alt="AMSystem Logo Light" width="200"/>
    <img src="AMSystem/static/images/AMSystemlogo-light.png#gh-dark-mode-only" alt="AMSystem Logo Dark" width="200"/>
    <br>
    📊 Attendance Management System
</h1>

<div class="section">
    <h2>🎯 Project Overview</h2>
    <p>The Attendance Management System is a web-based system designed to manage and streamline employee attendance, leave applications, and reporting.</p>
    <p>It includes user-friendly features for both employees and administrators, offering an efficient solutions to track and manage attendance records and leave requests. This system is designed to substitute traditional methods of tracking attendance with a digital solution that efficiently records, stores, and processes attendance data.</p>
</div>

<div class="section">
    <h2>👥 Team Members</h2>
    <ul>
    <li>👨‍💻 <strong>Macapobre, Clarence Kirk H.</strong></li>
    <li>👨‍💻 <strong>Solasco, Ephraim Jay A.</strong></li>
    <li>👨‍💻 <strong>Villamor, Giles Anthony II I.</strong></li>
    </ul>
</div>

<div class="section">
    <h2>🛠️ Built with:</h2>
    <p align="center">
        <strong>🔧 Backend Technologies</strong><br/>
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
        <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
        <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
    </p>
    <p align="center">
        <strong>🎨 Frontend Technologies</strong><br/>
        <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML"/>
        <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS"/>
        <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
        <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS"/>
    
</div>

<div class="section">
    <h2>✨ Functional Requirements</h2>
    <h3>🔐 1. User Authentication</h3>
    <ul>
    <li>Secure login system to verify users.</li>
    <li>Role-based access control (Admin and Employee).</li>
    </ul>
    <h3>👥 2. Employee Registration and Management</h3>
    <ul>
    <li>Ability to add new employees to the system.</li>
    <li>Manage and maintain employee records such as personal details and job roles.</li>
    </ul>
    <h3>⏰ 3. Attendance Recording</h3>
    <ul>
    <li>Log daily attendance with timestamps.</li>
    <li>Mark absences, late arrivals, and early departures.</li>
    </ul>
    <h3>📊 4. Attendance Reports</h3>
    <ul>
    <li>Generate detailed reports on attendance.</li>
    <li>Provide summaries for specific employees or departments.</li>
    </ul>
    <h3>📅 5. Leave Management</h3>
    <ul>
    <li>Allow employees to apply for leaves.</li>
    <li>Admins can review, approve, or reject leave requests.</li>
    </ul>
    <h3>📱 6. User Dashboards</h3>
    <ul>
    <li>Overview of attendance metrics.</li>
    <li>Quick access to manage employees, leaves, and reports.</li>
    </ul>
</div>

<div class="section">
    <h2>📚 Project Documentation/Resources</h2>
    <ul>
    <li>📄 <strong>Functional Requirements Document:</strong> <a href="https://docs.google.com/document/d/1CV0SnLQ8Mk_a7esE05MgeWcsuibVhiEMZl3C8cEM4TM/edit?usp=sharing" target="_blank">Project Document</a></li>
    <li>📊 <strong>Gantt Chart:</strong> <a href="https://cebuinstituteoftechnology-my.sharepoint.com/:x:/g/personal/clarencekirk_macapobre_cit_edu/EX0PUaIayKpGj128RzcTkwsBBmu9KCDw7roXzGJaw4Itug?e=vygDPE" target="_blank">View Timeline</a></li>
    <li>🔄 <strong>Entity Relationship Diagram (ERD):</strong> <a href="https://online.visual-paradigm.com/share.jsp?id=323938343239332d34" target="_blank">View ERD</a></li>
    <li>🎨 <strong>UI/UX Design:</strong> <a href="https://www.figma.com/design/6IJLOH5yoD7sXUFPLvHjBk/Attendance-Management-System?node-id=0-1&node-type=canvas" target="_blank">Figma Prototype</a></li>
    </ul>
</div>

<div class="section">
    <h2>🚀 Step 1: Clone the Repository</h2>
    <p>Open your terminal and run the following command to clone the repository:</p>
    <pre>git clone <repository_url></pre>
</div>

<div class="section">
    <h2>⚙️ Step 2: Set Up the Virtual Environment</h2>
    <ul>
        <li>Create a virtual environment:</li>
        <pre>python3 -m venv env</pre>
         <li>Navigate to the project directory:</li>
        <pre>cd AMSystem</pre>
        <li>Activate the virtual environment:</li>
        <pre>../env/bin/Activate</pre>
    </ul>
</div>

<div class="section">
    <h2>📦 Step 3: Install Dependencies</h2>
    <p>Once the virtual environment is activated, install the required dependencies:</p>
    <pre>pip install -r requirements.txt</pre>
</div>

<div class="section">
    <h2>🗄️ Step 4: Configure the Database</h2>
    <p>Run migrations to set up the database:</p>
    <pre>python manage.py makemigrations</pre>
    <pre>python manage.py migrate</pre>
</div>

<div class="section">
    <h2>🌐 Step 5: Run the Development Server</h2>
    <p>Start the Django development server:</p>
    <pre>python manage.py runserver</pre>
    <p>Visit the app by going to:</p>
    <pre>http://127.0.0.1:8000/</pre>
</div>
