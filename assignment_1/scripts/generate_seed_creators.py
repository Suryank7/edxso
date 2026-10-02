import json
import os

os.makedirs('packages/data', exist_ok=True)
os.makedirs('apps/api/data', exist_ok=True)
os.makedirs('apps/ai-service/data', exist_ok=True)

data = [
  # 1. Tech & AI Productivity (India) - Qualified
  {
    "creator_id": "cr_001",
    "name": "Rohan Sharma",
    "username": "rohan_techbytes",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/rohan_techbytes",
    "follower_count": 42500,
    "engagement_rate": 5.8,
    "category": "Technology",
    "niche": "AI & Productivity",
    "content_themes": ["AI productivity tools", "developer setups", "student workflows", "VS Code extensions"],
    "contact_email": "contact.rohansharma@gmail.com",
    "email_source": "public_profile",
    "email_confidence": "high",
    "website": "https://bento.me/rohantech",
    "audience_age": "18-24 (54%), 25-34 (32%)",
    "audience_gender": "70% Male, 30% Female",
    "audience_geography": "India (72%), United States (12%), Germany (4%)",
    "recent_content": [
      "Top 5 AI tools every computer science student needs",
      "How I automate my study schedule with Notion & AI",
      "Reviewing developer productivity gadgets"
    ],
    "discovery_source": "Instagram Public Directory",
    "posting_frequency": "4 reels / week",
    "brand_collaborations": ["Skillshare", "Notion Campus"]
  },
  # 2. YouTube Tech/AI - Qualified
  {
    "creator_id": "cr_002",
    "name": "Priya Patel",
    "username": "CodeWithPriya",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@CodeWithPriya",
    "follower_count": 68000,
    "engagement_rate": 4.6,
    "category": "Technology",
    "niche": "AI & Web Development",
    "content_themes": ["Full-stack tutorials", "AI coding assistants", "React best practices", "productivity hacks"],
    "contact_email": "priya.partnerships@codewithpriya.dev",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://codewithpriya.dev",
    "audience_age": "18-24 (46%), 25-34 (42%)",
    "audience_gender": "65% Male, 35% Female",
    "audience_geography": "India (65%), United States (15%), UK (6%)",
    "recent_content": [
      "Building a SaaS dashboard with AI in 30 minutes",
      "Cursor vs GitHub Copilot: Developer deep dive",
      "Productivity tools for engineering college students"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "2 videos / week",
    "brand_collaborations": ["Hostinger", "NordVPN"]
  },
  # 3. Instagram Productivity & Student Life - Qualified
  {
    "creator_id": "cr_003",
    "name": "Aarav Mehta",
    "username": "aarav.productive",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/aarav.productive",
    "follower_count": 28400,
    "engagement_rate": 6.2,
    "category": "Technology",
    "niche": "Student Productivity",
    "content_themes": ["Study workflows", "AI research tools", "time management", "digital note-taking"],
    "contact_email": "aarav.collabs@outlook.com",
    "email_source": "bio_link",
    "email_confidence": "high",
    "website": "https://aaravmehta.bio.link",
    "audience_age": "16-24 (78%), 25-34 (18%)",
    "audience_gender": "52% Male, 48% Female",
    "audience_geography": "India (82%), Singapore (5%), UAE (4%)",
    "recent_content": [
      "3 AI tools to summarize research papers in seconds",
      "My iPad digital study setup for 2026",
      "Deep work protocol for engineering exams"
    ],
    "discovery_source": "Hashtag Search #productivitytools",
    "posting_frequency": "5 reels / week",
    "brand_collaborations": ["Paperlike"]
  },
  # 4. Tech YouTube - Low Engagement (FAIL Test Case)
  {
    "creator_id": "cr_004",
    "name": "Vikram Verma",
    "username": "VikramTechLabs",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@VikramTechLabs",
    "follower_count": 55000,
    "engagement_rate": 1.8,
    "category": "Technology",
    "niche": "Hardware & PC Tech",
    "content_themes": ["PC builds", "smartphone benchmarks", "cooling systems"],
    "contact_email": "vikram.business@gmail.com",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "Not Found",
    "audience_age": "18-34 (70%)",
    "audience_gender": "88% Male, 12% Female",
    "audience_geography": "India (75%), Pakistan (10%)",
    "recent_content": [
      "Budget gaming PC build in 2026",
      "Testing budget cooling fans",
      "Unboxing new smartphone"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "1 video / week",
    "brand_collaborations": []
  },
  # 5. Technology - Missing Email (Unverified / Missing Email Test Case)
  {
    "creator_id": "cr_005",
    "name": "Neha Deshmukh",
    "username": "neha_codes_daily",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/neha_codes_daily",
    "follower_count": 19200,
    "engagement_rate": 4.1,
    "category": "Technology",
    "niche": "Software Engineering",
    "content_themes": ["Python tips", "Leetcode problem solving", "tech interview preparation"],
    "contact_email": "Not Found",
    "email_source": "not_found",
    "email_confidence": "not_found",
    "website": "https://github.com/nehadeshmukh",
    "audience_age": "18-24 (62%), 25-34 (30%)",
    "audience_gender": "58% Male, 42% Female",
    "audience_geography": "India (85%), United States (8%)",
    "recent_content": [
      "Daily Python snippet: generators vs iterators",
      "5 tips to crack coding interviews",
      "My remote software engineer morning routine"
    ],
    "discovery_source": "Instagram Public Directory",
    "posting_frequency": "3 reels / week",
    "brand_collaborations": []
  },
  # 6. Fashion & Lifestyle (Non-tech Niche FAIL Test Case)
  {
    "creator_id": "cr_006",
    "name": "Simran Kaur",
    "username": "simran_styles",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/simran_styles",
    "follower_count": 48000,
    "engagement_rate": 5.2,
    "category": "Fashion & Beauty",
    "niche": "Sustainable Fashion",
    "content_themes": ["Thrift styling", "capsule wardrobe", "skincare routines"],
    "contact_email": "collabs.simran@gmail.com",
    "email_source": "public_profile",
    "email_confidence": "high",
    "website": "https://simranstyles.com",
    "audience_age": "18-24 (45%), 25-34 (40%)",
    "audience_gender": "20% Male, 80% Female",
    "audience_geography": "India (80%), UAE (10%)",
    "recent_content": [
      "5 ways to style one oversized blazer",
      "Morning skincare routine under 10 minutes",
      "Thrifting in Delhi haul"
    ],
    "discovery_source": "Creator Marketplace",
    "posting_frequency": "4 reels / week",
    "brand_collaborations": ["Nykaa", "Zara"]
  },
  # 7. Follower Count Over Limit (FAIL Test Case - Macro influencer)
  {
    "creator_id": "cr_007",
    "name": "Aditya Sen",
    "username": "tech_aditya_official",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@tech_aditya_official",
    "follower_count": 320000,
    "engagement_rate": 3.5,
    "category": "Technology",
    "niche": "Consumer Tech",
    "content_themes": ["Flagship phone reviews", "laptop comparisons", "gadget tear-downs"],
    "contact_email": "aditya.partnerships@techaditya.in",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://techaditya.in",
    "audience_age": "18-34 (75%)",
    "audience_gender": "75% Male, 25% Female",
    "audience_geography": "India (88%)",
    "recent_content": [
      "iPhone 16 Pro 6 months later",
      "Best laptops for college students 2026",
      "Why I switched back to Android"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "3 videos / week",
    "brand_collaborations": ["Samsung", "Lenovo"]
  },
  # 8. Follower Count Below Limit (FAIL Test Case - Nano influencer)
  {
    "creator_id": "cr_008",
    "name": "Manish Kulkarni",
    "username": "manish_writes_code",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/manish_writes_code",
    "follower_count": 3200,
    "engagement_rate": 6.8,
    "category": "Technology",
    "niche": "AI & Productivity",
    "content_themes": ["Python automation", "AI tools", "command line tricks"],
    "contact_email": "manishkulkarni.dev@gmail.com",
    "email_source": "bio_link",
    "email_confidence": "medium",
    "website": "https://manish.hashnode.dev",
    "audience_age": "18-24 (70%)",
    "audience_gender": "75% Male, 25% Female",
    "audience_geography": "India (90%)",
    "recent_content": [
      "Automating email cleaning with Python",
      "Top 3 AI terminal tools",
      "My weekly study setup"
    ],
    "discovery_source": "Hashtag Search",
    "posting_frequency": "2 reels / week",
    "brand_collaborations": []
  },
  # 9. Kavya Nair
  {
    "creator_id": "cr_009",
    "name": "Kavya Nair",
    "username": "KavyaBuildsTech",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@KavyaBuildsTech",
    "follower_count": 34200,
    "engagement_rate": 5.4,
    "category": "Technology",
    "niche": "AI Tools & Productivity",
    "content_themes": ["No-code AI agents", "LLM workflows", "personal knowledge management", "Obsidian tutorials"],
    "contact_email": "kavya@buildstech.io",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://buildstech.io",
    "audience_age": "20-30 (60%), 31-40 (25%)",
    "audience_gender": "60% Male, 40% Female",
    "audience_geography": "India (68%), United States (18%), UK (5%)",
    "recent_content": [
      "How I use AI to read 4 books a month",
      "Build your personal AI assistant without coding",
      "Obsidian + AI second brain blueprint"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "2 videos / week",
    "brand_collaborations": ["Heptabase", "Readwise"]
  },
  # 10. Devansh Agarwal
  {
    "creator_id": "cr_010",
    "name": "Devansh Agarwal",
    "username": "devansh_ai_hacks",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/devansh_ai_hacks",
    "follower_count": 51000,
    "engagement_rate": 4.9,
    "category": "Technology",
    "niche": "AI & Productivity",
    "content_themes": ["Prompt engineering", "Generative AI workflows", "student productivity tools", "Chrome extensions"],
    "contact_email": "devansh.collabs@gmail.com",
    "email_source": "public_profile",
    "email_confidence": "high",
    "website": "https://devanshai.bio.link",
    "audience_age": "18-24 (65%), 25-34 (28%)",
    "audience_gender": "68% Male, 32% Female",
    "audience_geography": "India (78%), United States (10%)",
    "recent_content": [
      "Stop writing prompts like this: 3 prompt templates that actually work",
      "The best AI extension for Google Docs in 2026",
      "How students can prepare for exam week in 2 days with AI"
    ],
    "discovery_source": "Hashtag Search #promptengineering",
    "posting_frequency": "5 reels / week",
    "brand_collaborations": ["Gamma App", "Otter.ai"]
  },
  # 11. Tanvi Singhal
  {
    "creator_id": "cr_011",
    "name": "Tanvi Singhal",
    "username": "tanvi_techdiary",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/tanvi_techdiary",
    "follower_count": 16500,
    "engagement_rate": 6.5,
    "category": "Technology",
    "niche": "Developer Lifestyle & Productivity",
    "content_themes": ["Desk setup inspiration", "Mac productivity tips", "remote work routines", "junior dev advice"],
    "contact_email": "tanvi.partnerships@techdiary.co",
    "email_source": "bio_link",
    "email_confidence": "high",
    "website": "https://techdiary.co",
    "audience_age": "18-24 (50%), 25-34 (40%)",
    "audience_gender": "48% Male, 52% Female",
    "audience_geography": "India (70%), United States (15%), Canada (5%)",
    "recent_content": [
      "Top 4 Mac apps that doubled my engineering output",
      "What I pack in my tech backpack as a hybrid developer",
      "My Sunday reset for a productive sprint"
    ],
    "discovery_source": "Instagram Creator Directory",
    "posting_frequency": "3 reels / week",
    "brand_collaborations": ["Keychron", "Autonomous"]
  },
  # 12. Harshvardhan Rao
  {
    "creator_id": "cr_012",
    "name": "Harshvardhan Rao",
    "username": "CodeFlowHarsh",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@CodeFlowHarsh",
    "follower_count": 82000,
    "engagement_rate": 3.8,
    "category": "Technology",
    "niche": "DevOps & Cloud Tools",
    "content_themes": ["Docker tutorials", "Kubernetes automation", "CI/CD pipelines", "developer workflows"],
    "contact_email": "contact@codeflowharsh.com",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://codeflowharsh.com",
    "audience_age": "22-35 (80%)",
    "audience_gender": "85% Male, 15% Female",
    "audience_geography": "India (60%), United States (20%), Germany (8%)",
    "recent_content": [
      "Deploying Next.js on AWS with Docker in 10 minutes",
      "Modern developer workflow: terminal tips and tricks",
      "Automate code reviews with AI GitHub actions"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "1 video / week",
    "brand_collaborations": ["DigitalOcean", "Datadog"]
  },
  # 13. Ananya Joshi
  {
    "creator_id": "cr_013",
    "name": "Ananya Joshi",
    "username": "ananya.studies.ai",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/ananya.studies.ai",
    "follower_count": 23400,
    "engagement_rate": 7.1,
    "category": "Technology",
    "niche": "Student Productivity & AI",
    "content_themes": ["Study with me", "AI flashcards", "Cornell notes system", "focus sprints"],
    "contact_email": "ananya.studies@gmail.com",
    "email_source": "public_profile",
    "email_confidence": "high",
    "website": "https://ananyastudies.notion.site",
    "audience_age": "16-24 (85%)",
    "audience_gender": "40% Male, 60% Female",
    "audience_geography": "India (84%), United Kingdom (6%)",
    "recent_content": [
      "How I use AI to turn lecture slides into active recall quizzes",
      "Pomodoro technique vs Flowmodoro for long study sessions",
      "5 secret Chrome extensions for college students"
    ],
    "discovery_source": "Hashtag Search #studytok",
    "posting_frequency": "4 reels / week",
    "brand_collaborations": ["Quizlet", "Forest App"]
  },
  # 14. Rahul Nambiar
  {
    "creator_id": "cr_014",
    "name": "Rahul Nambiar",
    "username": "RahulProductivity",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@RahulProductivity",
    "follower_count": 41000,
    "engagement_rate": 4.4,
    "category": "Technology",
    "niche": "Productivity Systems",
    "content_themes": ["Time management", "Notion systems", "GTD method", "AI productivity stacks"],
    "contact_email": "rahul@rahulproductivity.in",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://rahulproductivity.in",
    "audience_age": "20-35 (72%)",
    "audience_gender": "65% Male, 35% Female",
    "audience_geography": "India (68%), United States (14%), Australia (5%)",
    "recent_content": [
      "The ultimate AI productivity stack for solo founders",
      "Why most to-do list apps fail you (and what works)",
      "Organizing my entire year inside Notion"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "2 videos / week",
    "brand_collaborations": ["Todoist", "TickTick"]
  },
  # 15. Siddharth Roy
  {
    "creator_id": "cr_015",
    "name": "Siddharth Roy",
    "username": "siddharth_dev_ai",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/siddharth_dev_ai",
    "follower_count": 38900,
    "engagement_rate": 5.1,
    "category": "Technology",
    "niche": "AI & Web Development",
    "content_themes": ["Full-stack tips", "AI tool reviews", "Next.js tutorials", "freelancing for developers"],
    "contact_email": "siddharth.roy.biz@gmail.com",
    "email_source": "public_profile",
    "email_confidence": "high",
    "website": "https://siddharthroy.tech",
    "audience_age": "18-28 (75%)",
    "audience_gender": "78% Male, 22% Female",
    "audience_geography": "India (76%), United States (12%)",
    "recent_content": [
      "I built a full-stack AI web app in 2 hours with this framework",
      "3 tools that save me 10 hours of manual coding each week",
      "How to get your first remote dev client in 2026"
    ],
    "discovery_source": "Creator Marketplace",
    "posting_frequency": "4 reels / week",
    "brand_collaborations": ["Vercel Community", "Supabase"]
  },
  # 16. Meera Pillai
  {
    "creator_id": "cr_016",
    "name": "Meera Pillai",
    "username": "meera_designs_tech",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/meera_designs_tech",
    "follower_count": 21800,
    "engagement_rate": 5.9,
    "category": "Technology",
    "niche": "UI/UX & Product Design",
    "content_themes": ["Figma AI plugins", "design system architecture", "product design workflows", "SaaS UX audits"],
    "contact_email": "meera@meeradesign.in",
    "email_source": "bio_link",
    "email_confidence": "high",
    "website": "https://meeradesign.in",
    "audience_age": "20-30 (68%)",
    "audience_gender": "45% Male, 55% Female",
    "audience_geography": "India (70%), UK (12%), US (10%)",
    "recent_content": [
      "5 AI Figma plugins that feel illegal to know",
      "Redesigning bad SaaS onboarding screens",
      "How to organize design tokens like a pro"
    ],
    "discovery_source": "Instagram Public Directory",
    "posting_frequency": "3 reels / week",
    "brand_collaborations": ["Figma Community", "Mobbin"]
  },
  # 17. Arjun Vats
  {
    "creator_id": "cr_017",
    "name": "Arjun Vats",
    "username": "TechWithArjunVats",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@TechWithArjunVats",
    "follower_count": 92000,
    "engagement_rate": 3.4,
    "category": "Technology",
    "niche": "Tech Reviews & Software Tutorials",
    "content_themes": ["Software productivity", "Windows power toys", "useful web apps", "gadget reviews"],
    "contact_email": "arjun.partnerships@vatsmedia.in",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://vatsmedia.in",
    "audience_age": "18-35 (70%)",
    "audience_gender": "80% Male, 20% Female",
    "audience_geography": "India (82%), UAE (6%)",
    "recent_content": [
      "Top 10 hidden Windows 11 productivity features",
      "The best free software you are not using",
      "How I organize my multi-monitor desk setup"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "2 videos / week",
    "brand_collaborations": ["Logitech", "Wondershare"]
  },
  # 18. Pooja Bhatia
  {
    "creator_id": "cr_018",
    "name": "Pooja Bhatia",
    "username": "pooja_techcareer",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/pooja_techcareer",
    "follower_count": 31500,
    "engagement_rate": 4.8,
    "category": "Technology",
    "niche": "Tech Careers & Productivity",
    "content_themes": ["Resume optimization", "AI interview prep", "internship guides", "productivity schedules"],
    "contact_email": "collabs@poojabhatia.in",
    "email_source": "public_profile",
    "email_confidence": "high",
    "website": "https://topmate.io/poojabhatia",
    "audience_age": "18-26 (82%)",
    "audience_gender": "55% Male, 45% Female",
    "audience_geography": "India (86%), US (6%)",
    "recent_content": [
      "How college students can land tech internships with AI tools",
      "3 tools to practice live coding interviews",
      "My 9-to-5 plus side project daily calendar"
    ],
    "discovery_source": "Hashtag Search #techcareers",
    "posting_frequency": "4 reels / week",
    "brand_collaborations": ["Topmate", "Unstop"]
  },
  # 19. Deepak Singhania
  {
    "creator_id": "cr_019",
    "name": "Deepak Singhania",
    "username": "deepak_automates",
    "platform": "Instagram",
    "profile_url": "https://instagram.com/deepak_automates",
    "follower_count": 14200,
    "engagement_rate": 6.0,
    "category": "Technology",
    "niche": "Automation & AI Workflows",
    "content_themes": ["Zapier workflows", "Make.com tutorials", "n8n open source setups", "business automation"],
    "contact_email": "deepak@automategrowth.in",
    "email_source": "bio_link",
    "email_confidence": "high",
    "website": "https://automategrowth.in",
    "audience_age": "22-35 (74%)",
    "audience_gender": "72% Male, 28% Female",
    "audience_geography": "India (65%), US (20%), UK (7%)",
    "recent_content": [
      "Automating client onboarding with n8n and AI",
      "How I replaced 3 virtual assistants with smart AI scripts",
      "Build an automatic meeting summarizer in 15 mins"
    ],
    "discovery_source": "Instagram Creator Directory",
    "posting_frequency": "3 reels / week",
    "brand_collaborations": ["Make.com", "Airtable"]
  },
  # 20. Ishan Mukherjee
  {
    "creator_id": "cr_020",
    "name": "Ishan Mukherjee",
    "username": "ishan_codes",
    "platform": "YouTube",
    "profile_url": "https://youtube.com/@ishan_codes",
    "follower_count": 47500,
    "engagement_rate": 4.7,
    "category": "Technology",
    "niche": "Competitive Programming & AI",
    "content_themes": ["DSA algorithms", "AI code generation", "system design for students", "productivity"],
    "contact_email": "ishan.codes.business@gmail.com",
    "email_source": "youtube_about",
    "email_confidence": "high",
    "website": "https://ishancodes.dev",
    "audience_age": "18-24 (76%), 25-30 (18%)",
    "audience_gender": "80% Male, 20% Female",
    "audience_geography": "India (82%), US (9%)",
    "recent_content": [
      "Can AI solve hard LeetCode problems faster than Grandmasters?",
      "Master dynamic programming in 7 days",
      "My VS Code configuration for maximum speed"
    ],
    "discovery_source": "YouTube Data API",
    "posting_frequency": "2 videos / week",
    "brand_collaborations": ["AlgoMonster", "Brilliant"]
  }
]

# Additional 32 creators to reach 52 total
creators_batch_2 = [
  ("Shreya Bansal", "shreya_studytech", "Instagram", 18500, 5.7, "Student Productivity", "Technology", "shreya.collabs@gmail.com", "public_profile", "high", "India (80%)", ["How I organize college notes with AI", "Study sprint with me for finals"]),
  ("Gaurav Tiwari", "gaurav_dev_ops", "YouTube", 53000, 3.9, "Cloud & DevOps", "Technology", "gaurav@tiwaritech.com", "youtube_about", "high", "India (68%), US (16%)", ["Kubernetes for beginner developers", "Top CI/CD productivity tools"]),
  ("Alisha Mirza", "alisha_ai_design", "Instagram", 27000, 6.1, "AI & UI Design", "Technology", "alisha.mirza.biz@outlook.com", "bio_link", "high", "India (70%), UK (12%)", ["Generative UI components in Figma", "AI tools transforming web design"]),
  ("Karthik Reddy", "karthik_techspot", "YouTube", 74000, 4.2, "Tech & Gadgets", "Technology", "karthik.reddy@techspotmedia.com", "youtube_about", "high", "India (84%)", ["Best student tablets for digital notes", "AI software every engineer should test"]),
  ("Sneha Chawla", "sneha_productivity", "Instagram", 33000, 5.3, "Productivity Systems", "Technology", "sneha@productiveclub.in", "public_profile", "high", "India (75%), UAE (8%)", ["My morning routine for 4 hours of deep focus", "Testing popular task management apps"]),
  ("Pranav Dixit", "pranav_builds_ai", "YouTube", 62000, 4.5, "AI Engineering", "Technology", "pranav.dixit@buildsai.dev", "youtube_about", "high", "India (65%), US (20%)", ["Fine-tuning local LLMs with Ollama", "AI agent architectures explained simply"]),
  ("Divya Nair", "divya_notionqueen", "Instagram", 41200, 6.4, "Productivity & Notion", "Technology", "divya@notionqueen.com", "bio_link", "high", "India (62%), US (22%)", ["Free aesthetic Notion template for university students", "How AI automates my life planner"]),
  ("Aman Gill", "aman_git_push", "Instagram", 15800, 5.0, "Web Development", "Technology", "Not Found", "not_found", "not_found", "India (82%)", ["Top 5 Git commands you need daily", "Fixing common React re-render bugs"]),
  ("Riya Sen", "riya_glow_lifestyle", "Instagram", 59000, 5.1, "Beauty & Wellness", "Fashion & Beauty", "riya.glow@gmail.com", "public_profile", "high", "India (82%)", ["5-step morning glass skin routine", "Affordable sunscreens for summer"]),
  ("Varun Kapoor", "varun_fit_coach", "YouTube", 44000, 4.0, "Fitness & Calisthenics", "Fitness", "varun@fitcoachkapoor.com", "youtube_about", "high", "India (85%)", ["Beginner calisthenics routine", "High protein meal prep for busy professionals"]),
  ("Nikhil Chopra", "nikhil_techtips", "Instagram", 87000, 3.2, "Consumer Software", "Technology", "nikhil@techtipsindia.com", "public_profile", "high", "India (88%)", ["Secret Android productivity settings", "Windows tools that will blow your mind"]),
  ("Tanya Joseph", "tanya_learns_code", "YouTube", 29000, 5.5, "Learn to Code", "Technology", "tanya.joseph.dev@gmail.com", "youtube_about", "high", "India (74%), US (14%)", ["How I learned JavaScript in 90 days", "Best AI tools for coding beginners"]),
  ("Kunal Saxena", "kunal_data_ai", "Instagram", 36000, 4.9, "Data Science & AI", "Technology", "kunal.saxena@datasciencehub.in", "bio_link", "high", "India (70%), US (18%)", ["Pandas vs Polars benchmark", "Using ChatGPT for exploratory data analysis"]),
  ("Pallavi Joshi", "pallavi_workmode", "Instagram", 22500, 6.3, "Productivity & Habits", "Technology", "pallavi.workmode@outlook.com", "public_profile", "high", "India (78%)", ["How to overcome procrastination using atomic habits", "AI tools for organizing thesis research"]),
  ("Tarun Bhat", "tarun_prompt_wizard", "YouTube", 38000, 4.8, "Prompt Engineering & AI", "Technology", "tarun@promptwizard.ai", "youtube_about", "high", "India (66%), US (18%)", ["Mastering Claude 3.5 Sonnet artifacts", "Automating daily research workflows with AI"]),
  ("Ankit Verma", "ankit_webdev", "Instagram", 12400, 5.2, "Frontend Dev", "Technology", "ankit.verma.code@gmail.com", "bio_link", "medium", "India (85%)", ["Tailwind CSS vs Vanilla CSS in 2026", "Building micro-interactions that impress"]),
  ("Bhavna Rao", "bhavna_tech_hub", "YouTube", 89000, 3.6, "Tech Reviews", "Technology", "bhavna@techhubmedia.in", "youtube_about", "high", "India (80%)", ["Best budget laptops for programming", "Top software tools every creator needs"]),
  ("Chetan Parekh", "chetan_software_pro", "Instagram", 46000, 4.3, "Software Architecture", "Technology", "chetan.parekh@gmail.com", "public_profile", "high", "India (72%), US (16%)", ["Microservices vs Monoliths real world trade-offs", "How AI changes engineering team productivity"]),
  ("Zoya Akhtar", "zoya_ai_research", "YouTube", 31000, 5.9, "AI Research & Summaries", "Technology", "zoya@airesearchlab.org", "youtube_about", "high", "India (60%), US (25%)", ["Deep dive into Transformer architectures", "Top AI breakthroughs this month"]),
  ("Rajesh Guha", "rajesh_tech_hacks", "Instagram", 105000, 2.9, "Tech Hacks", "Technology", "rajesh.guha@gmail.com", "public_profile", "high", "India (92%)", ["10 phone shortcuts nobody knows", "Fastest way to charge your laptop"]),
  ("Simi Thomas", "simi_remote_work", "Instagram", 26500, 5.8, "Remote Work & Productivity", "Technology", "simi.thomas@remoteworkers.in", "bio_link", "high", "India (68%), UK (15%)", ["My asynchronous remote work setup", "AI tools that save 2 hours of Zoom calls"]),
  ("Omkar Jadhav", "omkar_codes_cpp", "YouTube", 49000, 4.1, "C++ & Systems", "Technology", "omkar.jadhav.cpp@gmail.com", "youtube_about", "high", "India (84%)", ["Modern C++23 features in 20 minutes", "High performance computing workflows"]),
  ("Natasha Malik", "natasha_minimalist_desk", "Instagram", 37500, 6.0, "Minimalism & Productivity", "Technology", "natasha@minimalistwork.com", "public_profile", "high", "India (64%), US (20%)", ["Minimalist desk tour 2026", "Digital decluttering: how I cleared 500GB"]),
  ("Vineet Aggarwal", "vineet_ai_builder", "Instagram", 19800, 5.4, "AI Agents & Automation", "Technology", "vineet@builderai.in", "bio_link", "high", "India (75%), US (14%)", ["Building multi-agent systems with LangGraph", "How I built an automated research assistant"]),
  ("Geetika Sondhi", "geetika_tech_student", "Instagram", 24800, 6.6, "Student Engineering Life", "Technology", "geetika.sondhi@gmail.com", "public_profile", "high", "India (88%)", ["A day in the life of a female CS student", "My favorite AI note-taking and revision tools"]),
  ("Ayush Srivastava", "ayush_linux_dev", "YouTube", 64000, 4.4, "Linux & Open Source", "Technology", "ayush@linuxdev.in", "youtube_about", "high", "India (72%), Germany (10%)", ["Why I switched to Arch Linux for development", "Command line tools that make you feel like a hacker"]),
  ("Kriti Mehra", "kriti_crafts_diy", "Instagram", 52000, 4.7, "DIY & Home Decor", "Lifestyle", "kriti.crafts@gmail.com", "public_profile", "high", "India (86%)", ["Aesthetic desk decor DIY under 500", "Handmade room makeover ideas"]),
  ("Lokesh Yadav", "lokesh_ai_insights", "Instagram", 32000, 5.2, "AI Insights & Industry", "Technology", "lokesh@aiinsights.co", "bio_link", "high", "India (78%), US (12%)", ["5 AI tools reshaping software engineering jobs", "Prompt chains for automated market research"]),
  ("Trisha Sengupta", "trisha_study_space", "Instagram", 28900, 6.1, "Study Space & Productivity", "Technology", "trisha.collabs@outlook.com", "public_profile", "high", "India (82%)", ["Quiet study with me 3-hour pomodoro", "The best iPad pencil tips for digital writing"]),
  ("Mayank Goyal", "mayank_cyber_sec", "YouTube", 58000, 3.8, "Cybersecurity & Security", "Technology", "mayank@cyberseclabs.in", "youtube_about", "high", "India (80%), US (10%)", ["How hackers steal credentials with phishing", "Essential security tools for developers"]),
  ("Jasleen Vohra", "jasleen_tech_interviews", "Instagram", 41500, 5.0, "Interview Prep & Career", "Technology", "jasleen.vohra.partners@gmail.com", "public_profile", "high", "India (84%)", ["Behavioral interview framework that never fails", "How to negotiate remote software engineering offers"]),
  ("Suraj Rathi", "suraj_cloud_architect", "YouTube", 72000, 4.0, "Cloud Architecture", "Technology", "suraj@cloudarchitectpro.com", "youtube_about", "high", "India (65%), US (22%)", ["AWS Serverless vs Traditional Containers", "My daily workflow as a Principal Cloud Architect"])
]

start_id = 21
for item in creators_batch_2:
    cid = f"cr_{start_id:03d}"
    start_id += 1
    themes = [item[5].lower(), "developer productivity", "workflow automation", "software tools"]
    clean_handle = item[1].replace(".", "").replace("_", "")
    record = {
        "creator_id": cid,
        "name": item[0],
        "username": item[1],
        "platform": item[2],
        "profile_url": f"https://youtube.com/@{item[1]}" if item[2] == "YouTube" else f"https://instagram.com/{item[1]}",
        "follower_count": item[3],
        "engagement_rate": item[4],
        "category": item[6],
        "niche": item[5],
        "content_themes": themes,
        "contact_email": item[7],
        "email_source": item[8],
        "email_confidence": item[9],
        "website": f"https://{clean_handle}.dev" if item[7] != "Not Found" else "Not Found",
        "audience_age": "18-24 (60%), 25-34 (30%)",
        "audience_gender": "65% Male, 35% Female",
        "audience_geography": item[10],
        "recent_content": item[11],
        "discovery_source": f"{item[2]} Public Discovery",
        "posting_frequency": "3 posts / week",
        "brand_collaborations": ["Notion", "Skillshare"] if item[3] > 30000 else []
    }
    data.append(record)

print(f"Total creators assembled: {len(data)}")

targets = [
    "packages/data/creators_seed.json",
    "apps/api/data/creators_seed.json",
    "apps/ai-service/data/creators_seed.json"
]

for target in targets:
    with open(target, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {target} ({len(data)} creators)")
