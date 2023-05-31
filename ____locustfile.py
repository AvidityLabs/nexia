from locust import HttpUser, task, between

# Run locust --host=http://localhost:8000

class MyUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def my_task(self):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcyZmIxYTY1LWFkOTgtNDZhZC05OWY5LTQ4ODVmNTNlNmZmMSIsImV4cCI6MTY4NzgzNDgxMn0.7VcHZs779XZ2hni31FDpWe6-gzsMhH-D-rZ9DF5kilQ",
            'Content-Type': 'application/json',
            "X-RapidAPI-Host": "nexia2.p.rapidapi.com",
            "X-RapidAPI-Key": "33b988ce57mshcdcdc8943ca406cp12e826jsna798cb3d2ac5"
        }
        self.client.get("/api/v1/instructions/", headers=headers)
        self.client.get('/api/v1/instructions/tones/', headers=headers)
        self.client.get('/api/v1/instructions/?tones=insightful', headers=headers)
        self.client.get('/api/v1/instructions/tones/detail/1/', headers=headers)
        self.client.get('/api/v1/instructions/detail/1/', headers=headers)







    # path('v1/instructions/tones/create/', CreateToneAPIView.as_view(), name='create-tone'),
    # path('v1/instructions/tones/detail/<int:pk>/', ToneRetrieveView.as_view(), name='instruction-retrieve-update-destroy'),
    # path('v1/instructions/tones/update/<int:pk>/', ToneUpdateView.as_view(), name='instruction-retrieve-update-destroy'),
    # path('v1/instructions/create/', InstructionCreateView.as_view(), name='instruction-create'),
    # path('v1/instructions/update/<int:pk>/', InstructionUpdateView.as_view(), name='instruction-update'),

