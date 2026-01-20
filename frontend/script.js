// Me API Playground - Frontend JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const baseUrlInput = document.getElementById('baseUrl');
    const statusIndicator = document.getElementById('statusIndicator');
    const methodSelect = document.getElementById('methodSelect');
    const urlInput = document.getElementById('urlInput');
    const requestBody = document.getElementById('requestBody');
    const sendBtn = document.getElementById('sendBtn');
    const responseContent = document.getElementById('responseContent');

    // Check API health
    async function checkHealth() {
        try {
            const response = await fetch(`${baseUrlInput.value}/health`);
            if (response.ok) {
                statusIndicator.classList.add('connected');
            } else {
                statusIndicator.classList.remove('connected');
            }
        } catch (e) {
            statusIndicator.classList.remove('connected');
        }
    }

    // Initial health check
    checkHealth();
    setInterval(checkHealth, 5000);

    // Endpoint button clicks
    document.querySelectorAll('.endpoint-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            methodSelect.value = btn.dataset.method;
            urlInput.value = btn.dataset.path;

            // Set sample body for POST/PUT
            if (btn.dataset.method === 'POST' || btn.dataset.method === 'PUT') {
                if (btn.dataset.path.includes('/profile')) {
                    requestBody.value = JSON.stringify({
                        name: "John Doe",
                        email: "john@example.com",
                        title: "Software Developer",
                        bio: "Passionate about building great software"
                    }, null, 2);
                } else if (btn.dataset.path.includes('/experience')) {
                    requestBody.value = JSON.stringify({
                        profile_id: 1,
                        company: "Tech Corp",
                        position: "Senior Developer",
                        description: "Building awesome products",
                        start_date: "2022-01",
                        is_current: 1
                    }, null, 2);
                } else if (btn.dataset.path.includes('/projects')) {
                    requestBody.value = JSON.stringify({
                        profile_id: 1,
                        name: "My Project",
                        description: "A cool project",
                        tech_stack: "Python, FastAPI, React",
                        github_url: "https://github.com/user/project"
                    }, null, 2);
                }
            } else {
                requestBody.value = '';
            }
        });
    });

    // Send request
    sendBtn.addEventListener('click', async () => {
        const method = methodSelect.value;
        const url = `${baseUrlInput.value}${urlInput.value}`;

        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' }
        };

        if ((method === 'POST' || method === 'PUT') && requestBody.value.trim()) {
            options.body = requestBody.value;
        }

        const startTime = Date.now();

        try {
            const response = await fetch(url, options);
            const endTime = Date.now();
            const data = await response.json();

            const statusClass = response.ok ? 'success' : 'error';

            responseContent.innerHTML = `
                <div class="response-status">
                    <span class="status-code ${statusClass}">${response.status}</span>
                    <span style="color: var(--text-muted); font-size: 13px;">${endTime - startTime}ms</span>
                </div>
                <div class="response-body">
                    <pre>${syntaxHighlight(JSON.stringify(data, null, 2))}</pre>
                </div>
            `;
        } catch (e) {
            responseContent.innerHTML = `
                <div class="response-status">
                    <span class="status-code error">Error</span>
                </div>
                <div class="response-body">
                    <pre style="color: #ef4444;">${e.message}</pre>
                </div>
            `;
        }
    });

    // JSON syntax highlighting
    function syntaxHighlight(json) {
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
            match => {
                let cls = 'color: #c4b5fd'; // number
                if (/^"/.test(match)) {
                    cls = /:$/.test(match) ? 'color: #f472b6' : 'color: #a5f3fc'; // key : string
                } else if (/true|false/.test(match)) {
                    cls = 'color: #fcd34d'; // boolean
                } else if (/null/.test(match)) {
                    cls = 'color: #94a3b8'; // null
                }
                return `<span style="${cls}">${match}</span>`;
            }
        );
    }
});
