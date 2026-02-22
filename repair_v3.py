import os

def write_template(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip())
    print(f"Successfully wrote {path}")

# Feed Template
feed_content = """{% extends 'base.html' %}
{% block content %}
<div class="row mb-5 animate-fade-in">
    <div class="col-lg-8">
        <h1 class="display-4 fw-bold mb-3 text-dark">Ivy League <span style="color: #007bff;">Opportunities</span></h1>
        <p class="lead text-secondary">Real-time intelligence monitoring of the world's most prestigious universities.</p>
    </div>
    <div class="col-lg-4 d-flex align-items-center justify-content-end">
        <a href="{% url 'refresh_opportunities' %}" class="btn btn-outline-primary py-2 px-4 rounded-pill">
            <i class="bi bi-arrow-clockwise me-1"></i> Refresh Feed
        </a>
    </div>
</div>

<div class="row">
    {% for opp in opportunities %}
    <div class="col-md-6 mb-4">
        <div class="bg-white p-4 h-100 d-flex flex-column rounded-4 border shadow-sm">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2">{{ opp.get_domain_display|default:opp.domain }}</span>
                <small class="text-muted fw-bold">{{ opp.posted_date|date:"M d, Y" }}</small>
            </div>
            <h3 class="h4 fw-bold mb-2 text-dark">{{ opp.title }}</h3>
            <p class="fw-bold mb-3 text-primary">{{ opp.university.name }}</p>
            <p class="text-secondary small mb-4 flex-grow-1">{{ opp.description|truncatewords:45 }}</p>

            <div class="d-flex justify-content-between align-items-center mt-auto pt-3 border-top">
                <small class="fw-bold text-muted">Deadline: {{ opp.deadline|date:"M d, Y"|default:"TBA" }}</small>
                <div class="d-flex gap-2">
                    <a href="{{ opp.link }}" target="_blank" class="btn btn-outline-secondary btn-sm px-3 rounded-pill">Source</a>
                    <a href="{% url 'apply_opportunity' opp.pk %}" class="btn btn-primary btn-sm px-3 rounded-pill">Apply</a>
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <div class="bg-white p-5 rounded-4 border border-dashed">
            <h3 class="text-secondary">No current opportunities available.</h3>
            <p class="text-muted">Click the Refresh Feed button to fetch the latest academic events.</p>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}"""

# Shortlist Template
shortlist_content = """{% extends 'base.html' %}
{% block content %}
<div class="row mb-5 animate-fade-in">
    <div class="col-lg-12">
        <h1 class="display-5 fw-bold mb-3 text-dark">Smart <span style="color: #007bff;">Shortlisting</span></h1>
        <p class="lead text-secondary">AI-powered candidate shortlisting for <span class="fw-bold text-primary">{{ domain_display }}</span> institutions.</p>
    </div>
</div>

<div class="row mb-4">
    <div class="col-lg-12">
        <div class="bg-white p-4 rounded-4 border shadow-sm mb-5">
            <form method="GET" class="row g-3 align-items-center">
                <div class="col-auto"><label class="fw-bold text-muted small text-uppercase">Filter Domain:</label></div>
                <div class="col-auto">
                    <select name="domain" class="form-select border-secondary-subtle">
                        <option value="AI" {% if domain == 'AI' %}selected{% endif %}>AI / ML</option>
                        <option value="LAW" {% if domain == 'LAW' %}selected{% endif %}>Law</option>
                        <option value="BIO" {% if domain == 'BIO' %}selected{% endif %}>Biomedical</option>
                        <option value="ENG" {% if domain == 'ENG' %}selected{% endif %}>Engineering</option>
                    </select>
                </div>
                <div class="col-auto"><button type="submit" class="btn btn-primary px-4 rounded-pill">Generate Shortlist</button></div>
            </form>
        </div>
    </div>
</div>

<div class="row">
    {% for student in top_candidates %}
    <div class="col-lg-6 mb-4">
        <div class="bg-white p-4 h-100 d-flex align-items-center rounded-4 border shadow-sm">
            <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold h3 mb-0 me-4" style="width: 70px; height: 70px;">{{ student.user.username|first|upper }}</div>
            <div class="flex-grow-1">
                <div class="d-flex justify-content-between align-items-start">
                    <h5 class="fw-bold text-dark mb-1">{{ student.user.get_full_name|default:student.user.username }}</h5>
                    <span class="badge bg-primary-subtle text-primary border border-primary-subtle">Rank #{{ forloop.counter }}</span>
                </div>
                <p class="mb-3 text-secondary">InCoScore: <span class="fw-bold text-primary">{{ student.incoscore }}</span></p>
                <div class="d-flex gap-2">
                    <a href="{% url 'profile' %}" class="btn btn-sm btn-primary px-4 rounded-pill">View Profile</a>
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <div class="bg-white p-5 rounded-4 border border-dashed">
            <h4 class="text-muted">No candidates found for this domain yet.</h4>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}"""

# Login Template
login_content = """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center py-5 animate-fade-in">
    <div class="col-md-5">
        <div class="bg-white p-5 rounded-4 border shadow-sm">
            <h2 class="fw-bold mb-4 text-center">Login to <span class="text-primary">IvyNet</span></h2>
            <form method="POST">
                {% csrf_token %}
                <div class="mb-3">
                    <label class="form-label fw-bold text-muted small">Username</label>
                    <input type="text" name="username" class="form-control rounded-3" placeholder="Enter your username" required>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-bold text-muted small">Password</label>
                    <input type="password" name="password" class="form-control rounded-3" placeholder="Enter password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-bold">Sign In</button>
            </form>
            <div class="mt-4 text-center">
                <p class="text-secondary small">Don't have an account? <a href="#" class="text-primary fw-bold text-decoration-none">Join the network</a></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

# Leaderboard Template
leaderboard_content = """{% extends 'base.html' %}
{% block content %}
<div class="row mb-5 animate-fade-in">
    <div class="col-lg-12">
        <h1 class="display-4 fw-bold mb-3 text-dark">Global <span style="color: #007bff;">Leaderboard</span></h1>
        <p class="lead text-secondary">The definitive ranking of top students based on real-world academic excellence.</p>
    </div>
</div>

<div class="row">
    <div class="col-lg-12">
        <div class="bg-white rounded-4 border shadow-sm overflow-hidden">
            <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                    <tr><th class="ps-4">Rank</th><th>Student</th><th>Domain</th><th class="text-center">InCoScore</th><th class="pe-4 text-end">Action</th></tr>
                </thead>
                <tbody>
                    {% for student in top_students %}
                    <tr>
                        <td class="ps-4"><span class="fw-bold h5">#{{ forloop.counter }}</span></td>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px;">{{ student.user.username|first|upper }}</div>
                                <span class="fw-bold text-dark">{{ student.user.username }}</span>
                            </div>
                        </td>
                        <td><span class="badge bg-light text-dark border">{{ student.get_domain_interest_display }}</span></td>
                        <td class="text-center fw-bold text-primary h5">{{ student.incoscore }}</td>
                        <td class="pe-4 text-end"><a href="{% url 'profile' %}" class="btn btn-sm btn-outline-primary rounded-pill px-4">View</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""

write_template('templates_secure/opportunities/feed.html', feed_content)
write_template('templates_secure/opportunities/shortlist.html', shortlist_content)
write_template('templates_secure/accounts/login.html', login_content)
write_template('templates_secure/accounts/leaderboard.html', leaderboard_content)
