
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
        "/youtube/video_idea": generateYouTubeVideoIdea,
        "/youtube/video_description": generateYoutubeVideoDescription,
        "/youtube/channel_description": generateYoutubeChannelDescription,
        "/blog/idea_and_outline": generateBlogIdeaAndOutline,
        "/testimonials/testimonial_and_review": generateTestimonialAndReview,
        "/tagline_and_headline": generateTagLineAndHeadline,
        "/story/plots": generateStoryPlots,
        "/song/lyrics": generateSongLyrics,
        "/sms_and_notifications": generateSmsAndNotifications,
        "/email/subject_line": generateEmailSubjectLine,
        "/job/description": generateJobDescription,
        "/cover_letter": generateCoverLetter,
        "/profile/bio": generateProfileBio,
        "/reply_to_reviews_and_messages": generateReplyToReviewsAndMessages,
        "/grammar_correction": generateGrammarCorrection,
        "/business/idea": generateBusinessIdea,
        "/business/idea_pitch": generateBusinessIdeaPitch,
        "/citation": generateCitation,
        "/copywriting/framework_aida": generateCopywritingFrameworkAIDA,
        "/google/search_ad": generateGoogleSearchAd,
        "/interview/questions": generateInterviewQuestions,
        "/keywords/extractor": generateKeywordsExtractor,
        "/paraphrase/text": generateParaphraseText,
        "/post_and_caption/idea": generatePostAndCaptionIdea,
        "/product_description_with_bullet_points": generateProductDescriptionWithBulletPoints,
        "/product_description": generateProductDescription,
        "/seo/meta_title": generateSeoMetaTitle,
        "/generate/call_to_action": generateCallToAction,
        "/generate/brand_name": generateBrandName,
        "/generate/question_answer": generateQuestionAnswer,
        "/social_media/ad": generateSocialMediaAd,
        "/generate/facebook_ad": generateFacebookAd,
        "/generate/instagram_caption": generateInstagramCaption,
        "/generate/podcast_idea": generatePodcastIdea,
        "/generate/podcast_title": generatePodcastTitle,
        "/generate/presentation": generatePresentation,
        "/generate/press_release": generatePressRelease,
        "/generate/video_script": generateVideoScript,
        "/generate/website_copy": generateWebsiteCopy,
        "/generate/newsletter_idea": generateNewsletterIdea,
        "/generate/newsletter_title": generateNewsletterTitle,
        "/generate/sales_copy": generateSalesCopy,
        "/generate/course_title": generateCourseTitle,
        "/generate/course_subtitle": generateCourseSubtitle,
        "/generate/course_description": generateCourseDescription,
        "/generate/course_lecture_titles": generateCourseLectureTitles,
        "/generate/course_quiz_questions": generateCourseQuizQuestions,
        "/generate/course_exercises": generateCourseExercises,
        "/generate/course_articles": generateCourseArticles,
        "/summarize/text": generateSummarizeText,
        "/ad/copy": generateAdCopy,
        "/email/body": generateEmailBody,
        "/email/tone_adjustment": generateEmailToneAdjustment,
        "/social_media/post": generateSocialMediaPost,
        "/social_media/ad_generator": generateSocialMediaAd,
        "/google/search_ads_generator": generateGoogleSearchAd,
        "/email": generateEmail
}


""""Create a prompt package 

Create a package named usecase_functions in your Django app directory.

Inside the usecase_functions package, create separate modules or subpackages for each use case category. For example, you can have modules like academic.py, blog.py, brand.py, and subpackages like socialmedia, marketing, etc., based on the categories you have.

Move the respective use case functions into their corresponding modules or subpackages. For example, the functions related to academic use cases can be moved to academic.py, and functions related to social media use cases can be moved to socialmedia subpackage.

Update the import statements in usecase_functions.py to import the functions from the appropriate modules or subpackages.

Update the UseCase model to import the usecase_func_dict from the updated usecase_functions module.
"""