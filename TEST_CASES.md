
# Test case 1: Test UserRetrieveUpdateAPIView (feature not requred at the moment)

- [x]  Test if the user can retrieve their own information successfully using a GET request
- []  Test if the user can update their own information successfully using a PATCH request with valid data
- []  Test if the user can update their own information successfully using a PATCH request with invalid data

# Test case 2: Test LoginAPIView

- [x]  Test if a user can log in successfully using a POST request with valid credentials
- [x]  Test if a user cannot log in using a POST request with an invalid email
- [x]  Test if a user cannot log in using a POST request with an invalid password
- [x]  Test if a user subscription, pricing plan and token usage have been updated.

Test case 3: Test DeveloperRegisterView

- [x]  Test if a user can register successfully using a POST request with valid data
- [x]  Test if a user can register successfully and objects Subscription, TokenUsage created for the user.(plan=NOTSET)
- [x]  Test if a user cannot register using a POST request with an invalid email
- [x] Test if a user cannot register using a POST request with an invalid username
- [x]  Test if a user cannot register using a POST request with an invalid password

Test case 4: Test TextEmotionAnalysisView

1.  Test if a user can analyze text successfully using a POST request with valid data
2.  Test if a user cannot analyze text using a POST request with invalid data
3.  Test if a user cannot analyze text using a POST request with no authentication token.

- [x] Test for successful registration:

    - Input: {'email': '<test@test.com>', 'password': 'test1234'}

    - Expected Output: {'api_key': <generated API key>}

    - Status Code: 201

- [x] Test for missing email field:

    - Input: {'password': 'test1234'}

    - Expected Output: {'email': ['This field is required.']}

    - Status Code: 400

- [x] Test for invalid email format:

    - Input: {'email': 'test', 'password': 'test1234'}

    - Expected Output: {'email': ['Enter a valid email address.']}

    - Status Code: 400

- [x] Test for missing password field:

    - Input: {'email': '<test@test.com>'}

    - Expected Output: {'password': ['This field is required.']}

    - Status Code: 400

- [x] Test for short password:

    - Input: {'email': '<test@test.com>', 'password': 'test'}

    - Expected Output: {'password': ['Ensure this field has at least 8 characters.']}

    - Status Code: 400

- [x] Test for duplicate email:

    - Input: {'email': '<test@test.com>', 'password': 'test1234'}

    - Expected Output: {'error': 'UNIQUE constraint failed: auth_user.email'}

    - Status Code: 400

- [x] Test with invalid input data (missing 'text' field)

- [x] Test with empty 'text' field

- [x] Test with text containing only spaces

- [x] Test with text containing only special characters

- [x] Test with text containing only digits

- [x] Test with text containing non-ASCII characters

- [x] Test with text longer than the maximum allowed length

- [x] Test with text shorter than the minimum allowed length

14. Test with a connection error when querying the sentiment model

15. Test with a response data that is None

16. Test with an error in the sentiment model query

17. Test with a user who has not subscribed to any pricing plan

18. Test with a user who has subscribed to a pricing plan

19. Test with a user who has exceeded their prompt tokens usage limit

20. Test with a user who has exceeded their completion tokens usage limit

21. Test with a user who has exceeded their total tokens usage limit


incase the yget errors

{'detail': 'Authentication credentials were not provided.'}