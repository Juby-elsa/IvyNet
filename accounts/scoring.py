def calculate_incoscore(student_profile):
    """
    Logic to calculate the Intelligent Competency Score (InCoScore).
    Parameters: Hackathons, Internships, Research papers, Coding performance.
    """
    score = 0
    achievements = student_profile.achievements.all()
    
    weights = {
        'HACKATHON': 50,
        'INTERNSHIP': 100,
        'RESEARCH': 150,
        'COMPETITION': 40,
    }
    
    for ach in achievements:
        score += weights.get(ach.type, 20)
    
    # Add coding performance component
    score += (student_profile.coding_performance * 5)
    
    # Update profile
    student_profile.incoscore = score
    student_profile.save()
    return score
