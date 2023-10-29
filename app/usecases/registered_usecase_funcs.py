
from usecases.prompts.academic import *
from usecases.prompts.blog import *
from usecases.prompts.brand import *
from usecases.prompts.business import *
from usecases.prompts.copywriting import *
from usecases.prompts.email import *
from usecases.prompts.feedback import *
from usecases.prompts.job import *
from usecases.prompts.marketing import *
from usecases.prompts.newsletter import *
from usecases.prompts.other import *
from usecases.prompts.pressrelease import *
from usecases.prompts.product import *
from usecases.prompts.sales import * 
from usecases.prompts.seo import * 
from usecases.prompts.socialmedia import * 
from usecases.prompts.video import * 
from usecases.prompts.website import * 
from usecases.prompts.youtube import *
from usecases.prompts.podcast import *

usecase_func_dict = {
        "generate_youtube_video_script": generateYouTubeVideoScript,
        "youtube_video_description": generateYoutubeVideoDescription,
        "youtube_channel_description": generateYoutubeChannelDescription,
        "blog_idea_and_outline": generateBlogIdeaAndOutline,
        "testimonials_testimonial_and_review": generateTestimonialAndReview,
        "tagline_and_headline": generateTagLineAndHeadline,
        "story_plots": generateStoryPlots,
        "song_lyrics": generateSongLyrics,
        "sms_and_notifications": generateSmsAndNotifications,
        "email_subject_line": generateEmailSubjectLine,
        "job_description": generateJobDescription,
        "cover_letter": generateCoverLetter,
        "profile_bio": generateProfileBio,
        "reply_to_reviews_and_messages": generateReplyToReviewsAndMessages,
        "grammar_correction": generateGrammarCorrection,
        "business_idea": generateBusinessIdea,
        "business_idea_pitch": generateBusinessIdeaPitch,
        "citation": generateCitation,
        "copywriting_framework_aida": generateCopywritingFrameworkAIDA,
        "google_search_ad": generateGoogleSearchAd,
        "interview_questions": generateInterviewQuestions,
        "keywords_extractor": generateKeywordsExtractor,
        "paraphrase_text": generateParaphraseText,
        "post_and_caption_idea": generatePostAndCaptionIdea,
        "product_description_with_bullet_points": generateProductDescriptionWithBulletPoints,
        "product_description": generateProductDescription,
        "seo_meta_title": generateSeoMetaTitle,
        "generate_call_to_action": generateCallToAction,
        "generate_brand_name": generateBrandName,
        "generate_question_answer": generateQuestionAnswer,
        "social_media_ad": generateSocialMediaAd,
        "generate_facebook_ad": generateFacebookAd,
        "generate_instagram_caption": generateInstagramCaption,
        "generate_podcast_idea": generatePodcastIdea,
        "generate_podcast_title": generatePodcastTitle,
        "generate_presentation": generatePresentation,
        "generate_press_release": generatePressRelease,
        "generate_video_script": generateVideoScript,
        "generate_website_copy": generateWebsiteCopy,
        "generate_newsletter_idea": generateNewsletterIdea,
        "generate_newsletter_title": generateNewsletterTitle,
        "generate_sales_copy": generateSalesCopy,
        "generate_course_title": generateCourseTitle,
        "generate_course_subtitle": generateCourseSubtitle,
        "generate_course_description": generateCourseDescription,
        "generate_course_lecture_titles": generateCourseLectureTitles,
        "generate_course_quiz_questions": generateCourseQuizQuestions,
        "generate_course_exercises": generateCourseExercises,
        "generate_course_articles": generateCourseArticles,
        "summarize_text": generateSummarizeText,
        "ad_copy": generateAdCopy,
        "email_body": generateEmailBody,
        "email_tone_adjustment": generateEmailToneAdjustment,
        "social_media_post": generateSocialMediaPost,
        "social_media_ad_generator": generateSocialMediaAd,
        "google_search_ads_generator": generateGoogleSearchAd,
        "email": generateEmail
}


""""Create a prompt package 

Create a package named usecase_functions in your Django app directory.

Inside the usecase_functions package, create separate modules or subpackages for each use case category. For example, you can have modules like academic.py, blog.py, brand.py, and subpackages like socialmedia, marketing, etc., based on the categories you have.

Move the respective use case functions into their corresponding modules or subpackages. For example, the functions related to academic use cases can be moved to academic.py, and functions related to social media use cases can be moved to socialmedia subpackage.

Update the import statements in usecase_functions.py to import the functions from the appropriate modules or subpackages.

Update the UseCase model to import the usecase_func_dict from the updated usecase_functions module.
"""