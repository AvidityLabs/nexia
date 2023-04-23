# Test cases for DeveloperRegisterView

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
