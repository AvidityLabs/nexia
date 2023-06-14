from .usecase import UseCase


def promptExecute(usecase: int, payload: any):
    registered_use_cases = {
        "/youtube/idea": generateYouTubeIdea,
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
        "/landing_page": generateLandingPage,
        "/paraphrase/text": generateParaphraseText,
        "/post_and_caption/idea": generatePostAndCaptionIdea,
        "/product_description_with_bullet_points": generateProductDescriptionWithBulletPoints,
        "/product_description": generateProductDescription,
        "/seo/meta_title": generateSeoMetaTitle,
        "/generate/call_to_action": generateCallToAction,
        "/generate/brand_name": generateBrandName,
        "/generate/question_answer": generateQuestionAnswer,
        "/social_media/ad": generateSocialMediaAd,
        "/generate/landing_page_copy": generateGenerateLandingPageCopy,
        "/generate/facebook_ad": generateGenerateFacebookAd,
        "/generate/instagram_caption": generateGenerateInstagramCaption,
        "/generate/podcast_idea": generateGeneratePodcastIdea,
        "/generate/podcast_title": generateGeneratedPodcastTitle,
        "/generate/presentation": generateGeneratePresentation,
        "/generate/press_release": generateGeneratePressRelease,
        "/generate/video_script": generateGenerateVideoScript,
        "/generate/website_copy": generateGenerateWebsiteCopy,
        "/generate/newsletter_idea": generateGenerateNewsletterIdea,
        "/generate/newsletter_title": generateGenerateNewsletterTitle,
        "/generate/sales_copy": generateGenerateSalesCopy,
        "/generate/course_title": generateGenerateCourseTitle,
        "/generate/course_subtitle": generateGenerateCourseSubtitle,
        "/generate/course_description": generateGenerateCourseDescription,
        "/generate/course_lecture_titles": generateGenerateCourseLectureTitles,
        "/generate/course_quiz_questions": generateGenerateCourseQuizQuestions,
        "/generate/course_exercises": generateGenerateCourseExercises,
        "/generate/course_articles": generateGenerateCourseArticles,
        "/summarize/text": generateSummarizeText,
        "/ad/copy": generateAdCopy,
        "/email/body": generateEmailBody,
        "/email/tone_adjustment": generateEmailToneAdjustment,
        "/social_media/post": generateSocialMediaPost,
        "/social_media/ad_generator": generateSocialMediaAdGenerator,
        "/google/search_ads_generator": generateGoogleSearchAdsGenerator,
        "/email": generateEmail
    }

    # Register the functions in the dictionary
    for url, function in registered_use_cases.items():
        use_case_functions[url] = function

    if usecase is None:
        return None

    if function:
        try:
            return function(payload)
        except KeyError:
            # Handle the case where the enumerated value doesn't exist
            raise ValueError(f"Invalid use case value: {usecase}")
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred while executing the use case: {e}")
            return None

    # Handle the case where the function is not found for the given use case
    raise ValueError(f"No function found for use case: {usecase}")








