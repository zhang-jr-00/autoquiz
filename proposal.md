# Team Name: AutoQuiz? 
## Team Members: Aigerim Kurmanbekova, Connor Bernard, Jingru Zhang, Mawil Hasan, Michael Herrington 

## Summary  
Our project aims to build an LLM powered Quiz and Learning Module Generator using the OpenAI API. The application will be able to automatically generate structured learning quizzes, and potentially learning modules from educational content. Users can upload either Youtube video links or a **PDF document** (e.g., lecture notes, research papers, textbooks). Our API will extract the content using OCR and transcription tools, process it through **OpenAI’s API**, and generate relevant output.  

The system can additionally be designed to reinforce key concepts dynamically - for example, if a user answers a question incorrectly, the API can generate follow-up questions to improve retention. Additionally, chatbots can be used to explain the reasoning behind incorrect answers.

## Motivation  
With the rise of AI-driven education**, personalized learning has become a key focus. In addition, multi-modal learning materials have emerged as common resources for learning. While this has been useful for engaging students, the breadth of information makes it difficult to easily create content-specific learning tools. 

Additionally as LLMs have taken the software world by store, the addition of mastery learning, first presented by Benjamin Bloom of UChicago in late 60's, has become achievable. His work highlighted that a mastery learning of topics resulted in a two-standard-deviation (σ) improvement in student achievement compared to traditional classroom instruction. 

- **For academic users** (e.g., undergrad/grad students), PDFs provide structured, well-formatted input, making it easier to create tailored quizzes.  
- **For broader accessibility**, integrating with YouTube enables **post-video learning assessments**, supporting students in online education platforms like Khan Academy, Coursera, and YouTube EDU.  
- **Instead of static quizzes, we could implement mastery-based modules** — similar to Duolingo—where topics are segmented, and learning progresses when students demonstrate mastery.  

## Planned External APIs  
1. **OpenAI API** – Summarizes content, generates quiz questions, and potentially adaptive learning modules and chatbots.  
   - API Documentation: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)  
2. **Google Cloud Vision API (OCR for PDFs)** – Extracts text from PDFs for AI processing.  
   - API Documentation: [https://cloud.google.com/vision/docs/ocr](https://cloud.google.com/vision/docs/ocr)  
3. **YouTube Data API (if expanded to video support)** – Fetches **video transcripts** for OpenAI processing.  
   - API Documentation: [https://developers.google.com/youtube/registering_an_application](https://developers.google.com/youtube/registering_an_application)  

## Database & Data Persistence  
We will use **MongoDB** to store:  
- **User Profiles** (past interactions, learning progress)  
- **Generated Modules & Quizzes** (for users to revisit)  
- **Topic Categorization & Reinforcement Data** (to adapt difficulty over time)  

## Dockerization  
- The API, OCR service, and database will run in eparate Docker containers for scalability.  
- **Docker Compose** will be used to orchestrate service dependencies.  

## Project Feasibility & Features  
### Core Features  
- Accepts PDF uploads and extracts text via OCR  
- Calls OpenAI API to generate quizzes or structured learning modules 
- Stores user progress and history in MongoDB  
- Uses an adaptive learning approach (incorrect answers trigger reinforcement)  

### Stretch Goals  
- Integrate YouTube transcripts for processing video-based learning content  
- Implement a difficulty adjustment system based on user accuracy  

## Next Steps  
1. Define **API endpoints** and create a **system architecture diagram**.  
2. Develop **OCR-based text extraction for PDFs**.  
3. Integrate **OpenAI API for quiz/module generation**.  
4. Implement **MongoDB** for storing learning progress.  
5. Containerize services using **Docker**.  
6. Expand to **YouTube transcript processing**.  
