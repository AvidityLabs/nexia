from .instructions import *
from .usecase import UseCase


def promptExecute(usecase: int, payload: any):
    use_case_functions = {
        UseCase.YoutubeIdea.value[0]: generateYouTubeIdea,
        UseCase.generateBlogIdeaAndOutline.value[0]: generateBlogIdeaAndOutline,
        UseCase.YoutubeVideoDescription.value[0]: generateYoutubeVideoDescription,
        UseCase.YoutubeChannelDescription.value[0]: generateYoutubeChannelDescription,
        UseCase.TestimonialAndReview.value[0]: generateTestimonialAndReview,
        UseCase.TagLineAndHeadline.value[0]: generateTagLineAndHeadline,
        UseCase.StoryPlots.value[0]: generateStoryPlots,
        UseCase.SongLyrics.value[0]: generateSongLyrics,
        UseCase.SmsAndNotifications.value[0]: generateSmsAndNotifications,
        UseCase.EmailSubjectLine.value[0]: generateEmailSubjectLine,
        UseCase.JobDescription.value[0]: generateJobDescription,
        UseCase.CoverLetter.value[0]: generateCoverLetter,
        UseCase.ProfileBio.value[0]: generateProfileBio,
        UseCase.ReplyToReviewsAndMessages.value[0]: generateReplyToReviewsAndMessages,
        UseCase.GrammarCorrection.value[0]: generateGrammarCorrection,
        UseCase.BusinessIdea.value[0]: generateBusinessIdea,
        UseCase.BusinessIdeaPitch.value[0]: generateBusinessIdeaPitch,
        UseCase.CopywritingFrameworkAIDA.value[0]: generateCopywritingFrameworkAIDA,
        UseCase.GoogleSearchAd.value[0]: generateGoogleSearchAd,
        UseCase.InterviewQuestions.value[0]: generateInterviewQuestions,
        UseCase.KeywordsExtractor.value[0]: generateKeywordsExtractor,
        UseCase.LandingPage.value[0]: generateLandingPageCopy,
        UseCase.ParaphraseText.value[0]: generateParaphraseText,
        UseCase.PostAndCaptionIdea.value[0]: generatePostAndCaptionIdea,
        UseCase.ProductDescriptionWithBulletPoints.value[0]: generateProductDescriptionWithBulletPoints,
        UseCase.ProductDescription.value[0]: generateProductDescription,
        UseCase.SeoMetaTitle.value[0]: generateSeoMetaTitle,
        UseCase.GenerateCallToAction.value[0]: generateCallToAction,
        UseCase.GenerateBrandName.value[0]: generateBrandName,
        UseCase.GenerateQuestionAnswer.value[0]: generateQuestionAnswer,
        UseCase.SocialMediaAd.value[0]: generateSocialMediaAd,
        UseCase.GenerateCourseTitle.value[0]: generateCourseTitle,
        UseCase.GenerateCourseSubtitle.value[0]: generateCourseSubtitle,
        UseCase.GenerateCourseDescription.value[0]: generateCourseDescription,
        UseCase.GenerateCourseLectureTitles.value[0]: generateCourseLectureTitles,
        UseCase.GenerateCourseQuizQuestions.value[0]: generateCourseQuizQuestions,
        UseCase.GenerateCourseExercises.value[0]: generateCourseExercises,
        UseCase.GenerateCourseArticles.value[0]: generateCourseArticles,
        UseCase.SummarizeText.value[0]: generateSummarizeText,
        UseCase.AdCopy.value[0]: generateAdCopy,
        UseCase.EmailBody.value[0]: generateEmailBody,
        UseCase.EmailToneAdjustment.value[0]: generateEmailToneAdjustment,
        UseCase.GenerateVideoScript.value[0]: generateVideoScript,
        UseCase.SocialMediaPost.value[0]: generateSocialMediaPost,
        UseCase.Email.value[0]: generateEmail,
        UseCase.GenerateLandingPageCopy.value[0]: generateLandingPageCopy,
        UseCase.GenerateFacebookAd.value[0]: generateFacebookAd,
        UseCase.GenerateInstagramCaption.value[0]: generateInstagramCaption,
        UseCase.GeneratePodcastIdea.value[0]: generatePodcastIdea,
        UseCase.GeneratePodcastTitle.value[0]: generatedcastTitle,
        UseCase.GeneratePresentation.value[0]: generatePresentation,
        UseCase.GeneratePressRelease.value[0]: generatePressRelease,
        UseCase.GenerateWebsiteCopy.value[0]: generateWebsiteCopy,
        UseCase.GenerateNewsletterIdea.value[0]: generateNewsletterIdea,
        UseCase.GenerateNewsletterTitle.value[0]: generateNewsletterTitle,
        UseCase.GenerateSalesCopy.value[0]: generateGenerateSalesCopy,
    }
    
    if usecase is None:
        return None
    
    function = use_case_functions.get(usecase)
    if function:
        return function(payload)
    
    return None

