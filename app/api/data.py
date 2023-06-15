from enum import Enum
#TODO: move this to usecases
class UseCase(Enum):
    YoutubeIdea = "youtube_video_idea"
    YoutubeVideoDescription = "youtube_video_description"
    YoutubeChannelDescription = "youtube_channel_description"
    BlogIdeaAndOutline = "blog_idea_and_outline"
    TestimonialAndReview = "testimonials_testimonial_and_review"
    TagLineAndHeadline = "tagline_and_headline"
    StoryPlots = "story_plots"
    SongLyrics = "song_lyrics"
    SmsAndNotifications = "sms_and_notifications"
    EmailSubjectLine = "email_subject_line"
    JobDescription = "job_description"
    CoverLetter = "cover_letter"
    ProfileBio = "profile_bio"
    ReplyToReviewsAndMessages = "reply_to_reviews_and_messages"
    GrammarCorrection = "grammar_correction"
    BusinessIdea = "business_idea"
    BusinessIdeaPitch = "business_idea_pitch"
    Citation = "citation"
    CopywritingFrameworkAIDA = "copywriting_framework_aida"
    GoogleSearchAd = "google_search_ad"
    InterviewQuestions = "interview_questions"
    KeywordsExtractor = "keywords_extractor"
    LandingPage = "landing_page"
    ParaphraseText = "paraphrase_text"
    PostAndCaptionIdea = "post_and_caption_idea"
    ProductDescriptionWithBulletPoints = "product_description_with_bullet_points"
    ProductDescription = "product_description"
    SeoMetaTitle = "seo_meta_title"
    GenerateCallToAction = "generate_call_to_action"
    GenerateBrandName = "generate_brand_name"
    GenerateQuestionAnswer = "generate_question_answer"
    SocialMediaAd = "social_media_ad"
    GenerateLandingPageCopy = "generate_landing_page_copy"
    GenerateFacebookAd = "generate_facebook_ad"
    GenerateInstagramCaption = "generate_instagram_caption"
    GeneratePodcastIdea = "generate_podcast_idea"
    GeneratePodcastTitle = "generate_podcast_title"
    GeneratePresentation = "generate_presentation"
    GeneratePressRelease = "generate_press_release"
    GenerateVideoScript = "generate_video_script"
    GenerateWebsiteCopy = "generate_website_copy"
    GenerateNewsletterIdea = "generate_newsletter_idea"
    GenerateNewsletterTitle = "generate_newsletter_title"
    GenerateSalesCopy = "generate_sales_copy"
    GenerateCourseTitle = "generate_course_title"
    GenerateCourseSubtitle = "generate_course_subtitle"
    GenerateCourseDescription = "generate_course_description"
    GenerateCourseLectureTitles = "generate_course_lecture_titles"
    GenerateCourseQuizQuestions = "generate_course_quiz_questions"
    GenerateCourseExercises = "generate_course_exercises"
    GenerateCourseArticles = "generate_course_articles"
    SummarizeText = "summarize_text"
    AdCopy = "ad_copy"
    EmailBody = "email_body"
    EmailToneAdjustment = "email_tone_adjustment"
    SocialMediaPost = "social_media_post"
    SocialMediaAdGenerator = "social_media_ad_generator"
    GoogleSearchAdsGenerator = "google_search_ads_generator"
    Email = "email"


use_cases = [
    {
        'title': 'Youtube Idea',
        'description': 'Generate ideas for YouTube videos.',
        'navigateTo': 'youtube_video_idea',
        'category': 'youtube'
    },
    {
        'title': 'Youtube Description',
        'description': 'Create descriptions for YouTube videos.',
        'navigateTo': 'youtube_video_description',
        'category': 'youtube'
    },
    {
        'title': 'Youtube Channel Description',
        'description': 'Write descriptions for YouTube channels.',
        'navigateTo': 'youtube_channel_description',
        'category': 'youtube'
    },
    {
        'title': 'Testimonial and Review',
        'description': 'Generate testimonials and reviews.',
        'navigateTo': 'testimonials_testimonial_and_review',
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
        'category': 'Job related'
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
        'category': 'Job related'
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
        "navigateTo": "generate_presentation",
        "category": "Presentation"
    },
    {
        "title": "GeneratePressRelease",
        "description": "Craft professional press releases to announce important news or events.",
        "navigateTo": "generate_press_release",
        "category": "Press Release"
    },
    {
        "title": "GenerateVideoScript",
        "description": "Create compelling scripts for videos, including commercials, tutorials, or presentations.",
        "navigateTo": "generate_video_script",
        "category": "Video Script"
    },
    {
        "title": "GenerateWebsiteCopy",
        "description": "Generate persuasive and informative copy for website pages and sections.",
        "navigateTo": "generate_website_copy",
        "category": "Website"
    },
    {
        "title": "GenerateNewsletterIdea",
        "description": "Get creative ideas and inspiration for your newsletters.",
        "navigateTo": "generate_newsletter_idea",
        "category": "Newsletter"
    },
    {
        "title": "GenerateNewsletterTitle",
        "description": "Generate catchy and attention_grabbing titles for your newsletters.",
        "navigateTo": "generate_newsletter_title",
        "category": "Newsletter"
    },
    {
        "title": "GenerateSalesCopy",
        "description": "Create persuasive and compelling sales copy for marketing campaigns.",
        "navigateTo": "generate_sales_copy",
        "category": "Sales Copy"
    },
    {
        "title": "GenerateCourseTitle",
        "description": "Generate catchy and informative titles for your online courses.",
        "navigateTo": "generate_course_title",
        "category": "Course"
    },
    {
        "title": "GenerateCourseSubtitle",
        "description": "Craft engaging and descriptive subtitles for your online course modules.",
        "navigateTo": "generate_course_subtitle",
        "category": "Course"
    },
    {
        "title": "GenerateCourseDescription",
        "description": "Write compelling descriptions to effectively communicate the value of your online course.",
        "navigateTo": "generate_course_description",
        "category": "Course"
    },
    {
        "title": "GenerateCourseLectureTitles",
        "description": "Generate clear and informative titles for the lectures in your online course.",
        "navigateTo": "generate_course_lecture_titles",
        "category": "Course"
    },
    {
        "title": "GenerateCourseQuizQuestions",
        "description": "Create engaging quiz questions to test the knowledge of your online course participants.",
        "navigateTo": "generate_course_quiz_questions",
        "category": "Course"
    },
    {
        "title": "GenerateCourseExercises",
        "description": "Generate practical exercises to reinforce learning in your online course.",
        "navigateTo": "generate_course_exercises",
        "category": "Course"
    },
    {
        "title": "GenerateCourseArticles",
        "description": "Generate informative articles as supplementary material for your online course.",
        "navigateTo": "generate_course_articles",
        "category": "Course"
    },
    {
        "title": "SummarizeText",
        "description": "Summarize long pieces of text into concise and meaningful summaries.",
        "navigateTo": "summarize_text",
        "category": "Text Summarization"
    },
        {
        "title": "AdCopy",
        "description": "Create compelling and persuasive copy for advertisements in various mediums.",
        "navigateTo": "ad_copy",
        "category": "Ad Copy"
    },
    {
        "title": "EmailBody",
        "description": "Craft effective and engaging bodies for email communications.",
        "navigateTo": "email_body",
        "category": "Email Body"
    },
    {
        "title": "EmailToneAdjustment",
        "description": "Adjust the tone and style of email messages to match the desired intent or audience.",
        "navigateTo": "email_tone_adjustment",
        "category": "Email Tone Adjustment"
    },
    {
        "title": "SocialMediaPost",
        "description": "Create engaging and attention_grabbing posts for social media platforms.",
        "navigateTo": "social_media_post",
        "category": "Social Media Post"
    },
    {
        "title": "SocialMediaAdGenerator",
        "description": "Generate effective and compelling advertisements for social media platforms.",
        "navigateTo": "social_media_ad_generator",
        "category": "Social Media Ad Generator"
    },
    {
        "title": "GoogleSearchAdsGenerator",
        "description": "Generate ads specifically designed for Google search engine results.",
        "navigateTo": "google_search_ads_generator",
        "category": "Google Search Ads Generator"
    }
]


