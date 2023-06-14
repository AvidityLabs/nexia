from enum import Enum

class UseCase(Enum):
    YoutubeIdea = "/youtube/video_idea"
    YoutubeVideoDescription = "/youtube/video_description"
    YoutubeChannelDescription = "/youtube/channel_description"
    BlogIdeaAndOutline = "/blog/idea_and_outline"
    TestimonialAndReview = "/testimonials/testimonial_and_review"
    TagLineAndHeadline = "/tagline_and_headline"
    StoryPlots = "/story/plots"
    SongLyrics = "/song/lyrics"
    SmsAndNotifications = "/sms_and_notifications"
    EmailSubjectLine = "/email/subject_line"
    JobDescription = "/job/description"
    CoverLetter = "/cover_letter"
    ProfileBio = "/profile/bio"
    ReplyToReviewsAndMessages = "/reply_to_reviews_and_messages"
    GrammarCorrection = "/grammar_correction"
    BusinessIdea = "/business/idea"
    BusinessIdeaPitch = "/business/idea_pitch"
    Citation = "/citation"
    CopywritingFrameworkAIDA = "/copywriting/framework_aida"
    GoogleSearchAd = "/google/search_ad"
    InterviewQuestions = "/interview/questions"
    KeywordsExtractor = "/keywords/extractor"
    LandingPage = "/landing_page"
    ParaphraseText = "/paraphrase/text"
    PostAndCaptionIdea = "/post_and_caption/idea"
    ProductDescriptionWithBulletPoints = "/product_description_with_bullet_points"
    ProductDescription = "/product_description"
    SeoMetaTitle = "/seo/meta_title"
    GenerateCallToAction = "/generate/call_to_action"
    GenerateBrandName = "/generate/brand_name"
    GenerateQuestionAnswer = "/generate/question_answer"
    SocialMediaAd = "/social_media/ad"
    GenerateLandingPageCopy = "/generate/landing_page_copy"
    GenerateFacebookAd = "/generate/facebook_ad"
    GenerateInstagramCaption = "/generate/instagram_caption"
    GeneratePodcastIdea = "/generate/podcast_idea"
    GeneratePodcastTitle = "/generate/podcast_title"
    GeneratePresentation = "/generate/presentation"
    GeneratePressRelease = "/generate/press_release"
    GenerateVideoScript = "/generate/video_script"
    GenerateWebsiteCopy = "/generate/website_copy"
    GenerateNewsletterIdea = "/generate/newsletter_idea"
    GenerateNewsletterTitle = "/generate/newsletter_title"
    GenerateSalesCopy = "/generate/sales_copy"
    GenerateCourseTitle = "/generate/course_title"
    GenerateCourseSubtitle = "/generate/course_subtitle"
    GenerateCourseDescription = "/generate/course_description"
    GenerateCourseLectureTitles = "/generate/course_lecture_titles"
    GenerateCourseQuizQuestions = "/generate/course_quiz_questions"
    GenerateCourseExercises = "/generate/course_exercises"
    GenerateCourseArticles = "/generate/course_articles"
    SummarizeText = "/summarize/text"
    AdCopy = "/ad/copy"
    EmailBody = "/email/body"
    EmailToneAdjustment = "/email/tone_adjustment"
    SocialMediaPost = "/social_media/post"
    SocialMediaAdGenerator = "/social_media/ad_generator"
    GoogleSearchAdsGenerator = "/google/search_ads_generator"
    Email = "/email"


use_cases = [
    {
        'title': 'Youtube Idea',
        'description': 'Generate ideas for YouTube videos.',
        'navigateTo': '/youtube/video_idea',
        'category': 'youtube'
    },
    {
        'title': 'Youtube Description',
        'description': 'Create descriptions for YouTube videos.',
        'navigateTo': '/youtube/video_description',
        'category': 'youtube'
    },
    {
        'title': 'Youtube Channel Description',
        'description': 'Write descriptions for YouTube channels.',
        'navigateTo': 'youtube/channel_description',
        'category': 'youtube'
    },
    {
        'title': 'Testimonial and Review',
        'description': 'Generate testimonials and reviews.',
        'navigateTo': '/testimonials/testimonial_and_review"',
        'category': 'Testimonials and Reviews'
    },    {
        'title': 'Tagline and Headline',
        'description': 'Generate catchy taglines and headlines.',
        'navigateTo': UseCase.TagLineAndHeadline.value,
        'category': 'Taglines and Headlines'
    },
    {
        'title': 'Story Plots',
        'description': 'Generate plots for stories or narratives.',
        'navigateTo': UseCase.StoryPlots.value,
        'category': 'Story Plots'
    },
    {
        'title': 'Song Lyrics',
        'description': 'Create lyrics for songs.',
        'navigateTo': UseCase.SongLyrics.value,
        'category': 'Song Lyrics'
    },
    {
        'title': 'SMS and Notifications',
        'description': 'Generate text messages and notifications.',
        'navigateTo': UseCase.SmsAndNotifications.value,
        'category': 'SMS and Notifications'
    },
    {
        'title': 'Email Subject Line',
        'description': 'Create subject lines for emails.',
        'navigateTo': UseCase.EmailSubjectLine.value,
        'category': 'Email'
    },
    {
        'title': 'Job Description',
        'description': 'Write descriptions for job postings.',
        'navigateTo': UseCase.JobDescription.value,
        'category': 'Job-related'
    },
    {
        'title': 'Blog Idea and Outline',
        'description': 'Generate ideas and outlines for blog posts.',
        'navigateTo': UseCase.BlogIdeaAndOutline.value,
        'category': 'blog'
    },
    {
        'title': 'Cover Letter',
        'description': 'Create cover letters for job applications.',
        'navigateTo': UseCase.CoverLetter.value,
        'category': 'Job-related'
    },
    {
        'title': 'Profile Bio',
        'description': 'Write a biography for a profile or portfolio.',
        'navigateTo': UseCase.ProfileBio.value,
        'category': 'profile'
    },
    {
        'title': 'Reply to Reviews and Messages',
        'description': 'Craft responses to reviews and messages.',
        'navigateTo': UseCase.ReplyToReviewsAndMessages.value,
        'category': 'Content Creation'
    },
    {
        'title': 'Grammar Correction',
        'description': 'Correct grammar and punctuation errors.',
        'navigateTo': UseCase.GrammarCorrection.value,
        'category': "Business"
    },
    {
        'title': 'Business Idea',
        'description': 'Generate ideas for new businesses.',
        'navigateTo': UseCase.BusinessIdea.value,
        'category': 'business'
    },
    {
        'title': 'Business Idea Pitch',
        'description': 'Create a pitch for a business idea.',
        'navigateTo': UseCase.BusinessIdeaPitch.value,
        'category': 'business'
    },
    {
        'title': 'Citation',
        'description': 'Generate citations for references.',
        'navigateTo': UseCase.Citation.value,
        'category': 'academic'
    },
    {
        'title': 'Copywriting Framework AIDA',
        'description': 'Apply the AIDA framework to copywriting.',
        'navigateTo': UseCase.CopywritingFrameworkAIDA.value,
        'category': 'business'
    },
        {
        'title': 'Google Search Ad',
        'description': 'Generate Google search ads.',
        'navigateTo': UseCase.GoogleSearchAd.value,
        'category': 'Marketing and Advertising'
    },
    {
        'title': 'Interview Questions',
        'description': 'Generate interview questions.',
        'navigateTo': UseCase.InterviewQuestions.value,
        'category': 'Interview'
    },
    {
        'title': 'Keywords Extractor',
        'description': 'Extract keywords from text or documents.',
        'navigateTo': UseCase.KeywordsExtractor.value,
        'category': 'seo'
    },
    {
        'title': 'Landing Page',
        'description': 'Create landing page content.',
        'navigateTo': UseCase.LandingPage.value,
        'category': 'seo'
    },
    {
        'title': 'Paraphrase Text',
        'description': 'Paraphrase or rephrase text.',
        'navigateTo': UseCase.ParaphraseText.value,
        'category': 'Content Editing'
    },
    {
        'title': 'Post and Caption Idea',
        'description': 'Generate ideas for social media posts and captions.',
        'navigateTo': UseCase.PostAndCaptionIdea.value,
        'category': 'Social Media'
    },
    {
        'title': 'Product Description with Bullet Points',
        'description': 'Write product descriptions with bullet points.',
        'navigateTo': UseCase.ProductDescriptionWithBulletPoints.value,
        'category': 'Product Description'
    },
    {
        'title': 'Product Description',
        'description': 'Write product descriptions.',
        'navigateTo': UseCase.ProductDescription.value,
        'category': 'Product Description'
    },
    {
        'title': 'SEO Meta Title',
        'description': 'Generate SEO meta titles.',
        'navigateTo': UseCase.SeoMetaTitle.value,
        'category': 'seo'
    },
    {
        'title': 'Generate Call to Action',
        'description': 'Create compelling calls to action.',
        'navigateTo': UseCase.GenerateCallToAction.value,
        'category': 'Call to Action'
    },
    {
        'title': 'Generate Brand Name',
        'description': 'Generate brand names.',
        'navigateTo': UseCase.GenerateBrandName.value,
        'category': 'Branding'
    },
    {
        'title': 'Generate Question Answer',
        'description': 'Generate questions and answers.',
        'navigateTo': UseCase.GenerateQuestionAnswer.value,
        'category': 'Questions and Answers'
    },
    {
        'title': 'Social Media Ad',
        'description': 'Generate social media ads.',
        'navigateTo': UseCase.SocialMediaAd.value,
        'category': 'Social Media Ad Generator'
    },
    {
        'title': 'Generate Landing Page Copy',
        'description': 'Generate landing page copy.',
        'navigateTo': UseCase.GenerateLandingPageCopy.value,
        'category': 'Landing Page'
    },
    {
        'title': 'Generate Facebook Ad',
        'description': 'Generate Facebook ads.',
        'navigateTo': UseCase.GenerateFacebookAd.value,
        'category': 'Facebook Ad'
    },
    {
        'title': 'Generate Instagram Caption',
        'description': 'Generate captions for Instagram posts.',
        'navigateTo': UseCase.GenerateInstagramCaption.value,
        'category': 'social media'
    },
    {
        'title': 'Generate Podcast Idea',
        'description': 'Generate ideas for podcasts.',
        'navigateTo': UseCase.GeneratePodcastIdea.value,
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


