"""Sanity test for filter logic - run synthetic jobs through and verify expected outcomes."""
import yaml
from src.filters import JobFilter
from src.models import Job

cfg = yaml.safe_load(open("config.yaml"))
f = JobFilter(cfg)

# (job, expected_pass, reason)
test_cases = [
    # SHOULD PASS:
    (Job("Google", "1", "Data Scientist, Early Career", "New York, NY, USA", "url"), True,
     "early career + DS + US"),
    (Job("Anthropic", "2", "Machine Learning Engineer", "San Francisco, CA, USA", "url"), True,
     "ML engineer in CA"),
    (Job("JPMorgan", "3", "Associate Data Scientist", "New York, NY", "url"), True,
     "Associate + DS + NY"),
    (Job("Meta", "4", "Research Engineer - AI Integrity", "Menlo Park, California, United States", "url"), True,
     "research engineer + AI + US"),
    (Job("Tempus AI", "5", "Applied Scientist", "Chicago, IL", "url"), True,
     "applied scientist + chicago"),
    (Job("NVIDIA", "6", "Deep Learning Engineer, New Grad 2027", "Santa Clara, CA, USA", "url"), True,
     "deep learning + new grad + 2027"),
    (Job("Stripe", "7", "Data Scientist, Risk ML", "New York City, New York, US", "url"), True,
     "DS + risk ML + NY"),
    (Job("S&P Global", "8", "NLP Engineer - Associate", "New York, NY, USA", "url"), True,
     "NLP + associate + NY"),

    # SHOULD FAIL - seniority:
    (Job("Google", "10", "Senior Data Scientist", "New York, NY, USA", "url"), False,
     "senior in title"),
    (Job("Meta", "11", "Staff Machine Learning Engineer", "Menlo Park, CA, USA", "url"), False,
     "staff in title"),
    (Job("Apple", "12", "Principal Applied Scientist", "Cupertino, CA, USA", "url"), False,
     "principal in title"),
    (Job("Microsoft", "13", "Data Science Manager", "Redmond, WA, USA", "url"), False,
     "manager in title"),
    (Job("Amazon", "14", "Lead Data Engineer", "Seattle, WA, USA", "url"), False,
     "lead in title"),

    # SHOULD FAIL - wrong location:
    (Job("Google", "20", "Data Scientist", "London, UK", "url"), False,
     "non-US location"),
    (Job("Microsoft", "21", "ML Engineer", "Dublin, Ireland", "url"), False,
     "non-US location"),

    # SHOULD FAIL - irrelevant role:
    (Job("Amazon", "30", "Marketing Manager", "Seattle, WA, USA", "url"), False,
     "no DS/AI/ML keyword in title + manager"),
    (Job("Apple", "31", "iOS Engineer", "Cupertino, CA, USA", "url"), False,
     "no relevant keyword"),
    (Job("Meta", "32", "Recruiter, Tech Talent", "Menlo Park, CA, USA", "url"), False,
     "recruiter excluded"),
    (Job("Google", "33", "Software Engineering Intern", "Mountain View, CA, USA", "url"), False,
     "intern excluded"),
]

print(f"{'PASS/FAIL':<10} {'EXPECTED':<10} {'SCORE':<6} {'TITLE':<55} {'LOCATION':<35}")
print("-" * 120)
correct = 0
incorrect = 0
for job, expected, reason in test_cases:
    passed, score, bd = f.passes(job)
    status = "PASS" if passed else "FAIL"
    expected_s = "PASS" if expected else "FAIL"
    match = "✓" if passed == expected else "✗ WRONG"
    if passed == expected:
        correct += 1
    else:
        incorrect += 1
    print(f"{match:<10} {expected_s:<10} {score:<6} {job.title:<55} {job.location:<35}  ({reason})")

print("-" * 120)
print(f"Correct: {correct}/{len(test_cases)}   Incorrect: {incorrect}")
