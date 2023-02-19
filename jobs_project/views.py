from django.http import HttpResponse
from django.shortcuts import render
from .models import JobCategory
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import numpy as np



def jobs(request):
    df = pd.read_csv('jobs_project/data/all_data_cleaned.csv')
    job_categories = JobCategory.objects.all()
    
    
    # Top 15 Job Categories
    new_df = df.groupby(by='job_categories')['job_title'].count().sort_values(ascending=True).tail(15).reset_index()
    top_15_job_categories = px.histogram(new_df, x='job_categories', y='job_title',text_auto=True, title="Top 15 Growing job category in Egypt")
    top_15_job_categories.update_layout(xaxis={'categoryorder':'total descending'})
    top_15_job_categories = plot(top_15_job_categories, output_type="div")
    
    # Data Preprocessing
    refilter = True
    if request.GET.get('job_category'):
        refilter = False
        df = df[df['job_categories'] == request.GET.get('job_category')]

    if request.GET.get('career_level'):
        df = df[df['career_level'] == request.GET.get('career_level')]

    if request.GET.get('education_level'):
        df = df[df['education_level'] == request.GET.get('education_level')]

    if request.GET.get('experience_needed'):
        df = df[df['experience_needed'] == request.GET.get('experience_needed')]

    if request.GET.get('gender'):
        df = df[df['gender'] == request.GET.get('gender')]
    
    
    if refilter == True:
        # Top 15 Job Categories
        new_df = df.groupby(by='job_categories')['job_title'].count().sort_values(ascending=True).tail(15).reset_index()
        top_15_job_categories = px.histogram(new_df, x='job_categories', y='job_title',text_auto=True, title="Top 15 Growing job category")
        top_15_job_categories.update_layout(xaxis={'categoryorder':'total descending'})
        top_15_job_categories = plot(top_15_job_categories, output_type="div")
        
    
    
    # category_level
    category_level = px.histogram(df, x='career_level', title="Career Level Needed", text_auto=True)
    category_level.update_layout(xaxis={'categoryorder':'total descending'})
    category_level = plot(category_level, output_type="div")
    
    # experience needed
    experience_needed = px.histogram(df, y='experience_needed', text_auto=True, title="Most wanted experience")
    experience_needed.update_layout(yaxis={'categoryorder':'total ascending'})
    experience_needed = plot(experience_needed, output_type="div")
    
    # education level
    education_level = px.pie(df, 'education_level', hole=0.6, title="Required Education level")
    education_level = plot(education_level, output_type="div")
    
    # gender
    gender = px.pie(df, 'gender', title='Gender Distribution')
    gender = plot(gender, output_type="div")
    
    # top companies
    new_df = df.groupby('company_name')['job_title'].count().reset_index().sort_values('job_title', ascending=False)
    new_df.rename(columns = {'job_title':'num_of_jobs'}, inplace = True)
    top_10_companies = px.histogram(new_df.head(10), 'company_name', 'num_of_jobs', text_auto=True, title='Top 10 companies with job offers in Egypt')
    top_10_companies = plot(top_10_companies, output_type="div")
    
    
    context = {
        'job_categories':job_categories,
        'top_15_job_categories':top_15_job_categories,
        'category_level':category_level,
        'experience_needed':experience_needed,
        'education_level':education_level,
        'gender':gender,
        'top_10_companies':top_10_companies,
    }
    return render(request, 'jobs_project/jobs.html', context)


def load_data_to_database(request):
    data = pd.read_csv('jobs_project/data/all_data_cleaned.csv')

    my_job_categories = data.groupby('job_categories')['job_title'].count().reset_index()
    job_categories = []
    for index, category in my_job_categories['job_categories'].items():
        my_job_category = JobCategory(
            name=str(category)
        )
        job_categories.append(my_job_category)
    
    JobCategory.objects.bulk_create(job_categories)
    return HttpResponse('Done')

