from enum import Enum

class UseCase(Enum):
    YoutubeIdea = 1,
    YoutubeDescription = 2,
    YoutubeChannelDescription = 3,
    TestimonialAndReview = 4,
    TagLineAndHeadline = 5,
    StoryPlots = 6,
    SongLyrics = 7,
    SmsAndNotifications = 8,
    EmailSubjectLine = 9,
    JobDescription = 10,
    BlogIdeaAndOutline= 11,
    CoverLetter = 12,
    ProfileBio=13,
    ReplyToReviewsAndMessages = 14,
    GrammarCorrection = 15,
    BusinessIdea = 16,
    BusinessIdeaPitch = 17,
    Citation = 18,
    CopywritingFrameworkAIDA = 19,
    GoogleSearchAd = 20,
    InterviewQuestions = 21,
    KeywordsExtractor = 22,
    LandingPage = 23, 
    ParaphraseText = 24,
    PostAndCaptionIdea = 25,
    ProductDescriptionWithBulletPoints = 26,
    ProductDescription = 27,
    SeoMetaTitle = 28,
    GenerateCallToAction = 29,
    GenerateBrandName = 30,
    GenerateQuestionAnswer = 31,
    SocialMediaAd = 32,
    GenerateLandingPageCopy = 33,
    GenerateFacebookAd = 34,
    GenerateInstagramCaption = 35,
    GeneratePodcastIdea = 36,
    GeneratePodcastTitle = 37,
    GeneratePresentation = 38,
    GeneratePressRelease = 39,
    GenerateVideoScript = 40,
    GenerateWebsiteCopy = 41,
    GenerateNewsletterIdea = 42,
    GenerateNewsletterTitle = 43,
    GenerateSalesCopy = 44,
    GenerateCourseTitle = 45,
    GenerateCourseSubtitle = 46,
    GenerateCourseDescription = 47,
    GenerateCourseLectureTitles = 48,
    GenerateCourseQuizQuestions = 49,
    GenerateCourseExercises = 50,
    GenerateCourseArticles = 51,
    SummarizeText = 52,
    AdCopy = 53,
    EmailBody = 54,
    EmailToneAdjustment = 55,
    SocialMediaPost = 56,
    SocialMediaAdGenerator = 57,
    GoogleSearchAdsGenerator = 58,
    Email = 59

use_cases = [
    {
        'title': 'Youtube Idea',
        'description': 'Generate ideas for YouTube videos.',
        'navigateTo': UseCase.YoutubeIdea.value[0],
        'category': 'youtube'
    },
    {
        'title': 'Youtube Description',
        'description': 'Create descriptions for YouTube videos.',
        'navigateTo': UseCase.YoutubeDescription.value[0],
        'category': 'youtube'
    },
    {
        'title': 'Youtube Channel Description',
        'description': 'Write descriptions for YouTube channels.',
        'navigateTo': UseCase.YoutubeChannelDescription.value[0],
        'category': 'youtube'
    },
    {
        'title': 'Testimonial and Review',
        'description': 'Generate testimonials and reviews.',
        'navigateTo': UseCase.TestimonialAndReview.value[0],
        'category': 'Testimonials and Reviews'
    },
    {
        'title': 'Tagline and Headline',
        'description': 'Generate catchy taglines and headlines.',
        'navigateTo': UseCase.TagLineAndHeadline.value[0],
        'category': 'Taglines and Headlines'
    },
    {
        'title': 'Story Plots',
        'description': 'Generate plots for stories or narratives.',
        'navigateTo': UseCase.StoryPlots.value[0],
        'category': 'Story Plots'
    },
    {
        'title': 'Song Lyrics',
        'description': 'Create lyrics for songs.',
        'navigateTo': UseCase.SongLyrics.value[0],
        'category': 'Song Lyrics'
    },
    {
        'title': 'SMS and Notifications',
        'description': 'Generate text messages and notifications.',
        'navigateTo': UseCase.SmsAndNotifications.value[0],
        'category': 'SMS and Notifications'
    },
    {
        'title': 'Email Subject Line',
        'description': 'Create subject lines for emails.',
        'navigateTo': UseCase.EmailSubjectLine.value[0],
        'category': 'Email'
    },
    {
        'title': 'Job Description',
        'description': 'Write descriptions for job postings.',
        'navigateTo': UseCase.JobDescription.value[0],
        'category': 'Job-related'
    },
    {
        'title': 'Blog Idea and Outline',
        'description': 'Generate ideas and outlines for blog posts.',
        'navigateTo': UseCase.BlogIdeaAndOutline.value[0],
        'category': 'blog'
    },
    {
        'title': 'Cover Letter',
        'description': 'Create cover letters for job applications.',
        'navigateTo': UseCase.CoverLetter.value[0],
        'category': 'Job-related'
    },
    {
        'title': 'Profile Bio',
        'description': 'Write a biography for a profile or portfolio.',
        'navigateTo': UseCase.ProfileBio.value[0],
        'category': 'profile'
    },
    {
        'title': 'Reply to Reviews and Messages',
        'description': 'Craft responses to reviews and messages.',
        'navigateTo': UseCase.ReplyToReviewsAndMessages.value[0],
        'category': 'Content Creation'
    },
    {
        'title': 'Grammar Correction',
        'description': 'Correct grammar and punctuation errors.',
        'navigateTo': UseCase.GrammarCorrection.value[0],
        'category': "Business"
    },
    {
        'title': 'Business Idea',
        'description': 'Generate ideas for new businesses.',
        'navigateTo': UseCase.BusinessIdea.value[0],
        'category': 'business'
    },
    {
        'title': 'Business Idea Pitch',
        'description': 'Create a pitch for a business idea.',
        'navigateTo': UseCase.BusinessIdeaPitch.value[0],
        'category': 'business'
    },
    {
        'title': 'Citation',
        'description': 'Generate citations for references.',
        'navigateTo': UseCase.Citation.value[0],
        'category': 'academic'
    },
    {
        'title': 'Copywriting Framework AIDA',
        'description': 'Apply the AIDA framework to copywriting.',
        'navigateTo': UseCase.CopywritingFrameworkAIDA.value[0],
        'category': 'business'
    },
        {
        'title': 'Google Search Ad',
        'description': 'Generate Google search ads.',
        'navigateTo': UseCase.GoogleSearchAd.value[0],
        'category': 'Marketing and Advertising'
    },
    {
        'title': 'Interview Questions',
        'description': 'Generate interview questions.',
        'navigateTo': UseCase.InterviewQuestions.value[0],
        'category': 'Interview'
    },
    {
        'title': 'Keywords Extractor',
        'description': 'Extract keywords from text or documents.',
        'navigateTo': UseCase.KeywordsExtractor.value[0],
        'category': 'seo'
    },
    {
        'title': 'Landing Page',
        'description': 'Create landing page content.',
        'navigateTo': UseCase.LandingPage.value[0],
        'category': 'seo'
    },
    {
        'title': 'Paraphrase Text',
        'description': 'Paraphrase or rephrase text.',
        'navigateTo': UseCase.ParaphraseText.value[0],
        'category': 'Content Editing'
    },
    {
        'title': 'Post and Caption Idea',
        'description': 'Generate ideas for social media posts and captions.',
        'navigateTo': UseCase.PostAndCaptionIdea.value[0],
        'category': 'Social Media'
    },
    {
        'title': 'Product Description with Bullet Points',
        'description': 'Write product descriptions with bullet points.',
        'navigateTo': UseCase.ProductDescriptionWithBulletPoints.value[0],
        'category': 'Product Description'
    },
    {
        'title': 'Product Description',
        'description': 'Write product descriptions.',
        'navigateTo': UseCase.ProductDescription.value[0],
        'category': 'Product Description'
    },
    {
        'title': 'SEO Meta Title',
        'description': 'Generate SEO meta titles.',
        'navigateTo': UseCase.SeoMetaTitle.value[0],
        'category': 'seo'
    },
    {
        'title': 'Generate Call to Action',
        'description': 'Create compelling calls to action.',
        'navigateTo': UseCase.GenerateCallToAction.value[0],
        'category': 'Call to Action'
    },
    {
        'title': 'Generate Brand Name',
        'description': 'Generate brand names.',
        'navigateTo': UseCase.GenerateBrandName.value[0],
        'category': 'Branding'
    },
    {
        'title': 'Generate Question Answer',
        'description': 'Generate questions and answers.',
        'navigateTo': UseCase.GenerateQuestionAnswer.value[0],
        'category': 'Questions and Answers'
    },
    {
        'title': 'Social Media Ad',
        'description': 'Generate social media ads.',
        'navigateTo': UseCase.SocialMediaAd.value[0],
        'category': 'Social Media Ad Generator'
    },
    {
        'title': 'Generate Landing Page Copy',
        'description': 'Generate landing page copy.',
        'navigateTo': UseCase.GenerateLandingPageCopy.value[0],
        'category': 'Landing Page'
    },
    {
        'title': 'Generate Facebook Ad',
        'description': 'Generate Facebook ads.',
        'navigateTo': UseCase.GenerateFacebookAd.value[0],
        'category': 'Facebook Ad'
    },
    {
        'title': 'Generate Instagram Caption',
        'description': 'Generate captions for Instagram posts.',
        'navigateTo': UseCase.GenerateInstagramCaption.value[0],
        'category': 'social media'
    },
    {
        'title': 'Generate Podcast Idea',
        'description': 'Generate ideas for podcasts.',
        'navigateTo': UseCase.GeneratePodcastIdea.value[0],
        'category': 'podcast'
    },
        {
        "title": "GeneratePresentation",
        "description": "Generate engaging and visually appealing presentations for various purposes.",
        "navigateTo": "/generate-presentation",
        "category": "Presentation"
    },
    {
        "title": "GeneratePressRelease",
        "description": "Craft professional press releases to announce important news or events.",
        "navigateTo": "/generate-press-release",
        "category": "Press Release"
    },
    {
        "title": "GenerateVideoScript",
        "description": "Create compelling scripts for videos, including commercials, tutorials, or presentations.",
        "navigateTo": "/generate-video-script",
        "category": "Video Script"
    },
    {
        "title": "GenerateWebsiteCopy",
        "description": "Generate persuasive and informative copy for website pages and sections.",
        "navigateTo": "/generate-website-copy",
        "category": "Website"
    },
    {
        "title": "GenerateNewsletterIdea",
        "description": "Get creative ideas and inspiration for your newsletters.",
        "navigateTo": "/generate-newsletter-idea",
        "category": "Newsletter"
    },
    {
        "title": "GenerateNewsletterTitle",
        "description": "Generate catchy and attention-grabbing titles for your newsletters.",
        "navigateTo": "/generate-newsletter-title",
        "category": "Newsletter"
    },
    {
        "title": "GenerateSalesCopy",
        "description": "Create persuasive and compelling sales copy for marketing campaigns.",
        "navigateTo": "/generate-sales-copy",
        "category": "Sales Copy"
    },
    {
        "title": "GenerateCourseTitle",
        "description": "Generate catchy and informative titles for your online courses.",
        "navigateTo": "/generate-course-title",
        "category": "Course"
    },
    {
        "title": "GenerateCourseSubtitle",
        "description": "Craft engaging and descriptive subtitles for your online course modules.",
        "navigateTo": "/generate-course-subtitle",
        "category": "Course"
    },
    {
        "title": "GenerateCourseDescription",
        "description": "Write compelling descriptions to effectively communicate the value of your online course.",
        "navigateTo": "/generate-course-description",
        "category": "Course"
    },
    {
        "title": "GenerateCourseLectureTitles",
        "description": "Generate clear and informative titles for the lectures in your online course.",
        "navigateTo": "/generate-course-lecture-titles",
        "category": "Course"
    },
    {
        "title": "GenerateCourseQuizQuestions",
        "description": "Create engaging quiz questions to test the knowledge of your online course participants.",
        "navigateTo": "/generate-course-quiz-questions",
        "category": "Course"
    },
    {
        "title": "GenerateCourseExercises",
        "description": "Generate practical exercises to reinforce learning in your online course.",
        "navigateTo": "/generate-course-exercises",
        "category": "Course"
    },
    {
        "title": "GenerateCourseArticles",
        "description": "Generate informative articles as supplementary material for your online course.",
        "navigateTo": "/generate-course-articles",
        "category": "Course"
    },
    {
        "title": "SummarizeText",
        "description": "Summarize long pieces of text into concise and meaningful summaries.",
        "navigateTo": "/summarize-text",
        "category": "Text Summarization"
    },
        {
        "title": "AdCopy",
        "description": "Create compelling and persuasive copy for advertisements in various mediums.",
        "navigateTo": "/ad-copy",
        "category": "Ad Copy"
    },
    {
        "title": "EmailBody",
        "description": "Craft effective and engaging bodies for email communications.",
        "navigateTo": "/email-body",
        "category": "Email Body"
    },
    {
        "title": "EmailToneAdjustment",
        "description": "Adjust the tone and style of email messages to match the desired intent or audience.",
        "navigateTo": "/email-tone-adjustment",
        "category": "Email Tone Adjustment"
    },
    {
        "title": "SocialMediaPost",
        "description": "Create engaging and attention-grabbing posts for social media platforms.",
        "navigateTo": "/social-media-post",
        "category": "Social Media Post"
    },
    {
        "title": "SocialMediaAdGenerator",
        "description": "Generate effective and compelling advertisements for social media platforms.",
        "navigateTo": "/social-media-ad-generator",
        "category": "Social Media Ad Generator"
    },
    {
        "title": "GoogleSearchAdsGenerator",
        "description": "Generate ads specifically designed for Google search engine results.",
        "navigateTo": "/google-search-ads-generator",
        "category": "Google Search Ads Generator"
    }
]