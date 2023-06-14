# Smartcut
## Meet the Team
| Member | Student ID | Learning Path | Role | Contacts |
| :--------------------: | :--------: | :----------------: | :-----------------------------: | :---------------------------------------------: |
| Rizki Aji Mahardika  | M125DKX4707 | Machine Learning | Machine Learning Engineer | [LinkedIn - Rizki] |
| Feri Firmansah | M282DSX1495 | Machine Learning | Machine Learning Engineer | [LinkedIn - Feri] |
| Nicholas Sky Salvatio | M181DSX0251 | Machine Learning | Machine Learning Engineer | [LinkedIn - Nicholas] |
| Rafli Dwi Putra | C225DSX0611 | Cloud Computing | Cloud Engineer | [LinkedIn - Rafli] |
| Felix Savero | C225DSX0936 | Cloud Computing | Cloud Engineer| [LinkedIn - Felix] |
| Farrell Liko Tanlimhuijaya | A225DSX1678 | Mobile Development | Mobile Engineer | [LinkedIn - Farrell] |

## About Smartcut

This is our capstone project in Bangkit 2023. It is an application that can give suitable hairstyle recommendations based on the user's face shape. We leverage Machine Learning algorithms using VGG-16 model to analyze the user's face shape and give personalized recommendations.

## Main Features

- Analyze the user's face shape
- Give recommendations based on the analyzed face shape

---

How to replicate

Assuming you already have Google Cloud Platform Project with linked billing account.
- Create a Cloud Storage with face shapes folders(Triangle, Oblong, Round, Square, Heart, Diamond, Oval). Each folder should contain the pictures of hairstyle models.
- Create a service account with the role "Cloud Storage Admin", then download the key json file
- Clone this repository
- Add .env
- The .env file MUST contain : 
    - ```MODEL_PATH = path to ml model```
    - ```TEMP_IMAGE_DIR = path to temporarily save user photo```
    - ```CLOUD_STORAGE_KEY = path to service account key json```
    - ```BUCKET_NAME = cloud storage bucket name```
    - ```FACE_SHAPES_PATH = path to face shapes models folders in Cloud Storage```
- Create a virtual environment ```conda create tf```
- Activate the virtual environment ```conda activate tf```
- Install the required dependencies```pip install -r requirements.txt```
- Containerize it using Docker and tag it ```gcr.io/**YOUR_PROJECT_ID**/smartcut-ml:v1```
- Push the container image to Google Container Registry (gcr)
- Create a Cloud Run service
    - For the container image url, choose ```gcr.io/**YOUR_PROJECT_ID**/smartcut-ml:v1```
    - For the region, we choose us-central1(Iowa) to get the lowest price-to-performance
    - The minimum number of instance is 0
    - The maximum number of instance is 3
    - The memory is 8MiB
    - The number of CPU is 2
    - **Deploy the application**

[linkedin - Rizki]: https://www.linkedin.com/in/rizkiajimahardika/
[linkedin - Feri]: https://www.linkedin.com/in/ferifirmansah/
[linkedin - Nicholas]: https://www.linkedin.com/in/nicholas-sky-salvatio-1957091b6/
[linkedin - Rafli]: https://www.linkedin.com/in/rafli-d-70b183137/
[linkedin - Felix]: https://www.linkedin.com/in/felixsavero/
[linkedin - Farrell]: https://www.linkedin.com/in/farrelllikotanlimhuijaya/
