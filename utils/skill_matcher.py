import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
#load model
model=SentenceTransformer('all-MiniLM-L6-v2')

#load json skills

with open("utils/role_skills.json")as f:
    ROLE_SKILLS=json.load(f)


def analyse_skills(resume_text,selected_role,threshold=0.25):
    #resume_embedding=model.encode([resume_text])
    skills=ROLE_SKILLS.get(selected_role,[])
    #split resume into chunks
    sentences=re.split(r'[.\n]',resume_text)
    print("Analysing role:",selected_role)

    matched=[]
    missing=[]

    for skill in skills:
        #print("checking skill:",skill)
        skill_embedding=model.encode([skill])
        max_similarity=0
        for sentence in sentences:
            if (sentence.strip()==""):
                continue
            sentence_embedding=model.encode([sentence])
            similarity=cosine_similarity(sentence_embedding,skill_embedding)[0][0]
        #print(skill,similarity)

            if similarity>max_similarity:
                max_similarity=similarity
        print(skill,"max_similarity",max_similarity)

        if(max_similarity>=threshold):
            matched.append(skill)
        else:
            missing.append(skill)

    coverage=round((len(matched)/len(skills))*100,2)if skills else 0
    print("coverage:",coverage)
    return coverage,matched,missing